# APIs and LLM Web Interfaces

In this lab you will create a web interface for the LLM-based class project.
Part 1 of this lab walks through the steps for using and creating APIs and web interfaces.
In Part 2, you will add a web interface to a partner's LLM project.

## Part 1: Webservers and APIs

You will need to clone this repo, cd into the clone, and install all dependencies in the `requirements.txt` file.

### Using APIs

An API (Application Programmer Interface) is a just a webpage that returns JSON instead of HTML.
We'll walk through a quick example of using reddit's API,
then we will see how to the groq/openai API works.

The subreddit /r/programmerhumor has a lot of memes that I've shown in class.
The url is: <https://www.reddit.com/r/ProgrammerHumor>
Click on the url and observe that the subreddit is full of memes.

Here is one of my favorites:

<img width=300px src=img/programmerhumor.jpg />

The API *endpoint* is the url the returns the JSON.
In the reddit API, to get the endpoint for a subreddit, we just append `.json` to the end of the url.
The API endpoint for /r/programmerhumor is <https://www.reddit.com/r/ProgrammerHumor.json>.
Click this link.
You should see a bunch of JSON like

<img width=600px src=img/json2.png />

or

<img width=600px src=img/json1.png />

The details of what this JSON means is not important.
The point is just that we can get all the information from reddit we might want without scraping.

> **NOTE:**
> [Ebay provides a free API](https://developer.ebay.com/api-docs/static/ebay-rest-landing.html) that we could have used to "scrape" its search results.
> It requires creating an account to use,
> but by using the ebay API we replace all the work you did with a single call to `requests.get` using the ebay API endpoint.
>
> <img width=300px src=img/scrape.png />

`curl` is the standard shell tool for working with APIs:
all it does is download a webpage and print the contents to the screen.
We could "scrape" reddit by using the API endpoint with curl like
```
$ curl https://www.reddit.com/r/ProgrammerHumor.json
```
You should see a bunch of JSON printed in the terminal.

As another example:
The website <https://cheat.sh/python> contains a simple python cheatsheet.
You can view it firefox by clicking the link or in the terminal with the command
```
$ curl https://cheat.sh/python
```

Many programmers use curl to access LLM APIs.
The [Groq QuickStart Guide](https://console.groq.com/docs/quickstart) has a section on using the API from the shell with curl.
It looks something like

<img src=img/curl.png />

The `curl` command contains a lot more inside of it than just the URL:
1. "headers" that handle the authentication (i.e. logging in with the `$GROQ_API_KEY`), and
1. "messages" that contain the messages being passed to the model.
Visit the quickstart guide and copy/paste the command above into your shell.
You will see the raw output of the groq API,
which is a large json object.
There are many fields in this object,
and you don't need to decipher them all,
but you should be able to find the text that the model responds with.

> **HINT:**
> Recall that the `|` operator can be used to pass the output of one program to the input to another program.
> Python has a built-in JSON formatter that can make reading JSON objects much easier, and we can pass the output of `curl` to this formatter to read it nicer.
> The incantation is:
> ```
> $ curl <insert_curl_params_here> | python3 -m json.tool
> ```
> You should see output that starts with something like
> ```
> {
>    "id": "chatcmpl-c76ad728-221c-4d25-aa71-78272358c9b0",
>    "object": "chat.completion",
>    "created": 1777047642,
>    "model": "llama-3.3-70b-versatile",
>    "choices": [
>        {
>            "index": 0,
>            "message": {
>                "role": "assistant",
>                "content": "Fast language models are crucial for various applications a
> ```
> Notice that the structure of this JSON object closely matches the structure of the python `response` variable from the command
> ```
> response = self.client.chat.completions.create( ... )
> text = response.choices[0].message.content
> ```

### Launching a custom chat web interface

The url that you curled above should look like
```
https://api.groq.com/openai/v1/chat/completions
```
Notice the `openai` in the url;
this is groq's implmementation of [the OpenAI-compatible LLM API](https://bentoml.com/llm/model-interaction/openai-compatible-api).
All modern LLM providers (e.g. OpenAI, Anthropic, openrouter.ai, etc.) implement this API,
and lots of tooling has been built around this API.
This tooling is generic and can work with any LLM provider.

For example, many people have built custom web-interfaces for AI chatbots that are quite a bit more powerful than the standard <https://chatgpt.com>.
Famous python-based examples include [oobabooga](https://github.com/oobabooga/textgen) and [open-webui](https://github.com/open-webui/open-webui).
These interfaces can do things like:
1. manually editing the context (i.e. `self.messages` in our `Chat` class),
1. adding/removing tools from the web interface,
1. setting optional parameters that change the behavior of the LLM (we talked briefly about `temperature`, but there's dozens of other parameters that affect output), and
1. sending queries to multiple models and automatically using only the best response.

In this lab, we're not going to explore these powerful features,
and instead use just a simple interface provided by [gradio](https://www.gradio.app/guides/quickstart).

The file `gradio_server.py` contains a web server that can be used to connect to any OpenAI compatible endpoint.
The following command will create a web interface for the groq endpoint you can use:
```
$ python3 gradio_server.py --url=https://api.groq.com/openai/v1 --apikey=$GROQ_API_KEY
* Running on local URL:  http://127.0.0.1:7860
* To create a public link, set `share=True` in `launch()`.
```
After running the command, visit the url displayed in your terminal (probably <http://127.0.0.1:7860>) to view the chatbot.
Have a brief conversation with the chatbot,
and verify that everything works.

> **NOTE:**
> The `:7860` in the url above defines a *port* that the webserver will run on.
> You will need to have multiple web servers running at different points,
> and the port allows us to specify which one of these web servers we will connect to.
> There are `2**16 = 65536` valid ports,
> and so a single computer can run up to 65536 servers at a time.

### Creating your own OpenAI-compatible Endpoint

If we create our own OpenAI compatible endpoint,
then we get all of this other tooling available to us "for free".
Programmers love using other people's code,
and we've been doing it well before ChatGPT came along.

<img width=300px src=img/steal.png />

The file `endpoint.py` contains a simple example of an OpenAI compatible endpoing written in FastAPI.
Run it with the command
```
$ python3 endpoint.py
INFO:     Started server process [180865]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
You should inspect the file and observe that it defines four "routes":
- `/`
- `/spanish`
- `/latin`
- `/v1/chat/completions`

Each of these routes is a path that we can connect to with curl (or firefox/chrome).
```
$ curl http://127.0.0.1:8000/
hello world
$ curl http://127.0.0.1:8000/spanish
hola mundo
$ curl http://127.0.0.1:8000/latin
salve munde
```
Notice that because I used curl in the examples above,
all I had to do to show you how to use the routes was copy/paste a terminal session.
Programmers *love* terminals because they enable copy/paste,
and you don't need long-winded explanations about clicking buttons in menus.

You can contact the API endpoint with a command like:
```
$ curl -X POST http://127.0.0.1:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"messages":[{"role":"user","content":"hello"}]}'
{"id":"chatcmpl-123","object":"chat.completion","created":0,"model":"unknown","choices":[{"index":0,"message":{"role":"assistant","content":"this is response number 1"},"finish_reason":"stop"}],"usage":{"prompt_tokens":0,"completion_tokens":0,"total_tokens":0}}
```

Now that we have our own API created, we can easily create a web interface to chat with our program:
We just point the `gradio_server.py` file we used before to our new endpoint.

You will need to have to terminals running in order to do this.
First, ensure that the `endpoint.py` program is running in the first terminal.
Then, run the `gradio_server.py` program with the url of your `endpoint.py` server:
```
$ python3 gradio_server.py --url=http://127.0.0.1:8000/v1
* Running on local URL:  http://127.0.0.1:7860
* To create a public link, set `share=True` in `launch()`.
```
Visit the url for the `gradio_server.py`, and you can have a conversation with the dummy endpoint.

> **NOTE:**
> This endpoint is a *mock*:
> It does not actually use LLMs and just returns fake results that don't care about the user input.
> In this case that is okay because the thing we are testing is the web server conntection.
> A mock LLM was not acceptable for your homework because the thing you were testing was the LLM itself.

## Part II: Web interface for project 3/4

Now we will add a web interface to not your own project, but someone else's in the class.

1. Fork your partner's project then clone it to your laptop.
1. Copy the `gradio_server.py` and `endpoint.py` files into the clone.
1. Modify the `endpoint.py` file so that it uses your partner's `Chat` class and not the mock.

    > **HINT:**
    > The `endpoint.py` is structured to make this easy.
    > All you should have to do is change the `import` line to import their `Chat` instead of the `Chat` from `mock_chat.py`.

1. Verify that you can have a conversation with the LLM,
    and verify that questions like "what does the README say this project is about?" correctly use the tool calls to answer the question.
1. Take a screenshot of your conversation that verifies the bot is working.
1. Add / commit your changes to git; push to github; and submit a pull request to your partner's project.  Your partner must accept this pull request.
1. Submit to canvas:
    1. the screenshot
    1. a link to the accepted pull request
