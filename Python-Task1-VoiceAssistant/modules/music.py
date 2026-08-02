"""
===========================================
          Music Player Module
===========================================
Author      : Anjali Thakur
Project     : AI Voice Assistant
Internship  : OASIS INFOBYTE
===========================================
"""

import os
import random
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Music Folder
MUSIC_FOLDER = "assets/music"


def play_music():
    """
    Play a random song from music folder
    """

    try:

        if not os.path.exists(MUSIC_FOLDER):
            return "Music folder not found."

        songs = [
            song for song in os.listdir(MUSIC_FOLDER)
            if song.endswith(".mp3")
        ]

        if len(songs) == 0:
            return "No MP3 songs found."

        song = random.choice(songs)

        song_path = os.path.join(MUSIC_FOLDER, song)

        pygame.mixer.music.load(song_path)

        pygame.mixer.music.play()

        return f"Playing {song}"

    except Exception as e:
        return f"Music Error : {e}"


def stop_music():
    """
    Stop currently playing music
    """

    try:

        pygame.mixer.music.stop()

        return "Music stopped."

    except Exception as e:
        return f"Music Error : {e}"


def pause_music():
    """
    Pause music
    """

    try:

        pygame.mixer.music.pause()

        return "Music paused."

    except Exception as e:
        return f"Music Error : {e}"


def resume_music():
    """
    Resume paused music
    """

    try:

        pygame.mixer.music.unpause()

        return "Music resumed."

    except Exception as e:
        return f"Music Error : {e}"