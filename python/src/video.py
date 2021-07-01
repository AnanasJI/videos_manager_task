"""A video class."""

from typing import Sequence


class Video:
    """A class used to represent a Video."""

    def __init__(self, video_title: str, video_id: str, video_tags: Sequence[str]):
        """Video constructor."""
        self._title = video_title
        self._video_id = video_id

        # Turn the tags into a tuple here so it's unmodifiable,
        # in case the caller changes the 'video_tags' they passed to us
        self._tags = tuple(video_tags)
        self._flag = False
        self._flag_reason = "Not supplied"

    @property
    def title(self) -> str:
        """Returns the title of a video."""
        return self._title

    @property
    def video_id(self) -> str:
        """Returns the video id of a video."""
        return self._video_id

    @property
    def tags(self) -> Sequence[str]:
        """Returns the list of tags of a video."""
        return self._tags

    @property
    def flag(self) -> str:
        """Returns the reason for flag."""
        return self._flag

    @property
    def flag_reason(self) -> str:
        """Returns the reason for flag."""
        return self._flag_reason

    def set_flag(self, reason="Not supplied"):
        self._flag_reason = reason
        self._flag = True

    def allow(self):
        self._flag_reason = "Not supplied"
        self._flag = False

    def format_tags(self):
        return ' '.join([str(elem) for elem in self.tags]).replace("(", "").replace(")", "").replace("'", "")