## People Data Enrichment

This directory contains evaluation script for the people data enrichment agents.

## Agent schema

People data enrichment agents are expected to have the following schema:

- Input:

    ```json
    {
      "type": "object",
      "title": "people_data_enrichment_input",
      "required": [
          "person"
      ],
      "properties": {
          "person": {
              "type": "object",
              "title": "Person",
              "properties": {
                  "name": {
                      "type": "string",
                      "title": "Name"
                  },
                  "company": {
                      "type": "string",
                      "title": "Company"
                  },
                  "linkedin": {
                      "type": "string",
                      "title": "LinkedIn URL"
                  },
                  "email": {
                      "type": "string",
                      "title": "Email"
                  },
                  "role": {
                      "type": "string",
                      "title": "Role"
                  }
              },
              "required": ["email"]
          },
          "extraction_schema": {
          "type": "object",
          "title": "Extraction Schema"
          },
          "user_notes": {
          "type": "string",
          "title": "User Notes",
          },
      }
    }
    ```

- Output:

    ```json
    {
      "type": "object",
      "title": "person_data_enrichment_output",
      "required": [
          "extracted_information"
      ],
      "properties": {
          "extracted_information": {
          "type": "object",
          "title": "Extracted Information"
          }
      }
    }
    ```

## Dataset

There is one dataset for public evaluation in LangSmith:

- [People Dataset](https://smith.langchain.com/public/2af89d2a-93f6-4c84-80ac-70defcfd14c8/d). This dataset has a list of people to extract the following fields for:
  - `Years-Experience`
  - `Company`
  - `Role`
  - `Prior-Companies`


Example input:
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
      "Years-Experience",
      "Company",
      "Role",
      "Prior-Companies"
    ],
    "properties": {
      "Role": {
        "type": "string",
        "description": "Current role of the person."
      },
      "Company": {
        "type": "string",
        "description": "The name of the current company the person works at."
      },
      "Prior-Companies": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "List of previous companies where the person has worked"
      },
      "Years-Experience": {
        "type": "number",
        "description": "How many years of full time work experience (excluding internships) does this person have."
      }
    },
    "description": "Person information"
  }
}
```

Example output:
```json
{
    "extracted_information": {
        "Role": "Exploring new ideas and building out next project",
        "Company": "South Park Commons",
        "Prior-Companies": [
        "Instabase",
        "Chestnut",
        "MIT"
        ],
        "Years-Experience": 5
  }
}
```

## Evaluation Metric

Currently there is a single evaluation metric: fraction of the fields that were correctly extracted (per person). Correctness is defined differently depending on the field type:

- fuzzy matching for list of string fields such as `Prior-Companies`
- fuzzy matches for fields like `Role` / `Company`
- checking within a certain tolerance (+/- 15%) for `Years-Experience` field

### Running evals

To evaluate the People mAIstro agent, you can run the `run_eval.py` script. This will create new experiments in LangSmith for the [dataset](#dataset) mentioned above.

**Basic usage:**

```shell
python people_data_enrichment/run_eval.py
```

By default this will use the `Person Researcher Dataset` dataset & `People mAIstro` agent by LangChain.

**Advanced usage:**

You can pass the following parameters to customize the evaluation:

- `--dataset-name`: Name of the dataset to evaluate against. Defaults to `Person Researcher Dataset` dataset.
- `--agent-id`: ID of the agent to evaluate. Defaults to `people_maistro`.
- `--agent-url`: URL of the deployed agent to evaluate. Defaults to `People mAIstro` deployment.
- `--experiment-prefix`: Prefix for the experiment name.
- `--min-score`: Minimum acceptable score for evaluation. If specified, the script will raise an assertion error if the average score is below this threshold.

```shell
python company_data_enrichment/run_eval.py --experiment-prefix "My custom prefix" --min-score 0.9
```

### Using different schema

#### Different Extraction Schema

If you want to use a different extraction schema, you can modify the `extraction_schema` variable in `run_eval.py` to match whatever extraction schema you are looking for.

#### Different Agent Schema

If your agent uses a schema that's different from the [example one above](#agent-schema), you can modify `make_agent_runner` in `run_eval.py` in the following way:

```python
def make_agent_runner(agent_id: str, agent_url: str):
    agent_graph = RemoteGraph(agent_id, url=agent_url)

    def run_agent(inputs: dict):
        # transform the inputs (single LangSmith dataset record) to match the agent's schema
        transformed_inputs = {"my_agent_key": inputs["Person"], ...}
        response = agent_graph.invoke(transformed_inputs)
        # transform the agent outputs to match expected eval schema
        transformed_outputs = {"info": response["my_agent_output_key"]}
        return transformed_outputs

    return run_agent
```
