import ollama, chromadb

client = chromadb.PersistentClient(path="./memory")
collection = client.get_or_create_collection("turtle_memory")
short_term: list[dict] = []
expiering_memory = []

def add_short_term(mem):
    short_term.append(mem)
    if len(short_term) > 15:
        expiering_memory.append(short_term.pop(0))

def add_long_term(mem:str, mem_id:str, pos:dict[str, int]):
    collection.add(
        documents=[json.dumps(mem)],
        ids=[mem_id],
        metadatas={"x_pos": pos.get("x", 0), "y_pos":pos.get("y", 0)}
    )

def recall(query, n=3):
    results = collection.query(query_texts=[query], n_results=n)
    return results["documents"][0]

def build_prompt(data, session):
    search_query = " ".join([
        data.
    ])


if __name__ == "__main__":
    client = chromadb.PersistentClient(path=".test_memory")
    collection = client.get_or_create_collection("turtle_memory")

    generate_msg()