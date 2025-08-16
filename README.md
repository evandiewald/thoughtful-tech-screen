# Thoughtful AI Tech Screen

Hello! Here is my Thoughtful AI Agent built using LangGraph. Due to the time constraints, I used a number of pre-built components from LangGraph/LangChain to bootstrap the project quickly. The agent has access to a tool that searches a small knowledge base using semantic embeddings to retrieve similar queries.

There are some basic features like token streaming and in-memory checkpointing to store in-thread memory, which will be lost when you refresh the page. The bot should not answer questions for which it does not have a relevant answer.

I've (temporarily) got a running version of the app on Replit, but I'm not sure how long it'll stay up:

https://replit.com/join/tjtvlfaryg-evandiewald

To run the app:

1. This project uses [`uv`](https://github.com/astral-sh/uv) to manage dependencies. Use the appropriate [installation command](https://github.com/astral-sh/uv) for your platform.

2. You will need API Keys for [Anthropic](https://docs.anthropic.com/en/docs/get-started) and [Cohere](https://cohere.com) (for the embeddings - you can use a rate-limited trial key). 

3. `cp .env.template .env` and paste your API keys in the appropriate fields.

4. `uv sync` to install dependencies (if you don't already have Python 3.11+, you can install with `uv python install 3.11`)

5. `uv run streamlit run main.py` - your app will be available at [`http://localhost:8501`](http://localhost:8501) by default!