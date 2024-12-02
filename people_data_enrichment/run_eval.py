from langsmith import Client, evaluate
from Levenshtein import ratio
from langgraph.pregel.remote import RemoteGraph
from typing import Optional
from langsmith.evaluation import EvaluationResults
import argparse

# Defaults
EXPERIMENT_PREFIX = "People mAIstro "
TOLERANCE = 0.15  # should match within 15%
NUMERIC_FIELDS = ("Years-Experience",)
FUZZY_MATCH_FIELDS = ("Role", "Company")
LIST_OF_STRING_FIELDS = ("Prior-Companies",)
DEFAULT_DATASET_NAME = "People Data Enrichment"
DEFAULT_GRAPH_ID = "people_maistro"
DEFAULT_AGENT_URL = "https://langr.ph/marketplace/62bf5890-28fa-4dd1-b469-4751fe7ecdf3"

client = Client()

extraction_schema = {
    "type": "object",
    "required": [
        "Years-Experience",
        "Company",
        "Role",
        "Prior-Companies",
    ],
    "properties": {
        "Role": {"type": "string", "description": "Current role of the person."},
        "Years-Experience": {
            "type": "number",
            "description": "How many years of full time work experience (excluding internships) does this person have.",
        },
        "Company": {
            "type": "string",
            "description": "The name of the current company the person works at.",
        },
        "Prior-Companies": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of previous companies where the person has worked",
        },
    },
    "description": "Person information",
    "title": "Person-Schema",
}


def evaluate_list_of_string_fields(outputs: dict, reference_outputs: dict):
    field_to_score = {}
    for k in LIST_OF_STRING_FIELDS:
        if k not in reference_outputs:
            continue

        output_list = outputs.get(k, [])
        reference_list = reference_outputs[k].split(", ")

        # Convert to lists if needed
        if isinstance(output_list, str):
            output_list = [output_list]
        if isinstance(reference_list, str):
            reference_list = [reference_list]

        # Convert to lowercase
        output_list = [str(item).lower() for item in output_list]
        reference_list = [str(item).lower() for item in reference_list]

        if not output_list or not reference_list:
            score = 0.0
        else:
            # For each reference item, find the best ratio match in output
            scores = []
            for ref_item in reference_list:
                best_ratio = max(ratio(ref_item, out_item) for out_item in output_list)
                scores.append(best_ratio)

            # Average the ratios
            score = sum(scores) / len(scores)

        field_to_score[k] = score
    return field_to_score


def evaluate_numeric_fields(outputs: dict, reference_outputs: dict):
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

    actual_person_info = outputs["info"]
    expected_person_info = reference_outputs

    results = {
        **evaluate_numeric_fields(actual_person_info, expected_person_info),
        **evaluate_fuzzy_match_fields(actual_person_info, expected_person_info),
        **evaluate_list_of_string_fields(actual_person_info, expected_person_info),
    }
    return sum(results.values()) / len(results)


def transform_dataset_inputs(inputs: dict) -> dict:
    """Transform LangSmith dataset inputs to match the agent's input schema before invoking the agent."""
    # see the `Example input` in the README for reference on what `inputs` dict should look like
    return {
        "person": {
            "name": inputs["Person"],
            "email": inputs["Work-Email"],
            "linkedin": inputs["Linkedin"],
        },
        "extraction_schema": extraction_schema,
    }


def transform_agent_outputs(outputs: dict) -> dict:
    """Transform agent outputs to match the LangSmith dataset output schema."""
    # see the `Example output` in the README for reference on what the output should look like
    # the agent outputs already match the dataset output schema, but you can add any additional processing here
    return outputs


def make_agent_runner(graph_id: str, agent_url: str):
    """Wrapper that transforms inputs/outputs to match the expected eval schema and invokes the agent."""
    agent_graph = RemoteGraph(graph_id, url=agent_url)

    def run_agent(inputs: dict) -> dict:
        """Run the agent on the inputs from the LangSmith dataset record, return outputs conforming to the LangSmith dataset output schema."""
        transformed_inputs = transform_dataset_inputs(inputs)
        response = agent_graph.invoke(transformed_inputs)
        return transform_agent_outputs(response)

    return run_agent


def get_agent_metadata(graph_id: str, agent_url: str):
    if "marketplace" in agent_url:
        project_id = agent_url.split("/")[-1]
        return {"project_id": project_id, "graph_id": graph_id}
    return {"graph_id": graph_id}


def run_eval(
    *,
    dataset_name: str = DEFAULT_DATASET_NAME,
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
        blocking=True,
    )
    return results


# Update main block
if __name__ == "__main__":
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
