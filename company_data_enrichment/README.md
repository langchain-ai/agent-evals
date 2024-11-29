## Public Company Data Enrichment

This directory contains evaluation script for evaluating an agent on how well it does at researching information about a public company.

## Dataset

The dataset used can be found [here](https://smith.langchain.com/public/640df79c-1831-494e-8824-d7300205dc8e/d). 
This dataset has a list of publicly traded companies to extract the following fields for:
  - `name`
  - `description`
  - `website`
  - `linkedin_profile`
  - `headquarters`
  - `employee_count`
  - `ceo`

<details>
<summary>Example input:</summary>
<br>

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
<summary>Example output:</summary>
<br>

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


## Evaluation Metric

Currently there is a single evaluation metric: fraction of the fields that were correctly extracted (per company).
This is evaluated by asking an LLM to produce a score.

## Invoking the agent

// TODO: add something about how to invoke the agent based on the schema. IMO we should make this really easy, as I think its pretty unlikely agents would have the same exact schema

## Running evals

To evaluate the agent, you can run `company_data_enrichment/run_eval.py` script. This will create new experiments in LangSmith for the two [datasets](#datasets) mentioned above.

**Basic usage:**

```shell
python company_data_enrichment/run_eval.py
```

By default this will use the `Public companies` dataset & `Company mAIstro` agent by LangChain.

**Advanced usage:**

You can pass the following parameters to customize the evaluation:

- `--dataset-name`: Name of the dataset to evaluate against. Defaults to `Public Company Data Enrichment` dataset.
- `--graph-id`: graph ID of the agent to evaluate. Defaults to `company_maistro`.
- `--agent-url`: URL of the deployed agent to evaluate. Defaults to `Company mAIstro` deployment.
- `--experiment-prefix`: Prefix for the experiment name.

```shell
python company_data_enrichment/run_eval.py --experiment-prefix "My custom prefix"
```

### Testing a local agent

If your agent uses a schema that's different from the [example one above](#agent-schema), you can modify `make_agent_runner` in `run_eval.py` in the following way:

```python
def make_agent_runner(agent_id: str, agent_url: str):
    agent_graph = RemoteGraph(agent_id, url=agent_url)

    def run_agent(inputs: dict):
        # transform the inputs (single LangSmith dataset record) to match the agent's schema
        transformed_inputs = {"my_agent_key": inputs["company"], ...}
        response = agent_graph.invoke(transformed_inputs)
        # transform the agent outputs to match expected eval schema
        transformed_outputs = {"info": response["my_agent_output_key"]}
        return transformed_outputs

    return run_agent
```