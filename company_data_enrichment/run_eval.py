from typing import Any, Optional

from Levenshtein import ratio
from langsmith import Client, evaluate
from langsmith.evaluation import LangChainStringEvaluator, EvaluationResults

from langgraph.pregel.remote import RemoteGraph


client = Client()

TOLERANCE = 0.10  # should match within 10%
NUMERIC_FIELDS = (
    "employee_count",
    "total_funding_mm_usd",
    "latest_round_amount_mm_usd",
)
EXACT_MATCH_FIELDS = (
    "website",
    "crunchbase_profile",
    "linkedin_profile",
    "headquarters",
    "year_founded",
    "latest_round",
    "latest_round_date",
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


def make_agent_runner(graph_id: str, agent_url: str):
    agent_graph = RemoteGraph(graph_id, url=agent_url)

    def run_agent(inputs: dict):
        response = agent_graph.invoke(inputs)
        return {"info": response["info"]}

    return run_agent


def get_agent_metadata(graph_id: str, agent_url: str):
    if "marketplace" in agent_url:
        project_id = agent_url.split("/")[-1]
        return {"project_id": project_id, "graph_id": graph_id}
    return {"graph_id": graph_id}


def run_eval(
    *,
    dataset_name: str,
    graph_id: str = DEFAULT_GRAPH_ID,
    agent_url: str = DEFAULT_AGENT_URL,
    experiment_prefix: Optional[str] = None,
    min_score: Optional[float] = None,
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

    if min_score is not None:
        results_df = results.to_pandas()
        score = results_df["feedback.evaluate_agent"].mean()
        if score < min_score:
            raise AssertionError(
                f"Average fraction of correctly extracted fields ({score}) is less than min expected score of {min_score}"
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
    parser.add_argument(
        "--min-score",
        type=float,
        help="Minimum acceptable score for evaluation",
    )
    args = parser.parse_args()

    run_eval(
        dataset_name=args.dataset_name,
        graph_id=args.graph_id,
        agent_url=args.agent_url,
        experiment_prefix=args.experiment_prefix,
        min_score=args.min_score,
    )