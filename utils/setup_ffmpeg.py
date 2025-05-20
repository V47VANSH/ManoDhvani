# utils/setup_ffmpeg.py
import os
import platform
import subprocess
import urllib.request
import zipfile
import shutil

def ensure_ffmpeg():
    if is_ffmpeg_installed():
        return

    print("🔧 ffmpeg not found. Downloading and configuring...")

    system = platform.system()
    bin_dir = os.path.join(os.getcwd(), "bin")
    os.makedirs(bin_dir, exist_ok=True)

    if system == "Windows":
        ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        zip_path = os.path.join(bin_dir, "ffmpeg.zip")
        urllib.request.urlretrieve(ffmpeg_url, zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(bin_dir)
        os.remove(zip_path)

        # Find ffmpeg.exe in extracted directory
        for root, _, files in os.walk(bin_dir):
            if "ffmpeg.exe" in files:
                src = os.path.join(root, "ffmpeg.exe")
                dst = os.path.join(bin_dir, "ffmpeg.exe")
                shutil.copyfile(src, dst)
                break

        os.environ["PATH"] += os.pathsep + bin_dir

    elif system == "Linux" or system == "Darwin":
        try:
            subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            subprocess.run(["sudo", "apt-get", "install", "-y", "ffmpeg"])

def is_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False
