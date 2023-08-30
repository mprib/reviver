from pathlib import Path
import shutil

def delete_directory_contents(directory: Path):
    if directory.exists() and directory.is_dir():
        for item in directory.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        print(f"The path {directory} does not exist or is not a directory.")