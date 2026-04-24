static_message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."


class Chat:
    '''
    Mock Chat class that returns static lorem ipsum instead of making LLM calls.

    >>> chat = Chat()
    >>> chat.send_message('my name is bob')
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    >>> len(chat.messages)
    3
    >>> chat.messages[1]['role']
    'user'
    >>> chat.messages[2]['role']
    'assistant'
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
