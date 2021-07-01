"""A video player class."""

from .video_library import VideoLibrary
from .video_playlist import Playlist
from random import choice


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._vid_playing = None
        self._paused = False
        self._playlists = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")

        vid_list = self._video_library.get_all_videos()
        vid_list.sort(key=lambda x: x.title)

        for vid in vid_list:
            tags = vid.format_tags()
            if vid.flag:
                print(f"    {vid.title} ({vid.video_id}) [{tags}] - FLAGGED (reason: {vid.flag_reason})")
            else:
                print(f"    {vid.title} ({vid.video_id}) [{tags}]")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        if self._video_library.get_video(video_id):
            if self._vid_playing:
                self.stop_video()
            self._vid_playing = self._video_library.get_video(video_id)
            self._paused = False
            if self._vid_playing.flag:
                print(f"Cannot play video: Video is currently flagged (reason: {self._vid_playing.flag_reason})")
            else:
                print(f"Playing video: {self._vid_playing.title}")
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if self._vid_playing:
            print(f"Stopping video: {self._vid_playing.title}")
            self._vid_playing = None
            self._paused = False
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        videos = self._video_library.get_all_videos()
        vid = choice(videos)
        while vid.flag:
            videos.remove(vid)
            if videos:
                vid = choice(videos)
            else:
                break
        if videos:
            self.play_video(vid.video_id)
        else:
            print("No videos available")

    def pause_video(self):
        """Pauses the current video."""
        if self._vid_playing:
            if self._paused:
                print(f"Video already paused: {self._vid_playing.title}")
            else:
                print(f"Pausing video: {self._vid_playing.title}")
                self._paused = True
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if self._vid_playing:
            if self._paused:
                print(f"Continuing video: {self._vid_playing.title}")
            else:
                print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        vid = self._vid_playing
        if vid:
            tags = vid.format_tags()
            if self._paused:
                print(f"Currently playing: {vid.title} ({vid.video_id}) [{tags}] - PAUSED")
            else:
                print(f"Currently playing: {vid.title} ({vid.video_id}) [{tags}]")
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in self._playlists:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlists[playlist_name.upper()] = Playlist(playlist_name)
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if playlist_name.upper() in self._playlists:
            vid = self._video_library.get_video(video_id)
            if vid:
                if vid.flag:
                    print(f"Cannot add video to {playlist_name}: "
                          f"Video is currently flagged (reason: {vid.flag_reason})")
                elif vid in self._playlists[playlist_name.upper()].videos:
                    print(f"Cannot add video to {playlist_name}: Video already added")
                else:
                    self._playlists[playlist_name.upper()].videos.append(vid)
                    print(f"Added video to {playlist_name}: {vid.title}")
            else:
                print(f"Cannot add video to {playlist_name}: Video does not exist")
        else:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""
        if self._playlists:
            print("Showing all playlists: ")
            for p in sorted(self._playlists.values(), key=lambda x: x.title):
                print(f"    {p.title}")
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in self._playlists:
            print(f"Showing playlist: {playlist_name}")
            video_list = self._playlists[playlist_name.upper()].videos
            if video_list:
                for vid in video_list:
                    tags = vid.format_tags()
                    if vid.flag:
                        print(f"    {vid.title} ({vid.video_id}) [{tags}] - FLAGGED (reason: {vid.flag_reason})")
                    else:
                        print(f"    {vid.title} ({vid.video_id}) [{tags}]")
            else:
                print("    No videos here yet")
        else:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.upper() in self._playlists:
            vid = self._video_library.get_video(video_id)
            if vid is None:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
            elif vid in self._playlists[playlist_name.upper()].videos:
                self._playlists[playlist_name.upper()].videos.remove(vid)
                print(f"Removed video from {playlist_name}: {vid.title}")
            else:
                print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
        else:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in self._playlists:
            self._playlists[playlist_name.upper()].clear()
            print(f"Successfully removed all videos from {playlist_name}")
        else:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in self._playlists:
            del self._playlists[playlist_name.upper()]
            print(f"Deleted playlist: {playlist_name}")
        else:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")


    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = sorted(self._video_library.get_all_videos(), key=lambda x: x.title)
        results = []
        for vid in videos:
            if search_term.upper() in vid.title.upper():
                if not vid.flag:
                    results.append(vid)

        if results:
            print(f"Here are the results for {search_term}:")
            for i in range(len(results)):
                v = results[i]
                tags = v.format_tags()
                print(f"  {i+1}) {v.title} ({v.video_id}) [{tags}]")

            print("Would you like to play any of the above? If yes, specify the number of the video. ")
            print("If your answer is not a valid number, we will assume it's a no.")
            index = input()
            if index.isnumeric() and (0 <= int(index) <= len(results)):
                self.play_video(results[int(index) - 1].video_id)
        else:
            print(f"No search results for {search_term}")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = sorted(self._video_library.get_all_videos(), key=lambda x: x.title)
        results = []
        for vid in videos:
            if video_tag.lower() in vid.tags:
                if not vid.flag:
                    results.append(vid)

        if results:
            print(f"Here are the results for {video_tag}:")
            for i in range(len(results)):
                v = results[i]
                tags = v.format_tags()
                print(f"  {i+1}) {v.title} ({v.video_id}) [{tags}]")

            print("Would you like to play any of the above? If yes, specify the number of the video. ")
            print("If your answer is not a valid number, we will assume it's a no.")
            index = input()
            if index.isnumeric() and (0 <= int(index) <= len(results)):
                self.play_video(results[int(index) - 1].video_id)
        else:
            print(f"No search results for {video_tag}")

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        vid = self._video_library.get_video(video_id)
        if vid:
            if vid.flag:
                print("Cannot flag video: Video is already flagged")
            else:
                vid.set_flag(flag_reason)
                if self._vid_playing == vid:
                    self.stop_video()
                print(f"Successfully flagged video: {vid.title} (reason: {flag_reason})")
        else:
            print("Cannot flag video: Video does not exist")


    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        vid = self._video_library.get_video(video_id)
        if vid:
            if vid.flag:
                vid.allow()
                print(f"Successfully removed flag from video: {vid.title}")
            else:
                print("Cannot remove flag from video: Video is not flagged")
        else:
            print("Cannot remove flag from video: Video does not exist")

