'''
A basic openai-compatible endpoint for servering model responses.

The existing "model" just counts the number of times that the user has input a message.
'''

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def english():
    return 'hello world\n'

@app.get("/spanish", response_class=HTMLResponse)
async def english():
    return 'hola mundo\n'

@app.get("/latin", response_class=HTMLResponse)
async def english():
    return 'salve munde\n'

@app.post("/v1/chat/completions")
async def chat_completions(request: dict) -> dict:
    messages = request.get("messages", [])
    user_message_count = sum(1 for msg in messages if msg.get("role") == "user")
    
    response_content = f"this is response number {user_message_count}"
    
    return {
        "id": "chatcmpl-123",
        "object": "chat.completion",
        "created": 0,
        "model": request.get("model", "unknown"),
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_content
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
