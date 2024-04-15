class Article:
    def __init__(self, path):
        self.path = path

    def __str__(self):
        with open(self.path) as f:
            return f.read()
    
    def add_paragraph(self, paragraph, index=None):
        with open(self.path) as f:
            paragraphs = f.readlines()
        if index is None or index == -1:
            paragraphs.append(paragraph + "\n")
        else:
            paragraphs.insert(index, paragraph + "\n")
        with open(self.path, "w") as f:
            f.write("".join(paragraphs))   

    def modify_paragraph(self, index, paragraph):
        with open(self.path) as f:
            paragraphs = f.readlines()
        paragraphs[index] = paragraph + "\n"
        with open(self.path, "w") as f:
            f.write("".join(paragraphs))

    def remove_paragraph(self, index):
        with open(self.path) as f:
            paragraphs = f.readlines()
        del paragraphs[index]
        with open(self.path, "w") as f:
            f.write("".join(paragraphs))

    def get_paragraph(self, index):
        with open(self.path) as f:
            paragraphs = f.readlines()
        return paragraphs[index]
    
    def get_all_paragraphs(self):
        """Returns a json object with all paragraphs and their indexes"""
        with open(self.path) as f:
            paragraphs = f.readlines()
        return {i: p for i, p in enumerate(paragraphs)}
    
    def update_article(self, article):
        with open(self.path, "w") as f:
            f.write(article)

