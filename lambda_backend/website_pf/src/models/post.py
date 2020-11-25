class Post:
    def __init__(self):
        self.post_name: str = ''
        self.post_url: str = ''
        self.post_slug: str = ''
        self.author_username: str = ''
        self.author_name: str = ''
        self.primary_image_path: str = ''
        self.post_html: str = ''
        self.post_summary: str = ''
        self.post_views: int = 0
        self.post_created_date: str = ''
        self.post_updated_date: str = ''
        self.post_tags: list = []
