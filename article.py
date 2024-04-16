
from firebase_admin import firestore
from firestore_config import db

class Article:
    def __init__(self, session_id):
        self.session_id = session_id
        self.db = db
        
    def get_article(self):
        doc = self.db.collection('sessions').document(self.session_id).get()
        return doc.to_dict()['article'] if doc.exists else ''
    
    def get_sample_text(self):
        doc = self.db.collection('sessions').document(self.session_id).get()
        return doc.to_dict()['sample_text'] if doc.exists else ''
    
    def set_chat_history(self, chat_history):
        self.db.collection('sessions').document(self.session_id).set({'chat_history': chat_history}, merge=True)

    def get_chat_history(self):
        doc = self.db.collection('sessions').document(self.session_id).get()
        return doc.to_dict()['chat_history'] if doc.exists else []

    def update_article(self, article):
        self.db.collection('sessions').document(self.session_id).set({'article': article}, merge=True)

    def add_paragraph(self, paragraph, index=-1):
        article = self.get_article()
        paragraphs = article.split('\n')
        if index == -1 or index >= len(paragraphs):
            paragraphs.append(paragraph)
        else:
            paragraphs.insert(index, paragraph)
        self.update_article('\n'.join(paragraphs))

    def modify_paragraph(self, index, paragraph):
        article = self.get_article()
        paragraphs = article.split('\n')
        paragraphs[index] = paragraph
        self.update_article('\n'.join(paragraphs))

    def remove_paragraph(self, index):
        article = self.get_article()
        paragraphs = article.split('\n')
        del paragraphs[index]
        self.update_article('\n'.join(paragraphs))

    def get_paragraph(self, index):
        article = self.get_article()
        paragraphs = article.split('\n')
        return paragraphs[index]
    
    def get_all_paragraphs(self):
        article = self.get_article()
        paragraphs = article.split('\n')
        return {i: p for i, p in enumerate(paragraphs)}
    
    def __str__(self):
        return self.get_article()
