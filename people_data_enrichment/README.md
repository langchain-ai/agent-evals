# People Data Enrichment

This directory contains evaluation script for the people data enrichment agents.

## Dataset

The dataset used can be found [here](https://smith.langchain.com/public/3384cc3a-722c-4eb1-8e41-dff56fea05b8/d). This dataset has a list of people to do research on and extract the following fields for:
  - `years_experience`
  - `current_company`
  - `role`
  - `prior_companies`


<details>
<summary>Example input</summary>

```json
{
  "person": {
    "name": "Erick Friis",
    "role": null,
    "email": "erick@langchain.dev",
    "company": null,
    "linkedin": "https://www.linkedin.com/in/efriis/"
  },
  "extraction_schema": {
    "type": "object",
    "title": "Person-Schema",
    "required": [
      "years_experience",
      "current_company",
      "role",
      "prior_companies"
    ],
    "properties": {
      "role": {
        "type": "string",
        "description": "Current role of the person."
      },
      "current_company": {
        "type": "string",
        "description": "The name of the current company the person works at."
      },
      "prior_companies": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "List of previous companies where the person has worked"
      },
      "years_experience": {
        "type": "number",
        "description": "How many years of full time work experience (excluding internships) does this person have."
      }
    },
    "description": "Person information"
  }
}
```
</details>
<br>
<details>
<summary>Example output</summary>

```json
{
  "extracted_information": {
      "role": "Exploring new ideas and building out next project",
      "current_company": "South Park Commons",
      "prior_companies": [
        "Instabase",
        "Chestnut",
        "MIT"
      ],
      "years_experience": 5
  }
}
```
</details>

### Using the dataset

To use the data from this dataset in your own project, you can:

(1) clone the dataset using LangSmith SDK:

```python
from langsmith import Client
client = Client()

cloned_dataset = client.clone_public_dataset(
    "https://smith.langchain.com/public/3384cc3a-722c-4eb1-8e41-dff56fea05b8/d",
    dataset_name="People Data Enrichment"
)
```

(2) create a new dataset with the same examples using the following command:

```shell
python people_data_enrichment/create_dataset.py
```

## Evaluation Metric

Currently there is a single evaluation metric: fraction of the fields that were correctly extracted (per person). Correctness is defined differently depending on the field type:

- fuzzy matching for list of string fields such as `prior_companies`
- fuzzy matches for fields like `role` / `current_company`
- checking within a certain tolerance (+/- 15%) for `years_experience` field

## Invoking the agent

The agent is invoked using a `RemoteGraph`:

```python
from langgraph.pregel.remote import RemoteGraph

agent_graph = RemoteGraph(agent_id, url=agent_url)
agent_graph.invoke(inputs)
```

### Using different agent schema

Your agent might be using a custom input/output schema that doesn't match the dataset schema. To handle this, you can modify `transform_dataset_inputs` and `transform_agent_outputs` in `run_eval.py` in the following way:

```python

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
```

`transform_dataset_inputs` will be applied to LangSmith dataset inputs before invoking the agent, and `transform_agent_outputs` will be applied to the agent's response before it's compared to the expected output in the LangSmith eval dataset.

## Running evals

First, make sure you have created the dataset as described in the [Using the dataset](#using-the-dataset) section.

To evaluate the agent, you can run `people_data_enrichment/run_eval.py` script. This will create new experiments in LangSmith for the two [datasets](#datasets) mentioned above.

By default this will use the `People Data Enrichment` dataset & `People mAIstro` agent by LangChain.

```shell
python people_data_enrichment/run_eval.py --experiment-prefix "My custom prefix"
```

You can pass the following parameters to customize the evaluation:

- `--dataset-name`: Name of the dataset to evaluate against. Defaults to `People Data Enrichment` dataset.
- `--graph-id`: graph ID of the agent to evaluate. Defaults to `people_maistro`.
- `--agent-url`: URL of the deployed agent to evaluate. Defaults to `People mAIstro` deployment.
- `--experiment-prefix`: Prefix for the experiment name.

### Testing the agent locally

#### Import agent

You can import the compiled LangGraph graph object corresponding to your agent and that as `agent_graph` in `run_eval.py` instead of `RemoteGraph`. Then you can run the evaluation script as usual - `graph-id` and `agent-url` params will be ignored.

#### Run local LangGraph server

You can test the agent locally by using [LangGraph CLI](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/#launch-langgraph-server). From the directory that contains the `langgraph.json` configuration file, run

```shell
langgraph dev
```

This will start a local server that you can interact with using `RemoteGraph`.

Then simply pass local URL for `agent-url` parameter and run the evaluation script as before:

```shell
python people_data_enrichment/run_eval.py --experiment-prefix "My custom prefix" --agent-url http://localhost:8123
```