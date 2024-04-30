import zipfile 
import os 

from datetime import datetime

def backup_directory(directory):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    zip_filename = f"backup_db_{date_time}.zip"

    if not os.path.exists(directory):
        print(f"Directory '{directory}' does not exist.")
        return

    # Create a new ZIP file
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # Walk through the directory and add files to the ZIP file
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                # Get the full path of the file
                filepath = os.path.join(foldername, filename)
                # Add the file to the ZIP file with relative path
                zipf.write(filepath, os.path.relpath(filepath, directory))

    print(f"Backup created: {zip_filename}")

if __name__ == "__main__":
    backup_directory()
