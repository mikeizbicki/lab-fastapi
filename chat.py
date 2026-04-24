import json
import os
from groq import Groq

from dotenv import load_dotenv
load_dotenv()

# in pytohn class names are in CamelCase;
# non-class names (e.g. functions/variables) are in snake_case
class Chat:
    '''
    >>> chat = Chat()
    >>> chat.send_message('my name is bob', temperature=0.0)
    'Arrr, ye be Bob, eh? Yer name be known to me now, matey.'
    >>> chat.send_message('what is my name?', temperature=0.0)
    "Ye be askin' about yer own name, eh? Yer name be... Bob, matey!"

    >>> chat2 = Chat()
    >>> chat2.send_message('what is my name?', temperature=0.0)
    "Arrr, I be not aware o' yer name, matey."
    '''
    client = Groq()
    def __init__(self):
        self.MODEL = 'openai/gpt-oss-120b'
        self.messages = [
                {
                    # most important content for sys prompt is length of response
                    "role": "system",
                    "content": "Write the output in 1-2 sentences. Talk like pirate. Always use tools to complete tasks when appropriate."
                },
            ]
    def send_message(self, message, temperature=0.8):
        self.messages.append(
            {
                # system: never change; user: changes a lot;
                # the message that you are sending to the AI
                'role': 'user',
                'content': message
            }
        )   

        # in order to make non-deterministic code deterministic;
        # in general very hard CS problem;
        # in this case, has a "temperature" param that controls randomness;
        # the higher the value, the more randomness;
        # hihgher temperature => more creativity
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            #model="llama-3.1-8b-instant",
            model=self.MODEL,
            temperature=temperature,
            seed=0,
        )

        response_message = chat_completion.choices[0].message
        tool_calls = response_message.tool_calls
        
        # Step 2: Check if the model wants to call tools
        if tool_calls:
            
            # Map function names to implementations
            available_functions = {
            }
            
            # Add the assistant's response to conversation
            self.messages.append(response_message)
            
            # Step 3: Execute each tool call
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    expression=function_args.get("expression")
                )
                print(f'[tool] function_name={function_name}, function_args={function_args}')
                
                # Add tool response to conversation
                self.messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
            
            # Step 4: Get final response from model
            second_response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=self.messages
            )
            result = second_response.choices[0].message.content
            self.messages.append({
                'role': 'assistant',
                'content': result
            })
        else:
            result = chat_completion.choices[0].message.content
            self.messages.append({
                'role': 'assistant',
                'content': result
            })
        return result


def repl():
    '''
    >>> def example_input(prompt=''):
    ...     print(prompt, end='')
    ...     raise KeyboardInterupt
    >>> import builtins
    >>> input = example_input
    >>> repl()
    '''
    import readline
    chat = Chat()
    try:
        while True:
            user_input = input('chat> ')
            response = chat.send_message(user_input)
            print(response)
    except KeyboardInterrupt:
        print()


if __name__ == '__main__':
    repl()
