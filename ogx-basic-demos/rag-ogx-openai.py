from openai import OpenAI

model = "ollama/llama3.2:3b"
relevant_threshold = 0.002

client = OpenAI(base_url="http://localhost:8321/v1", api_key="fake")

vector_store = None


def build_rag():
    global vector_store

    files = [
        "kubernetes_doc.txt",
        "ogx-ollama_doc.txt",
        "my-resume_doc.txt",
        "event-agenda-doc.txt",
        "training-courses-doc.txt"
    ]

    file_ids = []

    for filename in files:
        uploaded_file = client.files.create(
            file=open(filename, "rb"),
            purpose="assistants",
        )
        file_ids.append(uploaded_file.id)
        print(f"Uploaded {filename}: {uploaded_file.id}")

    vector_store = client.vector_stores.create(
        name="my-docs",
        file_ids=file_ids,
    )

    print(f"Vector Store ID: {vector_store.id}")
    print("RAG setup completed!")


def get_top_score(output_list):
    top_score = 0.0

    for item in output_list:
        if getattr(item, "type", None) == "file_search_call":
            for r in getattr(item, "results", []):
                score = getattr(r, "score", 0.0) or 0.0
                top_score = max(top_score, score)

    return top_score


def not_relevant(top_score):
    if top_score < relevant_threshold:
        print("Didn't find any relevant answer...")
        return True
    else:
        print("Found relevant answer...")
        return False


def normal_llm(query: str):
    return client.responses.create(
        model=model,
        temperature=0.0,
        input=query
    )


def ask_rag(query: str, full_response: bool = False):
    response = client.responses.create(
        model=model,
        temperature=0.0,
        input=query,
        tools=[
            {
                "type": "file_search",
                "vector_store_ids": [vector_store.id],
                "max_num_results": 3,
            }
        ],
    )

    top_score = get_top_score(response.output)
    print("top_score=", top_score)

    if not_relevant(top_score):
        response = normal_llm(query)

    return response if full_response else response.output_text


if __name__ == "__main__":
    print("connecting to ...", getattr(client, "base_url", "unknown"))
    build_rag()

    print("\nRAG ready! \nType 'exit' to quit.\n")

    while True:
        query = input("Ask RAG: ")

        if query.lower() in ["exit", "quit"]:
            break

        answer = ask_rag(query)
        print("\n", answer, "\n")
    
    if vector_store is not None:
        client.vector_stores.delete(vector_store.id)
        print(f"Vector Store ID deleted: {vector_store.id}")
        
    print("\nGood bye, Thanks for trying me...\n")