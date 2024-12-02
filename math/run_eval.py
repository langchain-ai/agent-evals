from typing import Optional
from math import isclose

from langsmith import Client, evaluate
from langsmith.evaluation import EvaluationResults

from langgraph.pregel.remote import RemoteGraph


client = Client()

DEFAULT_DATASET_NAME = "Math Evaluation Dataset"
DEFAULT_GRAPH_ID = "agent"
DEFAULT_AGENT_URL = "https://langr.ph/marketplace/b5152a8c-e0ed-4ed9-9bac-9c3cb7566c8d"


def correct(outputs: dict, reference_outputs: dict) -> bool:
    """Evaluator."""
    actual_answer = outputs["output"]
    reference_answer = reference_outputs["Answer"]

    try:
        actual_float = float(actual_answer)
        reference_float = float(reference_answer)
    except (ValueError, TypeError):
        # Return False if conversion to float fails
        return False

    # Compare the floats with precision tolerance
    return isclose(actual_float, reference_float, rel_tol=1e-9, abs_tol=1e-9)


def make_agent_runner(graph_id: str, agent_url: str):
    agent_graph = RemoteGraph(graph_id, url=agent_url)

    def run_agent(inputs: dict):
        return agent_graph.invoke({"question": inputs["Question"]})["value"]

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
        evaluators=[correct],
        experiment_prefix=experiment_prefix,
        metadata=get_agent_metadata(graph_id, agent_url),
    )

    if min_score is not None:
        results_df = results.to_pandas()
        score = results_df["feedback.correct"].mean()
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
