import os
import sys

def ensure_ffmpeg():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_path = os.path.join(project_dir, '..', 'data', 'ffmpeg.exe')
    ffmpeg_path = os.path.abspath(ffmpeg_path)

    # If ffmpeg.exe exists in that folder, add it to PATH
    if os.path.exists(ffmpeg_path):
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ["PATH"]
    else:
        raise FileNotFoundError(f"ffmpeg.exe not found at {ffmpeg_path}")
