class SearchResult:
    def __init__(self, title, image_url, url, preview_image) -> None:
        self.preview_image = preview_image
        self.image_url = image_url
        self.title = title
        self.url = url

    def __str__(self) -> str:
        return f"{self.image_url}"

    def __repr__(self) -> str:
        return f'<SearchResult image_url={self.image_url}>'
