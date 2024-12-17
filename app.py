import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from image_description import describe_image
from embeddings import create_embedding, compare_embeddings

app = Flask(__name__)

# Load environment variables for OpenAI API
load_dotenv()

# Path to inventory JSON file
INVENTORY_FILE = "clothing_inventory_with_embeddings.json"

# Load clothing inventory with precomputed embeddings
def load_inventory():
    print(f"Attempting to load inventory from: {INVENTORY_FILE}")
    print(f"Current working directory: {os.getcwd()}")
    
    try:
        with open(INVENTORY_FILE, "r") as f:
            inventory = json.load(f)
        print(f"Successfully loaded inventory. Number of items: {len(inventory)}")
        return inventory
    except FileNotFoundError:
        print(f"ERROR: Inventory file {INVENTORY_FILE} not found!")
        print("Possible reasons:")
        print("1. File does not exist in the current directory")
        print("2. Incorrect file path")
        print("3. Permissions issue")
        return []
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON in {INVENTORY_FILE}")
        return []
    except Exception as e:
        print(f"Unexpected error loading inventory: {e}")
        return []

clothing_inventory = load_inventory()

@app.route('/search', methods=['GET'])
def search_clothing():
    """
    Search endpoint that processes an image URL, generates a description, 
    creates embeddings, and compares against the clothing inventory.
    """
    # Extract image URL from query params
    image_url = request.args.get('url', '')
    
    print(f"Received search request for URL: {image_url}")
    
    if not image_url:
        print("ERROR: No URL provided in the request")
        return jsonify({"error": "No URL provided"}), 400
    
    # Step 1: Generate image description
    print("Attempting to describe image...")
    description = describe_image(image_url)
    
    if not description:
        print("ERROR: Failed to generate image description")
        return jsonify({"error": "Failed to generate description"}), 500
    
    print(f"Generated description: {description}")
    
    # Step 2: Create embedding for the description
    print("Creating embedding for description...")
    description_embedding = create_embedding(description)
    
    if description_embedding is None:
        print("ERROR: Failed to create embedding")
        return jsonify({"error": "Failed to create embedding"}), 500
    
    print(f"Description embedding created. Length: {len(description_embedding)}")
    
    # Step 3: Compare description embedding with precomputed embeddings
    results = []
    print(f"Comparing against {len(clothing_inventory)} inventory items")
    
    for item in clothing_inventory:
        item_embedding = item.get("embedding", [])
        if not item_embedding:
            print(f"Skipping item without embedding: {item.get('name', 'Unknown')}")
            continue  # Skip items without embeddings
        
        # Calculate similarity
        similarity = compare_embeddings(description_embedding, item_embedding)
        
        print(f"Item: {item.get('name', 'Unknown')}, Similarity: {similarity}")
        
        if similarity >= 0.5:
            item_with_similarity = item.copy()
            item_with_similarity["similarity"] = similarity
            results.append(item_with_similarity)
    
    # Step 4: Sort results by similarity in descending order
    sorted_results = sorted(results, key=lambda x: x["similarity"], reverse=True)
    
    print(f"Total matching results: {len(sorted_results)}")
    
    # Step 5: Return results
    return jsonify(sorted_results)

if __name__ == '__main__':
    print("Starting Flask application...")
    print(f"Inventory items loaded: {len(clothing_inventory)}")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))