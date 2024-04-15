from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from article import Article

load_dotenv()

with open("sample_text.md") as f:
    sample_text = f.read()

with open("system_prompt.txt") as f:
    system_prompt = f.read()

from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("system", "The sample text is the following. You should use that style to write a new text based on the user input. Sample text: " + sample_text),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

current_article = Article("article.txt")

@tool
def get_all_paragraphs() -> str:
    """Returns a json object with all paragraphs and their indexes"""
    return current_article.get_all_paragraphs()

@tool
def add_paragraph(new_paragraph: str) -> str:
    """Adds a paragraph to the article"""
    current_article.add_paragraph(new_paragraph)
    return "Paragraph added"

@tool
def modify_paragraph(index: int, modified_paragraph: str) -> str:
    """Modifies a paragraph in the article"""
    current_article.modify_paragraph(index, modified_paragraph)
    return "Paragraph modified"

@tool
def remove_paragraph(index: int) -> str:
    """Removes a paragraph from the article"""
    current_article.remove_paragraph(index)
    return "Paragraph removed"

tools = [get_all_paragraphs, add_paragraph, modify_paragraph, remove_paragraph]
llm = ChatOpenAI(model="gpt-4-turbo")
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
message_history = ChatMessageHistory()
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    # This is needed because in most real world scenarios, a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# Example usage
input = """I want to include that Suno AI was developed by Anthropic, a group of ex-OpenAI researchers and the same ones who developed Claude 3, a powerful model that copete directly with GPT-4 that i will talk about later in this article. Put that where i write about Suno AI.
"""
agent_with_chat_history.invoke(
    {"input": input},
    config={"configurable": {"session_id": "<foo>"}},
)

