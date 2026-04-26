import ollama, chromadb, json

client = chromadb.PersistentClient(path="./data/memory")
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

def submit_action(thought: str, action: int) -> str:
    """Subbmit your actions to be done

    Args:
      thought: your current internal though (in character)
      action: an integer from 0 to 4, 0 = idle, 1 = move_forwards, 2 = move_backwards, 3 = turn_right, 4 = turn_left.
    
    Returns:
      the structured JSON for yout action
    """
    action = "move_forwards" if action == 1 else "move_backwards" if action == 2 else "turn_right" if action == 3 else "turn_left" if action == 4 else "idle"

    return json.dumps({"thought": thought, "action": action})

def get_action(data, session, messages):
    facing = data.get('facing', [0, 0])
    facing_text = 'You are currently facing east, or in other words towards the positive X' if facing[0] == 1 else 'You are currently facing west, or in other words towards the negative X' if facing[0] == -1 else 'You are currently facing south, or in other words towards the positive Z' if facing[1] == 1 else 'You are currently facing north, or in other words towards the negative Z'

    if not messages:
        messages = [{"role":"system", "content":f"""
You are a robot living inside a Minecraft world. You are not a helpfull assistant, you are a robot that can move arround in the world and interact with blocks and players.

## Surroundings
Your surroundings will be formated as a list of JSON objects, their structure will be:
[{'{'}"y": int (how far away the block is from you in the y axis), "x": int (how far away the block is from you in the x axis), "name": str (what type of block it is, including its namespace), "z": int (how far away the block is from you in the z axis){'}'}]
Your curent surroundings are:
{data.get('scan')}

all blocks you can see in the list are 1 block away from your position (including diagonals).
{facing_text}

---

to do anything you have gotten a tool "submit_action".
currently, you can not interract with any blocks. You can only move arround and try searching for things.
    """.strip()}]
    else:
        messages.append({"role":"system", "content":f"## Surroundings:\n{data.get('scan')}\n\n{facing_text}"})

    response = ollama.chat(model="qwen3.5:latest", messages=messages, think=True, tools=[submit_action])

    messages.append(response.message)

    result = None

    if response.message.tool_calls:
        call = response.message.tool_calls[0]
        result = submit_action(**call.function.arguments)

        messages.append({"role": "tool", "tool_name": call.function.name, "content":result})

    while len(messages) > 10:
        messages.pop(1)

    return result, response, messages

def parse_llama_message(message:str):
    return message.split("\n\n")[1]
