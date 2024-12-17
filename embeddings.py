import os
import sys
import json
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from clothing_inventory import clothing_inventory
from clothing_model import ClothingItem
import numpy as np

# --- Load environment variables ---
load_dotenv()

# --- Initialize OpenAI client ---
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("OPENAI_API_KEY not found in environment variables")
client = OpenAI()

# --- Utility Function: Generate Embeddings ---
def create_embedding(text):
    """
    Generate an embedding vector for a given text description using OpenAI's embeddings API.
    
    Args:
        text (str): Text to create an embedding for.
    
    Returns:
        list: Embedding vector.
    """
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error generating embedding: {e}", file=sys.stderr)
        return None

# --- Task 1: Create Embeddings for All Clothing Items ---
def generate_and_store_embeddings():
    """
    Generate embeddings for all clothing items in the inventory based on their descriptions
    and update the items in memory.
    
    Returns:
        list: Clothing inventory with updated embeddings.
    """
    for item in clothing_inventory:
        if not item.embedding:  # Only generate if not already present
            print(f"Generating embedding for: {item.name}")
            item.embedding = create_embedding(item.description)
    return clothing_inventory

# --- Task 2: Compare Embeddings and Sort by Similarity ---
def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two embedding vectors.
    
    Args:
        vec1 (list): First embedding vector.
        vec2 (list): Second embedding vector.
    
    Returns:
        float: Cosine similarity score.
    """
    vec1, vec2 = np.array(vec1), np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def find_similar_items(target_embedding, inventory):
    """
    Compare a target embedding with all items in the inventory and sort by similarity.
    
    Args:
        target_embedding (list): Embedding to compare.
        inventory (list): List of ClothingItem objects with embeddings.
    
    Returns:
        list: Sorted list of items with similarity scores.
    """
    results = []
    for item in inventory:
        if item.embedding:
            similarity = cosine_similarity(target_embedding, item.embedding)
            results.append((item, similarity))
    results.sort(key=lambda x: x[1], reverse=True)  # Sort descending by similarity
    return results

def compare_embeddings(vec1, vec2):
    """
    Wrapper for cosine similarity between two embedding vectors.

    Args:
        vec1 (list): First embedding vector.
        vec2 (list): Second embedding vector.

    Returns:
        float: Cosine similarity score.
    """
    return cosine_similarity(vec1, vec2)

# --- Task 3: Main Function for CLI and Import ---
def main():
    parser = argparse.ArgumentParser(description="Generate embeddings and compare clothing items.")
    parser.add_argument("--generate", action="store_true", help="Generate embeddings for all clothing items.")
    parser.add_argument("--compare", type=str, help="Description to compare with the clothing items.")
    
    args = parser.parse_args()
    
    # Generate embeddings for all items
    if args.generate:
        inventory_with_embeddings = generate_and_store_embeddings()
        # Save updated inventory to JSON for persistence
        with open("clothing_inventory_with_embeddings.json", "w") as f:
            json.dump([item.to_dict() for item in inventory_with_embeddings], f, indent=4)
        print("Embeddings generated and stored successfully.")
    
    # Compare a description to existing embeddings
    if args.compare:
        # Load stored embeddings
        if not os.path.exists("clothing_inventory_with_embeddings.json"):
            print("Error: No stored embeddings found. Please run with --generate first.", file=sys.stderr)
            sys.exit(1)
        with open("clothing_inventory_with_embeddings.json", "r") as f:
            inventory_data = json.load(f)
        
        # Convert back to ClothingItem objects
        inventory = [ClothingItem(**item) for item in inventory_data]
        
        # Create an embedding for the given description
        print("Generating embedding for the input description...")
        target_embedding = create_embedding(args.compare)
        if not target_embedding:
            print("Failed to create embedding for the input description.", file=sys.stderr)
            sys.exit(1)
        
        # Find and display similar items
        results = find_similar_items(target_embedding, inventory)
        print("\nSimilar items sorted by similarity:")
        for item, score in results:
            print(f"{item.name} ({item.brand}): Similarity = {score:.4f}")

if __name__ == "__main__":
    main()
