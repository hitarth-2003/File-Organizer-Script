import os
import shutil
from pathlib import Path
from datetime import datetime


class FileOrganizer:
    """
    File Organizer using OOP principles
    - Sorts files based on extension
    - Creates folders automatically
    - Logs operations
    """

    def __init__(self, directory: str):
        self.directory = Path(directory)

        # Extension mapping
        self.file_types = {
            ".pdf": "Documents",
            ".docx": "Documents",
            ".txt": "Documents",
            ".jpg": "Images",
            ".png": "Images",
            ".mp3": "Music",
            ".mp4": "Videos",
            ".zip": "Archives",
        }

        self.log_file = self.directory / "organizer_log.txt"

    def log(self, message: str):
        """Log actions to file"""
        with open(self.log_file, "a") as f:
            f.write(f"[{datetime.now()}] {message}\n")

    def create_folder(self, folder_name: str) -> Path:
        """Create folder if not exists"""
        folder_path = self.directory / folder_name
        folder_path.mkdir(exist_ok=True)
        return folder_path
    

    def confirm_action(self, file_path):
        while True:
            choice = input(f"Move file {file_path.name}? (y/n): ").lower()
            if choice in ['y', 'yes', 'Y']:
                return True
            elif choice in ['n', 'no', 'N']:
                return False
            else:
                print("Invalid input. Please enter 'y' or 'n'.")



    def move_file(self, file_path: Path, destination: Path):
        """Move file safely"""
        try:
            target_path = destination / file_path.name

            # Handle duplicate files
            if target_path.exists():
                target_path = destination / f"{file_path.stem}_copy{file_path.suffix}"

            if not self.confirm_action(file_path):
                print(f"Skipped: {file_path.name}")
                return

            shutil.move(str(file_path), str(target_path))
            print(f"Moved: {file_path.name} -> {destination.name}")
            self.log(f"Moved: {file_path.name} -> {destination.name}")

        except Exception as e:
            print(f"Error moving {file_path.name}: {e}")
            self.log(f"Error: {file_path.name} -> {e}")

    def organize(self):
        """Main method to organize files"""
        if not self.directory.exists():
            print("Directory does not exist!")
            return

        for item in self.directory.iterdir():
            if item.is_dir():
                continue

            file_ext = item.suffix.lower()

            if file_ext in self.file_types:
                folder_name = self.file_types[file_ext]
            else:
                folder_name = "Others"

            folder_path = self.create_folder(folder_name)
            self.move_file(item, folder_path)

 
class Scheduler:
    """
    Simple scheduler (demo purpose)
    """

    def __init__(self, organizer: FileOrganizer):
        self.organizer = organizer

    def run_once(self):
        print("Running File Organizer...")
        self.organizer.organize()


if __name__ == "__main__":
    path = input("Enter directory path to organize: ")

    organizer = FileOrganizer(path)
    scheduler = Scheduler(organizer)

    scheduler.run_once()