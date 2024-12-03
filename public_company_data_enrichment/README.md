# Public Company Data Enrichment

This directory contains evaluation script for evaluating an agent on how well it does at researching information about a public company.

## Dataset

The dataset used can be found [here](https://smith.langchain.com/public/640df79c-1831-494e-8824-d7300205dc8e/d). This dataset has a list of publicly traded companies to do research on and extract the following fields for:
  - `name`
  - `description`
  - `website`
  - `linkedin_profile`
  - `headquarters`
  - `employee_count`
  - `ceo`

<details>
<summary>Example input</summary>

  ```json
  {
    "company": "Nvidia",
    "extraction_schema": {
      "type": "object",
      "title": "company_info",
      "required": [
        "name",
        "description",
        "website",
        "linked_profile",
        "headquarters",
        "employee_count",
        "ceo"
        ],
      "properties": {
      "ceo": {
        "type": "string",
        "description": "Name of the company's CEO"
      },
      "name": {
        "type": "string",
        "description": "Official company name"
      },
      "website": {
        "type": "string",
        "format": "uri",
        "description": "Company's official website URL"
      },
      "description": {
        "type": "string",
        "description": "Brief description of the company and its activities"
      },
      "headquarters": {
        "type": "string",
        "description": "Location of company headquarters, formatted as <city>, <state code> (e.g. San Francisco, CA)"
      },
      "employee_count": {
        "type": "integer",
        "minimum": 0,
        "description": "Number of employees in the company"
      },
      "linkedin_profile": {
        "type": "string",
        "format": "uri",
        "description": "Company's LinkedIn profile URL"
      }
      },
      "description": "Company information"
    }
  }
  ```
</details>


<details>

<summary>Example output</summary>

  ```json
  {
    "info": {
      "ceo": "Jensen Huang",
      "name": "Nvidia Corporation",
      "website": "https://www.nvidia.com",
      "description": "Nvidia Corporation is a multinational technology company specializing in the design and manufacture of graphics processing units (GPUs) for gaming, professional visualization, data centers, and automotive markets. The company is a leader in artificial intelligence (AI) computing, providing platforms and solutions that power AI applications across various industries.",
      "headquarters": "Santa Clara, CA",
      "employee_count": 29600,
      "linkedin_profile": "https://www.linkedin.com/company/nvidia"
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
    "https://smith.langchain.com/public/640df79c-1831-494e-8824-d7300205dc8e/d",
    dataset_name="Public Company Data Enrichment"
)
```

(2) create a new dataset with the same examples using the following command:

```shell
python public_company_data_enrichment/create_dataset.py
```

## Evaluation Metric

The extracted outputs are evaluated using LLM-as-a-judge that compares extracted and reference outputs for each company and produces a score between 0 and 1, where 1 is a perfect match and 0 is a complete mismatch.

You can adjust the prompt and evaluation criteria in the `run_eval.py` script if you're adapting this to your own dataset.

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
    # see the `Example output` in the README for reference on what the output should look like
    return {"my_agent_key": inputs["company"], ...}


def transform_agent_outputs(outputs: dict) -> dict:
    """Transform agent outputs to match the LangSmith dataset output schema."""
    # see the `Example output` for reference on what the output should look like
    return {"info": response["my_agent_output_key"]}
```

`transform_dataset_inputs` will be applied to LangSmith dataset inputs before invoking the agent, and `transform_agent_outputs` will be applied to the agent's response before it's compared to the expected output in the LangSmith eval dataset.

## Running evals

First, make sure you have created the dataset as described in the [Using the dataset](#using-the-dataset) section.

To evaluate the agent, you can run `public_company_data_enrichment/run_eval.py` script. This will create new experiments in LangSmith for the two [datasets](#datasets) mentioned above.

By default this will use the `Public Company Data Enrichment` dataset & `Company mAIstro` agent by LangChain.

```shell
python public_company_data_enrichment/run_eval.py --experiment-prefix "My custom prefix"
```

You can pass the following parameters to customize the evaluation:

- `--dataset-name`: Name of the dataset to evaluate against. Defaults to `Public Company Data Enrichment` dataset.
- `--graph-id`: graph ID of the agent to evaluate. Defaults to `company_maistro`.
- `--agent-url`: URL of the deployed agent to evaluate. Defaults to `Company mAIstro` deployment.
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
python public_company_data_enrichment/run_eval.py --experiment-prefix "My custom prefix" --agent-url http://localhost:8123
```