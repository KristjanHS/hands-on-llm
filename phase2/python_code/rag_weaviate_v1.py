#!/usr/bin/env python3
import weaviate
import os

# Connect to your Weaviate instance
client = weaviate.Client("http://localhost:8080")

# Define the schema for your data
class_obj = {
    "class": "Document",
    "vectorizer": "text2vec-nomic",
    "moduleConfig": {
        "text2vec-nomic": {
            "model": "nomic-embed-text-v1.5",
        }
    },
}

# Create the schema in Weaviate
if not client.schema.exists("Document"):
    client.schema.create_class(class_obj)
    print("'Document' class created.")

# Load your documents
# For this example, we'll use a simple list of strings.
# In a real application, you would load your documents from files.
documents = [
    "The quick brown fox jumps over the lazy dog.",
    "The five boxing wizards jump quickly.",
    "How vexingly quick daft zebras jump!",
    "Sphinx of black quartz, judge my vow.",
]

# Ingest the data into Weaviate
with client.batch as batch:
    for i, d in enumerate(documents):
        print(f"importing document: {i+1}")
        properties = {
            "content": d,
        }
        batch.add_data_object(properties, "Document")

print("Data ingested.")

# Perform a similarity search
query = "What did the fox jump over?"
result = client.query.get("Document", ["content"]).with_near_text({"concepts": [query]}).with_limit(2).do()

# Print the results
print("\nQuery: ", query)
print("Results: ", result)
