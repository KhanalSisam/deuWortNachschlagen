import os


def play_audio(audio_link):
    os.system(
        f"mpv https:{audio_link} >nul 2>&1")
