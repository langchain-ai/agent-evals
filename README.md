# Agent Evals

This is a collection of evaluation scripts for evaluating agents.

## Repo Structure

Each folder in the repo contains:

- `README.md`: A description of the evaluation (dataset, metrics, how to run the eval)
- `run_eval.py`: A script to run the evaluation

## Available evals

Below is the list of currently available evals:
| Task | Dataset | Description | Input Example | Output Example |
|------|----------|-------------|---------------|----------------|
| [Math](./math) | [Math Problems](https://smith.langchain.com/public/14f42e3e-4272-4609-8322-4beaff2f2eef/d) | Solve math problems and return numerical answers | `{"Question": "Find the second derivative of f(x)=ln(x) and evaluate it at x=0.5."}` | `{"Answer": "-4"}` |
| [Company Data Enrichment](./company_data_enrichment) | [Public Companies](https://smith.langchain.com/public/bb139cd5-c656-4323-9bea-84cb7bf6080a/d) | Extract structured company information like CEO, headquarters, employee count etc. | `{"company": "Nvidia", "extraction_schema": {...}}` | `{"info": {"ceo": "Jensen Huang", "name": "Nvidia Corporation", ...}}` |
| [People Data Enrichment](./people_data_enrichment) | [People Dataset](https://smith.langchain.com/public/bb139cd5-c656-4323-9bea-84cb7bf6080a/d) | Extract structured information about people like work experience, role, company etc. | `{"person": {"name": "Erick Friis", "email": "erick@langchain.dev", ...}, "extraction_schema": {...}}` | `{"extracted_information": {"Years-Experience": 10, "Company": "LangChain", ...}}` |