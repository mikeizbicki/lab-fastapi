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
    completion = client.chat.completions.create(
        model=args.model,
        messages=[{"role": "user", "content": message}]
    )
    return completion.choices[0].message.content

gr.ChatInterface(chat).launch(server_port=args.port)
