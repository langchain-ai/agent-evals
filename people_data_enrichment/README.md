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

## Datasets

There is one dataset for public evaluation in LangSmith:

- [People Information](https://smith.langchain.com/public/bb139cd5-c656-4323-9bea-84cb7bf6080a/d). This dataset has a list of peopl to extract the following fields for:
  - `


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

To evaluate the People mAIstro agent, you can run `evals/test_agent.py` script. This will create new experiments in LangSmith for the [dataset](#dataset) mentioned above.

Basic usage:

```shell
python evals/test_agent.py
```

You can also customize additional parameters such as the maximum number of concurrent runs and the experiment prefix.

```shell
python evals/test_agent.py --max-concurrency 4 --experiment-prefix "My custom prefix"
```