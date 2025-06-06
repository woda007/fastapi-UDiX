from fastapi import FastAPI, HTTPException, Query, Request
import json
from typing import List, Dict, Any
import os

app = FastAPI()

@app.post("/drony")
async def get_instructions(request: Request):
    
    payload = await request.json()
    print("Webhook received:", payload)
