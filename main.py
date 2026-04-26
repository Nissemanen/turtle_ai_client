import asyncio
import server
import json
import llm


messages = []

def on_request(data, session, raw_message):
    global messages

    print(raw_message)

    return input();

    print("messages: "+str(messages))

    actions, response, messages = llm.get_action(data, session, messages)
    print("\n\n--------------------1---------------------\n")
    print(response.message.thinking)
    print("\n\n--------------------2---------------------\n")
    print(response.message.content)
    print("\n\n--------------------3---------------------\n")
    print(actions)



    try:
        return actions if actions else "";

    except Exception as e:
        e.with_traceback()
        return "";


asyncio.run(server.start(on_request))