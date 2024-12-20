# visualsearch-backend

The `visualsearch-backend` is a web service designed to assist Salesforce Agentforce agents in providing clothing recommendations to users based on images they provide. For example, a user can upload a picture of a cool leather jacket they like, and the service will return the most similar jackets from the inventory.

<img src="./2024-12-20-agentforce-sdk-visual-search.gif" height="610" width="282" alt="Visual Search GIF">

In addition to the web service, you will need to configure your Agentforce agent to route clothing recommendation requests to the API endpoint.

### How It Works

1. **Image Upload**: The user uploads an image of a clothing item via a URL.
2. **Image Description**: The service generates a textual description of the image using an image description model.
3. **Embedding Creation**: The textual description is converted into a vector embedding using a pre-trained language model.
4. **Inventory Comparison**: The service compares the generated embedding with precomputed embeddings of clothing items in the inventory.
5. **Similarity Calculation**: Similarity scores are calculated between the user's image embedding and the inventory embeddings.
6. **Result Sorting and Filtering**: The service filters and sorts the inventory items based on their similarity scores, returning the top matches.

### Test Data

The app compares the user's images to its "inventory" of clothing. This is test data that you can find in ```clothing_inventory.py```. To make it searchable, you have to create embeddings. They're found in ```clothing_inventory_with_embeddings.json```. You can re-generate the embeddings by running ```python3 embeddings.py --generate```.

## Setup

### Python Backend Setup

1. **Environment Variables**:
   - Create a `.env` file with the OpenAI API key:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key
     ```

2. **Virtual Environment**:
   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```

3. **Install Dependencies**:
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

4. **Run the Application**:
   - The application can be run directly on Heroku. If running locally, use:
     ```bash
     python app.py
     ```

### Salesforce Setup

1. **Named Credentials and Unauthenticated External Credentials**:
   - Create named credentials and unauthenticated external credentials in Salesforce to securely access the backend service.

2. **External Service**:
   - Create an external service in Salesforce using the OpenAPI 3.0 specification provided in the repository.

3. **Custom Object**:
   - Create a custom object to model the data (e.g., `Clothing_Item__c`).

4. **Flow**:
   - Create a flow with an input URL and an output record list:
     - Call out the external service to process the image URL.
     - Transform the data to the custom object format.
     - Assign the custom object to output variables.

5. **Permission Set**:
   - Add a permission set for the agent user to access the external credentials:
     - Either an employee user using the assistive agent or an agent service user using the customer agent.

6. **Agent Actions**:
   - Add the flow to agent actions.
   - Assign the agent action to specific agents with topics and instructions.

## Copyright
Copyright Toni Melisma 2024
