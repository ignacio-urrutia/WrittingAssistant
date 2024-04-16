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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# with open(os.path.join(BASE_DIR, "resources", "sample_text.md")) as f:
#     sample_text = f.read()

with open(os.path.join(BASE_DIR, "resources", "system_prompt.txt")) as f:
    system_prompt = f.read()

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("system", "The sample text is the following. You should use that style to write a new text based on the user input. Sample text: {sample_text}"),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

def parse_chat_history(chat_history):
    history = ChatMessageHistory()
    for message in chat_history:
        if message["sender"] == "user":
            history.add_user_message(message["message"])
        elif message["sender"] == "ai":
            history.add_ai_message(message["message"])
    return history.messages

def invoke_agent_with_chat_history(session_id: str, user_input: str):
    current_article = Article(session_id)
    sample_text = current_article.get_sample_text()

    @tool
    def get_all_paragraphs() -> str:
        """Returns a json object with all paragraphs and their indexes"""
        return current_article.get_all_paragraphs()

    @tool
    def add_paragraph(new_paragraph: str, index:int) -> str:
        """Adds a paragraph to the article at the specified index. If index is -1, the paragraph is added at the end"""
        current_article.add_paragraph(new_paragraph, index)
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
    # message_history = ChatMessageHistory()
    message_history = current_article.get_chat_history()
    parsed_chat_history = parse_chat_history(message_history)
    
    result = agent_executor.invoke(
        {"input": user_input, "chat_history": parsed_chat_history, "sample_text": sample_text},
    )
    response = result.get("output", "No response from the agent.")
    message_history.append({"sender": "user", "message": user_input})
    message_history.append({"sender": "ai", "message": response})
    
    current_article.set_chat_history(message_history)

    return response, current_article.get_article()

# Example usage
# input = """I want to include that Suno AI was developed by Anthropic, a group of ex-OpenAI researchers and the same ones who developed Claude 3, a powerful model that copete directly with GPT-4 that i will talk about later in this article. Put that where i write about Suno AI.
# """
# agent_with_chat_history.invoke(
#     {"input": input},
#     config={"configurable": {"session_id": "<foo>"}},
# )

