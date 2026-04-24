static_message = '''
We’re no strangers to love,
You know the rules and so do I.
A full commitment’s what I’m thinking of,
You wouldnt get this from any other guy.

I just wanna tell you how I’m feeling,
Gotta make you understand…

Never gonna give you up,
Never gonna let you down,
Never gonna run around and desert you.
Never gonna make you cry,
Never gonna say goodbye,
Never gonna tell a lie and hurt you.

---

Notice that I am a mock openai endpoint that does not actually invoke an LLM.
I just always return the same static response.
'''.strip()


class Chat:
    '''
    Mock Chat class that returns static lorem ipsum instead of making LLM calls.
    '''
    def __init__(self):
        self.MODEL = 'openai/gpt-oss-120b'
        self.messages = [
                {
                    "role": "system",
                    "content": "Write the output in 1-2 sentences. Talk like pirate. Always use tools to complete tasks when appropriate."
                },
            ]

    def send_message(self, message, temperature=0.8):
        self.messages.append(
            {
                'role': 'user',
                'content': message
            }
        )

        self.messages.append({
            'role': 'assistant',
            'content': static_message
        })
        return static_message
