"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, title):
        self.title = title
        self.videos = []

    def clear(self):
        self.videos = []
