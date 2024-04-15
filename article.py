class Article:
    def __init__(self, path):
        self.path = path
        self.paragraphs = self.load_paragraphs()

    def load_paragraphs(self):
        try:
            with open(self.path) as f:
                return f.readlines()
        except FileNotFoundError:
            print(f"Error: File not found {self.path}")
            return []
        except IOError as e:
            print(f"IOError: {e}")
            return []

    def save_paragraphs(self):
        try:
            with open(self.path, "w") as f:
                f.writelines(self.paragraphs)
        except IOError as e:
            print(f"IOError: {e}")

    def add_paragraph(self, paragraph):
        self.paragraphs.append(paragraph + "\n\n")
        self.save_paragraphs()

    def modify_paragraph(self, index, paragraph):
        if 0 <= index < len(self.paragraphs):
            self.paragraphs[index] = paragraph + "\n\n"
            self.save_paragraphs()
        else:
            print("Error: Index out of range")
