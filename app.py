from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from writerAgent import Article, agent_with_chat_history  # Ensure your agent and Article class are imported here

app = Flask(__name__)

current_article = Article("article.txt")

@app.route("/")
def index():
    return render_template("index.html", content=current_article.__str__())

@app.route("/update_article", methods=["POST"])
def update_article():
    data = request.get_json()  # Use get_json to parse the JSON request body
    markdownContent = data.get('article')  # Ensure the key here matches the key sent from frontend
    if markdownContent is None:
        return "No content provided", 400
    try:
        current_article.update_article(markdownContent)  # Assuming update_article is the correct method to handle the update
        return jsonify({"message": "Article updated successfully!"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to update article"}), 500

@app.route("/invoke_agent", methods=["POST"])
def invoke_agent():
    user_input = request.form.get("user_input")
    # Here we call your agent_with_chat_history to handle the input
    result = agent_with_chat_history.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": "example_session_id"}}  # example session_id, adjust as needed
    )
    response = result.get("output", "No response from the agent.")
    return jsonify({"response": response, "content": current_article.__str__()})


if __name__ == "__main__":
    app.run(debug=True)
