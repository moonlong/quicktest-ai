from .content import Content


class Page:
    def __init__(self):
        self.content = []

    def add_content(self, content: Content):
        self.content.append(content)
