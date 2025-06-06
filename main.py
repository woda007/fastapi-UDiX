from fastapi import FastAPI, HTTPException, Query, Request
import json
from openai import OpenAI
from typing import List, Dict, Any
import os

app = FastAPI()

def get_answer_from_openai(question, tools=None, model="gpt-4.1-2025-04-14"):
    
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    if tools != None:
        response = client.responses.create(
            model=model,
            tools=tools,
            input=question,
            tool_choice="auto"
            )
    else:
        response = client.responses.create(
            model=model,
            input=question,
        )


@app.post("/drony")
async def get_instructions(request: Request):
    
    payload = await request.json()
    print("Webhook received:", payload)

    prompt =  f"""Given the following json with a map. And the following human captured move intent, 1) prepare a move plan, 2) using the move plan find what's on the target field on the map, 3) provide the final answer in the format <answer>{{'description':'whats on the map'}}</answer>Your journey always starts in position (0,0), where "znacznik" is located.
    <map json>
    {{
      "map": [
        [
          {{"wiersz": 0, "kolumna": 0, "typ": "znacznik"}},
          {{"wiersz": 0, "kolumna": 1, "typ": "puste"}},
          {{"wiersz": 0, "kolumna": 2, "typ": "drzewo"}},
          {{"wiersz": 0, "kolumna": 3, "typ": "dom"}}
        ],
        [
          {{"wiersz": 1, "kolumna": 0, "typ": "puste"}},
          {{"wiersz": 1, "kolumna": 1, "typ": "wiatrak"}},
          {{"wiersz": 1, "kolumna": 2, "typ": "puste"}},
          {{"wiersz": 1, "kolumna": 3, "typ": "puste"}}
        ],
        [
          {{"wiersz": 2, "kolumna": 0, "typ": "puste"}},
          {{"wiersz": 2, "kolumna": 1, "typ": "puste"}},
          {{"wiersz": 2, "kolumna": 2, "typ": "skały"}},
          {{"wiersz": 2, "kolumna": 3, "typ": "drzewa"}}
        ],
        [
          {{"wiersz": 3, "kolumna": 0, "typ": "góry"}},
          {{"wiersz": 3, "kolumna": 1, "typ": "góry"}},
          {{"wiersz": 3, "kolumna": 2, "typ": "samochód"}},
          {{"wiersz": 3, "kolumna": 3, "typ": "jaskinia"}}
        ]
      ]
    }}
    </map json>
    <move intent>
    {payload["instructions"]}
    </move intent>
    """
    
    response = get_answer_from_openai(prompt)

    return response[response.find("<answer>") + len("<answer>") : response.find("</answer>")]

    
    
