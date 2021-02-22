from src.models.author import Author


class Post:
    def __init__(self):
        self.id: str = ''
        self.name: str = ''
        self.idName: str = ''
        self.summary: str = ''
        self.htmlFile: str = ''
        self.primaryImageFile: str = ''
        self.primaryImageThumbnail: str = ''
        self.views: int = 0
        self.createdDate: str = ''
        self.updatedDate: str = ''
        self.tags: list = []
        self.author: Author = Author()
