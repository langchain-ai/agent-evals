from typing import Any, Optional

from Levenshtein import ratio
from langchain_anthropic import ChatAnthropic
from langsmith import Client, evaluate
from langsmith.evaluation import LangChainStringEvaluator, EvaluationResults

from langgraph.pregel.remote import RemoteGraph


client = Client()

TOLERANCE = 0.10  # should match within 10%
NUMERIC_FIELDS = ("employee_count",)
EXACT_MATCH_FIELDS = (
    "website",
    "linkedin_profile",
    "headquarters",
)
FUZZY_MATCH_FIELDS = ("name", "ceo")
LONG_TEXT_FIELDS = ("description",)

DEFAULT_DATASET_NAME = "Public Company Data Enrichment"
DEFAULT_GRAPH_ID = "company_maistro"
DEFAULT_AGENT_URL = "https://langr.ph/marketplace/f7dcd212-1bd9-4596-a630-acc6ac4ff2f6"


# evaluation helpers for different types of fields


def evaluate_numeric_fields(outputs: dict, reference_outputs: dict) -> dict[str, float]:
    lower_bound = 1 - TOLERANCE
    upper_bound = 1 + TOLERANCE
    field_to_score = {}
    for k in NUMERIC_FIELDS:
        if k not in reference_outputs:
            continue

        raw_field_value = outputs.get(k, 0)
        try:
            score = float(
                lower_bound
                <= int(raw_field_value) / reference_outputs[k]
                <= upper_bound
            )
        except ValueError:
            score = 0.0

        field_to_score[k] = score
    return field_to_score


def _preprocess_value(value: Any) -> Any:
    if isinstance(value, str):
        # for urls
        return value.rstrip("/")

    return value


def evaluate_exact_match_fields(
    outputs: dict, reference_outputs: dict
) -> dict[str, float]:
    return {
        k: float(
            _preprocess_value(outputs.get(k)) == _preprocess_value(reference_outputs[k])
        )
        for k in EXACT_MATCH_FIELDS
        if k in reference_outputs
    }


def evaluate_long_text_fields(outputs: dict, reference_outputs: dict):
    emb_distance_evaluator = LangChainStringEvaluator(
        "embedding_distance", config={"distance": "cosine"}
    )
    return {
        k: 1
        - emb_distance_evaluator.evaluator.invoke(
            {"prediction": outputs.get(k, ""), "reference": reference_outputs[k]}
        )["score"]
        for k in LONG_TEXT_FIELDS
        if k in reference_outputs
    }


def evaluate_fuzzy_match_fields(outputs: dict, reference_outputs: dict):
    return {
        k: ratio(outputs.get(k, "").lower(), reference_outputs[k].lower())
        for k in FUZZY_MATCH_FIELDS
        if k in reference_outputs
    }


# effectively fraction of matching fields
def evaluate_agent(outputs: dict, reference_outputs: dict):
    if "info" not in outputs or not isinstance(outputs["info"], dict):
        return 0.0

    actual_company_info = outputs["info"]
    expected_company_info = reference_outputs["info"]

    results = {
        **evaluate_numeric_fields(actual_company_info, expected_company_info),
        **evaluate_exact_match_fields(actual_company_info, expected_company_info),
        **evaluate_fuzzy_match_fields(actual_company_info, expected_company_info),
    }
    return sum(results.values()) / len(results)


def get_agent_metadata(graph_id: str, agent_url: str):
    if "marketplace" in agent_url:
        project_id = agent_url.split("/")[-1]
        return {"project_id": project_id, "graph_id": graph_id}
    return {"graph_id": graph_id}


# PUBLIC API


def transform_dataset_inputs(inputs: dict) -> dict:
    """Transform LangSmith dataset inputs to match the agent's input schema before invoking the agent."""
    # see the `Example input` in the README for reference on what `inputs` dict should look like
    # the dataset inputs already match the agent's input schema, but you can add any additional processing here
    return inputs


def transform_agent_outputs(inputs: dict, outputs: dict) -> dict:
    """Transform agent outputs to match the LangSmith dataset output schema."""
    # see the `Example output` in the README for reference on what the output should look like
    outputs["info"] = get_structured_output(outputs["info"], inputs["extraction_schema"])
    return outputs


def make_agent_runner(graph_id: str, agent_url: str):
    """Wrapper that transforms inputs/outputs to match the expected eval schema and invokes the agent."""
    agent_graph = RemoteGraph(graph_id, url=agent_url)

    def run_agent(inputs: dict) -> dict:
        """Run the agent on the inputs from the LangSmith dataset record, return outputs conforming to the LangSmith dataset output schema."""
        transformed_inputs = transform_dataset_inputs(inputs)
        response = agent_graph.invoke(transformed_inputs)
        return transform_agent_outputs(inputs, response)

    return run_agent


EXTRACTION_PROMPT = """Your task is to take information gathered from web research and extract it into the following schema.

<schema>
{extraction_schema}
</schema>

Here is all of the information gathered from the research:

<research_info>
{info}
</research_info>
"""


def get_structured_output(output: str, extraction_schema: dict) -> dict:
    """Convert unstructured (text) output to structured output conforming to the dataset output schema."""
    llm = ChatAnthropic(model="claude-3-5-sonnet-latest").with_structured_output(
        extraction_schema
    )
    system_prompt = EXTRACTION_PROMPT.format(
        extraction_schema=extraction_schema, info=output
    )
    output = llm.invoke(
        [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": "Produce a structured output from this information.",
            },
        ]
    )
    return output


def run_eval(
    *,
    dataset_name: str,
    graph_id: str = DEFAULT_GRAPH_ID,
    agent_url: str = DEFAULT_AGENT_URL,
    experiment_prefix: Optional[str] = None,
) -> EvaluationResults:
    dataset = client.read_dataset(dataset_name=dataset_name)
    run_agent = make_agent_runner(graph_id, agent_url)
    results = evaluate(
        run_agent,
        data=dataset,
        evaluators=[evaluate_agent],
        experiment_prefix=experiment_prefix,
        metadata=get_agent_metadata(graph_id, agent_url),
    )
    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset-name",
        type=str,
        default=DEFAULT_DATASET_NAME,
        help="Name of the dataset to evaluate against",
    )
    parser.add_argument(
        "--graph-id",
        type=str,
        default=DEFAULT_GRAPH_ID,
        help="ID of the graph to evaluate",
    )
    parser.add_argument(
        "--agent-url",
        type=str,
        default=DEFAULT_AGENT_URL,
        help="URL of the deployed agent to evaluate",
    )
    parser.add_argument(
        "--experiment-prefix",
        type=str,
        help="Experiment prefix for the evaluation",
    )
    args = parser.parse_args()

    run_eval(
        dataset_name=args.dataset_name,
        graph_id=args.graph_id,
        agent_url=args.agent_url,
        experiment_prefix=args.experiment_prefix,
    )
