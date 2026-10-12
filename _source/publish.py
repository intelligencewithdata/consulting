"""Rebuild the whole site from _source and copy it into the repository root (GitHub Pages serves the root).
Usage (from the repo root):  python3 _source/publish.py"""
import pathlib, shutil, subprocess, sys

SRC = pathlib.Path(__file__).parent
REPO = SRC.parent
subprocess.run([sys.executable, str(SRC / "og" / "render_articles.py")], check=True)
subprocess.run([sys.executable, str(SRC / "build.py")], check=True)
BUILD = REPO / "_build"
shutil.copytree(BUILD, REPO, dirs_exist_ok=True)
shutil.rmtree(BUILD)
print("site published into", REPO)
