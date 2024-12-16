# visualsearch-backend

Allow Salesforce Agentforce agents to provide clothing recommendations to user based on pictures they provide. A user provides a picture of a cool leather jacket they like and Agentforce provides the most similar jackets from its inventory.

## Setup

### Python backend

- Create venv, pip install what's in requirements.txt etc
- Repo runs directly in Heroku

### Salesforce

- Create named credentials and unauthenticated external credentials
- Create external service, use the OpenAPI 3.0 spec in the repo
- Create a custom object to model the data (clothing Item)
- Create a flow with input URL and output record list
  - Call out the external service
  - Transform the data to the custom object format
  - Assign custom object to output variables
- Add permission set for agent user to access external credentials
  - Either employee user using the assistive agent or agent service user using customer agent
- Add flow to agent actions
- Add agent action to specific agent with topic, instructions etc