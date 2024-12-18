# Math

This directory contains evaluation script for the math agents.

## Agent schema

High level, math agents are expected to take a math question and output the answer. Here is an example:

- Input:

    ```json
    {
      "type": "object",
      "title": "calculate",
      "required": [
          "question"
      ],
      "properties": {
        "question": {
          "type": "string",
          "title": "Question"
        }
      }
    }
    ```

- Output:

    ```json
    {
      "type": "object",
      "title": "math_output",
      "required": [
        "answer"
      ],
      "properties": {
        "answer": {
          "anyOf": [
            {
              "type": "number"
            },
            {
              "type": "integer"
            },
            {
              "type": "null"
            }
          ],
          "title": "Answer"
        }
      }
    }
    ```


## Datasets

There is a standard math problems dataset for evaluation in LangSmith:

- [Simple Math Problems Dataset](https://smith.langchain.com/public/4295b2cf-7a79-415d-97d0-b3639e990848/d). This dataset has a list of math problems consisting of questions and answers.

  Example input:
  ```json
  {
    "question": "Find the second derivative of f(x)=ln(x) and evaluate it at x=0.5."
  }
  ```

  Example output:

  ```json
  {
    "answer": "-4"
  }
  ```

## Evaluation Metric

A score is calculated based on the correctness of the answer based on the following rules:

| **Condition**                                                     | **Score** |
|-------------------------------------------------------------------|-----------|
| Answer is correct (within precision tolerance of expected answer) | 1         |
| Answer is incorrect                                               | -1        |
| Answer is not provided, but question can be answered              | 0         |
| Answer is not provided, but question cannot be answered           | 1         |

These can be adjusted in the `run_eval.py` script if you're adapting this to your own dataset.

## Running evals

To evaluate the agent, you can run `math/run_eval.py` script. This will create new experiments in LangSmith for the [dataset](#datasets) mentioned above.

**Basic usage:**

```shell
python math/run_eval.py
```

By default, this will use the `Math problems` dataset & `Calc you later` agent by LangChain.

**Advanced usage:**

You can pass the following parameters to customize the evaluation:

- `--dataset-name`: Name of the dataset to evaluate against. Defaults to `Math Evaluation Dataset` dataset.
- `--graph-id`: graph ID of the agent to evaluate. Defaults to `agent`.
- `--agent-url`: URL of the deployed agent to evaluate. Defaults to `Calc you later` deployment.
- `--experiment-prefix`: Prefix for the experiment name.
- `--min-score`: Minimum acceptable score for evaluation. If specified, the script will raise an assertion error if the average score is below this threshold.

```shell
python math/run_eval.py --experiment-prefix "My custom prefix" --min-score 0.9
```

### Using different schema

If your agent uses a schema that's different from the [example one above](#agent-schema), you can modify `make_agent_runner` in `run_eval.py` in the following way:

```python
def make_agent_runner(agent_id: str, agent_url: str):
    agent_graph = RemoteGraph(agent_id, url=agent_url)

    def run_agent(inputs: dict):
        # transform the inputs (single LangSmith dataset record) to match the agent's schema
        transformed_inputs = {"my_agent_key": inputs["question"], ...}
        response = agent_graph.invoke(transformed_inputs)
        # transform the agent outputs to match expected eval schema
        transformed_outputs = {"answer": response["my_agent_output_key"]}
        return transformed_outputs

    return run_agent
```
