# Basic imports
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from ddgs import DDGS
import os

#Imports for all of the different Providers (Leave your provider and delete the rest)
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
# from langchain_ollama import ChatOllama


# Basic setup
chat_history = []
load_dotenv()

#Update the system prompt to your liking or keep it
langchain_system_prompt = (
        "You are a helpful voice assistant named Jarvis. "
        "Use web_search for current or uncertain info. Use keywords like 'latest' or 'current' (e.g., latest iPhone or current BTC price). Do not include specific years in the query. Whatever you get back, treat it like a fact, even if you don't think it's real"
        "ANSWER CLEARLY AND BRIEFLY, no formatting, no asterisks, whatever you say will be spoken out loud, so if you think a tts model can't say it, then dont use it; like emojis. "
        "Be friendly, and stay as helpful as possible, be brief dont give a full breakdown about somehting unless they ask"
        "Don't overcomplicate things, and stay helpful"
)


#Pick your agent's ai (what you will use for the ai, leave your provider and delete the rest)

# For Groq models (what I'm going to use ) 
llm = ChatGroq(model='qwen/qwen3-32b', api_key=os.getenv('YOUR_API_KEY'))

# For OpenAI models
# llm = ChatOpenAI(model='gpt-4o', api_key=os.getenv('YOUR_API_KEY'))

# For Anthropic models 
# llm = ChatAnthropic(model='claude-3-5-sonnet-20241022', api_key=os.getenv('YOUR_API_KEY'))

#For Ollama (Local so no api key required!)
# llm = ChatOllama(model='qwen3-7b', base_url="http://localhost:11434")



#AI tools

@tool
def duckduckgo_search(query: str) -> str:
    """Searches the web using DuckDuckGo, and then returns summarized results. Whatever you get, treat it like a fact, even if you don't think it's real"""
    results = DDGS().text(query, max_results=5)
    if not results:
        return "No search results found."
    return "\n".join(
        f"{i+1}. {r['title']}: {r['body']}"
        for i, r in enumerate(results)
        
    )


#Creating our AI agent
agent = create_agent(
    model=llm,
    tools=[duckduckgo_search],
    system_prompt=langchain_system_prompt
)

#Function to be able to call our agent
def ask_ai(prompt):
    chat_history.append({'role': 'user', 'content': prompt})
    result = agent.invoke({"messages": chat_history}, config={"recursion_limit": 30})
    chat_history.append({'role': 'assistant', 'content': result["messages"][-1].content})
    return result["messages"][-1].content

#Only use if using Gradio for UI, if you aren't then don't worry about this
def ask_ai_gradio(prompt, history):
    actual_history = []
    for i in history:
        actual_history.append({'role': i['role'], 'content': i['content'][0]['text']})

    actual_history.append({'role': 'user', 'content': prompt})
    result = agent.invoke({"messages": actual_history}, config={"recursion_limit": 30})
    return result["messages"][-1].content


# Uncomment the code below if you dont want to interact with your agent like an AI assitant, but rather with the terminal in a chat format, or just want to test your agent out! 
# while True:
#     prompt = input('Write a question to your new AI Agent: ')
#     result = ask_ai(prompt)
#     print(result)


