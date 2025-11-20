import os
import shutil


def cleanup():
    path = os.path.expanduser("~/.chromadb")
    if os.path.exists(path):
        shutil.rmtree(path)
        print("Chroma cache cleared.")
    else:
        print("No Chroma cache found.")


if __name__ == "__main__":
    cleanup()
