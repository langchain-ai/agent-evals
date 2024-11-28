import json
from typing import Optional

from langchain.evaluation import load_evaluator
from langgraph.pregel.remote import RemoteGraph
from langsmith import Client, evaluate
from langsmith.evaluation import EvaluationResults

try:
    import rapidfuzz
except ImportError:
    raise ImportError("Please install rapidfuzz using `pip install rapidfuzz`")


client = Client()

evaluator = load_evaluator("json_edit_distance")

DEFAULT_DATASET_ID = "9d30ea55-2979-439e-b60c-0f76f63f06b8"
DEFAULT_GRAPH_ID = "agent"

DEFAULT_AGENT_URL = (
    "https://api.smith.langchain.com/marketplace/9374a917-2b04-48d4-ac0b-1c9e6ab7abc9"
)


def score(inputs: dict, outputs: dict, reference_outputs: dict) -> float:
    """Evaluator."""

    extracted_records = outputs.get("data", [])
    expected_records = reference_outputs["output"]
    actual = json.dumps(extracted_records, sort_keys=True, indent=False)
    expected = json.dumps(expected_records, sort_keys=True, indent=False)
    score = (
        1 - evaluator.evaluate_strings(prediction=actual, reference=expected)["score"]
    )
    return score


def make_agent_runner(graph_id: str, agent_url: str):
    agent_graph = RemoteGraph(graph_id, url=agent_url)

    def run_agent(inputs: dict):
        result = agent_graph.invoke(
            {"url": inputs["url"], "json_schema": inputs["json_schema"]}
        )
        # Project to remove unnecessary fields
        return {
            "data": result["data"],
        }

    return run_agent


def get_agent_metadata(graph_id: str, agent_url: str):
    if "marketplace" in agent_url:
        project_id = agent_url.split("/")[-1]
        return {"project_id": project_id, "graph_id": graph_id}
    return {"graph_id": graph_id}


def run_eval(
    *,
    dataset_id: str,
    graph_id: str = DEFAULT_GRAPH_ID,
    agent_url: str = DEFAULT_AGENT_URL,
    experiment_prefix: Optional[str] = None,
) -> EvaluationResults:
    dataset = client.read_dataset(dataset_id=dataset_id)
    run_agent = make_agent_runner(graph_id, agent_url)
    results = evaluate(
        run_agent,
        data=dataset,
        evaluators=[score],
        experiment_prefix=experiment_prefix,
        metadata=get_agent_metadata(graph_id, agent_url),
    )

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset-id",
        type=str,
        default=DEFAULT_DATASET_ID,
        help="ID of the dataset to evaluate against",
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
        dataset_id=args.dataset_id,
        graph_id=args.graph_id,
        agent_url=args.agent_url,
        experiment_prefix=args.experiment_prefix,
    )
