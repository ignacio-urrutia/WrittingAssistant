import uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from writerAgent import Article, invoke_agent_with_chat_history  # Ensure your agent and Article class are imported here
from dotenv import load_dotenv

from firestore_config import db


load_dotenv()


app = Flask(__name__)

def generate_session_id():
    """Generate a unique session id"""
    return str(uuid.uuid4())

def start_session(session_id, sample_text):
    db.collection('sessions').document(session_id).set({
        'sample_text': sample_text,
        'chat_history': [],
        'article': ''
    })

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'md'}

def update_session_sample_text(session_id, text):
    db.collection('sessions').document(session_id).update({
        'sample_text': text
    })

@app.route("/")
def index():
    session_id = generate_session_id()
    sample_text = ""
    start_session(session_id, sample_text)
    return redirect(url_for('session_index', session_id=session_id))

@app.route("/load_session", methods=["POST"])
def load_session():
    session_id = request.form.get("session_id")
    if session_id is None:
        return "No session id provided", 400
    session = db.collection('sessions').document(session_id).get()
    if not session.exists:
        return "Session not found", 404
    return redirect(url_for('session_index', session_id=session_id))

@app.route("/session/<session_id>")
def session_index(session_id):
    current_article = Article(session_id)
    content = current_article.get_article()
    return render_template("index.html", content=content, session_id=session_id)

@app.route("/update_article/<session_id>", methods=["POST"])
def update_article(session_id):
    data = request.get_json()
    markdown_content = data.get('article')
    if markdown_content is None:
        return "No content provided", 400
    try:
        current_article = Article(session_id)
        current_article.update_article(markdown_content)
        return jsonify({"message": "Article updated successfully!"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to update article"}), 500


@app.route("/invoke_agent", methods=["POST"])
def invoke_agent():
    user_input = request.form.get("user_input")
    session_id = request.form.get("session_id")
    if user_input is None or session_id is None:
        return "No user input or session id provided", 400
    try:
        response, content = invoke_agent_with_chat_history(session_id, user_input)
        # add_to_chat_history(session_id, response)
        return jsonify({"response": response, "content": content}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to invoke agent"}), 500
    
@app.route('/upload_sample_text/<session_id>', methods=['POST'])
def upload_sample_text(session_id):
    if 'sample_text_file' not in request.files:
        return 'No file part', 400
    file = request.files['sample_text_file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        text = file.read().decode('utf-8')
        update_session_sample_text(session_id, text)
        return redirect(url_for('session_index', session_id=session_id))
    return 'Invalid file', 400


if __name__ == "__main__":
    app.run(debug=True)
