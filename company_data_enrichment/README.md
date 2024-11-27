## Company Data Enrichment

This directory contains evaluation script for the company data enrichment agents.

## Agent schema

High level, company data enrichment agents are expected to take a company and a JSON schema that describes the attributes to extract, and output extracted information in a JSON object. Here is an example:

- Input:

    ```json
    {
      "type": "object",
      "title": "company_data_enrichment_input",
      "required": [
          "company"
      ],
      "properties": {
        "company": {
          "type": "string",
          "title": "Company"
        },
        "extraction_schema": {
          "type": "object",
          "title": "Extraction Schema"
        }
      }
    }
    ```

- Output:

    ```json
    {
      "type": "object",
      "title": "company_data_enrichment_output",
      "required": [
        "info"
      ],
      "properties": {
        "info": {
          "type": "object",
          "title": "Info"
        }
      }
    }
    ```


## Datasets

There are two public datasets available for evaluation in LangSmith:

- [Public companies](https://smith.langchain.com/public/640df79c-1831-494e-8824-d7300205dc8e/d). This dataset has a list of publicly traded companies to extract the following fields for:
  - `name`
  - `description`
  - `website`
  - `linkedin_profile`
  - `headquarters`
  - `employee_count`
  - `ceo`

  Example input:
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

  Example output:

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

- [Startups](https://smith.langchain.com/public/afabd12a-62fa-4c09-b083-6b1742b4cc3a/d). This dataset has a list of AI startups to extract the following fields for:

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

  Example input:

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

  Example output:

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

## Evaluation Metric

Currently there is a single evaluation metric: fraction of the fields that were correctly extracted (per company). Correctness is defined differently depending on the field type:

- exact matches for fields like `founding_year` / `website`
- fuzzy matches for fields like `company_name` / `ceo`
- embedding similarity for fields like `description`
- checking within a certain tolerance (+/- 10%) for fields like `employee_count` / `total_funding_mm_usd`

These can be adjusted in the `run_eval.py` script if you're adapting this to your own dataset.

## Running evals

To evaluate the agent, you can run `company_data_enrichment/run_eval.py` script. This will create new experiments in LangSmith for the two [datasets](#datasets) mentioned above.

**Basic usage:**

```shell
python company_data_enrichment/run_eval.py
```

By default this will use the `Public companies` dataset & `Company mAIstro` agent by LangChain.

**Advanced usage:**

You can pass the following parameters to customize the evaluation:

- `--dataset-id`: ID of the dataset to evaluate against. Defaults to `Public companies` dataset.
- `--graph-id`: graph ID of the agent to evaluate. Defaults to `company_maistro`.
- `--agent-url`: URL of the deployed agent to evaluate. Defaults to `Company mAIstro` deployment.
- `--experiment-prefix`: Prefix for the experiment name.
- `--min-score`: Minimum acceptable score for evaluation. If specified, the script will raise an assertion error if the average score is below this threshold.

```shell
python company_data_enrichment/run_eval.py --experiment-prefix "My custom prefix" --min-score 0.9
```

### Using different schema

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