# Public Company Data Enrichment

This directory contains evaluation script for evaluating an agent on how well it does at researching information about a public company.

## Dataset

The dataset used can be found [here](https://smith.langchain.com/public/afabd12a-62fa-4c09-b083-6b1742b4cc3a/d). This dataset has a list of AI startups to extract the following fields for:
  - `name`
  - `description`
  - `website`
  - `crunchbase_profile`
  - `year_founded`
  - `ceo`
  - `total_funding_mm_usd`
  - `latest_round`
  - `latest_round_date`
  - `latest_round_amount_mm_usd`

<details>
<summary>Example input</summary>


  ```json
  {
    "company": "LangChain",
    "extraction_schema": {
      "type": "object",
      "title": "company_info",
      "required": [
        "name",
        "description",
        "website",
        "crunchbase_profile",
        "year_founded",
        "ceo",
        "total_funding_mm_usd",
        "latest_round",
        "latest_round_date",
        "latest_round_amount_mm_usd"
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
        "latest_round": {
          "type": "string",
          "description": "Type of the most recent funding round (e.g., Series A, Seed, etc.)"
        },
        "year_founded": {
          "type": "integer",
          "minimum": 1800,
          "description": "Year when the company was founded"
        },
        "latest_round_date": {
          "type": "string",
          "format": "date",
          "description": "Date of the most recent funding round (YYYY-MM-DD)"
        },
        "crunchbase_profile": {
          "type": "string",
          "format": "uri",
          "description": "Company's Crunchbase profile URL"
        },
        "total_funding_mm_usd": {
          "type": "number",
          "minimum": 0,
          "description": "Total funding raised in millions of USD"
        },
        "latest_round_amount_mm_usd": {
          "type": "number",
          "minimum": 0,
          "description": "Amount raised in the most recent funding round in millions of USD"
        }
      },
      "description": "Company information"
    }
  } 
  ```
</details>
<br>
<details>
<summary>Example output</summary>

  ```json
  {
    "info": {
      "ceo": "Harrison Chase",
      "name": "LangChain, Inc.",
      "website": "https://www.langchain.com",
      "description": "LangChain helps developers to build applications powered by large language models (LLMs). It provides tools and frameworks to integrate LLMs with external data sources and APIs, facilitating the creation of advanced AI applications.",
      "latest_round": "Series A",
      "year_founded": 2022,
      "latest_round_date": "2024-02-15",
      "crunchbase_profile": "https://www.crunchbase.com/organization/langchain",
      "total_funding_mm_usd": 35,
      "latest_round_amount_mm_usd": 25
    }
  }
  ```
</details>

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
    # see the `Example input` for reference on what `inputs` dict will look like
    return {"my_agent_key": inputs["company"], ...}


def transform_agent_outputs(outputs: dict) -> dict:
    """Transform agent outputs to match the LangSmith dataset output schema."""
    # see the `Example output` for reference on what the output from `run_agent` would look like
    return {"info": response["my_agent_output_key"]}
```

`transform_dataset_inputs` will be applied to LangSmith dataset inputs before invoking the agent, and `transform_agent_outputs` will be applied to the agent's response before it's compared to the expected output in the LangSmith eval dataset.

## Running evals

To evaluate the agent, you can run `startup_data_enrichment/run_eval.py` script. This will create new experiments in LangSmith for the two [datasets](#datasets) mentioned above.

By default this will use the `Startup Data Enrichment` dataset & `Company mAIstro` agent by LangChain.

```shell
python startup_data_enrichment/run_eval.py --experiment-prefix "My custom prefix"
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

This will start a local server that you can interact with using `RemoteGraph`. Simply pass local URL for `agent-url` parameter:

```shell
python startup_data_enrichment/run_eval.py --experiment-prefix "My custom prefix" --agent-url http://localhost:8123
```