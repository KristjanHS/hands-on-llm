#!/usr/bin/env python3
import os
from pypdf import PdfReader
import weaviate

# NEW weaviate v4 way:
client = weaviate.connect_to_local()


def load_pdf_documents(directory_path):
    documents = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(directory_path, filename)
            reader = PdfReader(filepath)
            document_text = ""
            for page in reader.pages:
                document_text += page.extract_text() + "\n"
            documents.append({"content": document_text, "source": filename})
    return documents


def prepare_documents_for_enumeration(documents):
    enumerated_documents = []
    for doc in documents:
        # Here you can split documents into smaller chunks if needed
        # For now, we'll treat each document as a single chunk
        enumerated_documents.append(doc)
    return enumerated_documents


def ingest_documents_into_weaviate(client, documents, class_name="Document"):
    with client.batch as batch:
        for i, doc in enumerate(documents):
            print(f"Importing document: {i+1}")
            properties = {
                "content": doc["content"],
                "source": doc.get("source", "unknown"),
            }
            batch.add_data_object(properties, class_name)
    print("Data ingestion complete.")


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

# Load PDF documents from the 'data' directory
pdf_documents = load_pdf_documents("./data")

# Prepare documents for enumeration (e.g., chunking)
prepared_documents = prepare_documents_for_enumeration(pdf_documents)

# Ingest the prepared data into Weaviate
ingest_documents_into_weaviate(client, prepared_documents)

# Perform a similarity search
query = "What did the fox jump over?"
result = client.query.get("Document", ["content"]).with_near_text({"concepts": [query]}).with_limit(2).do()

# Print the results
print("\nQuery: ", query)
print("Results: ", result)
