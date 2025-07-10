#!/usr/bin/env python3
import weaviate
import weaviate.classes as wvc


# --- Main execution ---
def main():
    client = None  # Initialize client to None
    try:
        # Connect to your Weaviate instance
        client = weaviate.connect_to_local()
        print("Successfully connected to Weaviate.")

        # Define the collection name
        collection_name = "Document"

        # Create the collection if it doesn't exist
        if not client.collections.exists(collection_name):
            client.collections.create(
                name=collection_name,
                # Manually configure the vectorizer and options
                vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_huggingface(
                    model="nomic-ai/nomic-embed-text-v1.5",
                    wait_for_model=True,
                    use_gpu=False,  # Set to True if you have a GPU
                    use_cache=True,
                ),
            )
            print(f"Collection '{collection_name}' created.")

        # Get the collection
        docs = client.collections.get(collection_name)

        # Load your documents
        documents = [
            "The quick brown fox jumps over the lazy dog.",
            "The five boxing wizards jump quickly.",
            "How vexingly quick daft zebras jump!",
            "Sphinx of black quartz, judge my vow.",
        ]

        # Ingest the data into Weaviate
        with docs.batch.dynamic() as batch:
            for i, d in enumerate(documents):
                print(f"importing document: {i+1}")
                properties = {
                    "content": d,
                }
                batch.add_object(properties=properties)

        print("Data ingested.")

        # Perform a similarity search
        query = "What did the fox jump over?"
        response = docs.query.near_text(query=query, limit=2)

        # Print the results
        print("\nQuery: ", query)
        for o in response.objects:
            print("Results: ", o.properties)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Ensure the client connection is closed
        if client:
            client.close()
            print("Client connection closed.")


if __name__ == "__main__":
    main()
