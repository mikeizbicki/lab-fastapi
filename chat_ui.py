#!/usr/bin/env python
import argparse
import gradio as gr
from openai import OpenAI

parser = argparse.ArgumentParser()
parser.add_argument("--url")
parser.add_argument("--apikey")
parser.add_argument("--model", default='llama-3.1-8b-instant')
parser.add_argument("--port", type=int, default=7860)
args = parser.parse_args()

client = OpenAI(base_url=args.url, api_key=args.apikey)

def chat(message, history):
    response = client.chat.completions.create(
        model=args.model,
        messages=[{"role": "user", "content": message}],
        stream=True
    )
    text = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            text += chunk.choices[0].delta.content
            yield text

gr.ChatInterface(chat).launch(server_port=args.port)
