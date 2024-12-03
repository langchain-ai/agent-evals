# Agent Evals

This is a collection of evaluation scripts for evaluating agents.

## Repo Structure

Each folder in the repo contains:

- `README.md`: A description of the evaluation (dataset, metrics, how to run the eval)
- `run_eval.py`: A script to run the evaluation

## Available evals

Below is the list of currently available evals:
| Task | Dataset(s) | Description | Input Example | Output Example |
|------|----------|-------------|---------------|----------------|
| [Math](./math) | [Math Problems](https://smith.langchain.com/public/e0993f2f-c055-4446-afc2-e52da6a4dda0/d) | Solve math problems and return numerical answers | `{"Question": "Find the second derivative of f(x)=ln(x) and evaluate it at x=0.5."}` | `{"Answer": "-4"}` |
| [Public Company Data Enrichment](./public_company_data_enrichment) | [Public Companies](https://smith.langchain.com/public/640df79c-1831-494e-8824-d7300205dc8e/d) | Extract structured company information like CEO, headquarters, employee count etc. | `{"company": "Nvidia", "extraction_schema": {...}}` | `{"info": {"ceo": "Jensen Huang", "name": "Nvidia Corporation", ...}}` |
| [Startup Data Enrichment](./startup_data_enrichment) | [Startups](https://smith.langchain.com/public/afabd12a-62fa-4c09-b083-6b1742b4cc3a/d) | Extract structured company information like latest round, total funding, year founded etc. | `{"company": "LangChain", "extraction_schema": {...}}` | `{"info": {"latest_round": "Series A", ...}}` |
| [People Data Enrichment](./people_data_enrichment) | [People Dataset](https://smith.langchain.com/public/3384cc3a-722c-4eb1-8e41-dff56fea05b8/d) | Extract structured information about people like work experience, role, company etc. | `{"person": {"name": "Erick Friis", "email": "erick@langchain.dev", ...}, "extraction_schema": {...}}` | `{"extracted_information": {"Years-Experience": 10, "Company": "LangChain", ...}}` |