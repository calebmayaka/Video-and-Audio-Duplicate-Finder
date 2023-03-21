import os
import hashlib
from tkinter import Tk, filedialog, messagebox

def find_duplicate_files(folder_path):
    '''Finds duplicate files in a given folder and its subfolders'''
    hashes = {}
    duplicates = []

    # Traverse the folder and its subfolders
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Only consider video and audio files
            if not (filename.lower().endswith('.mp3') or 
                    filename.lower().endswith('.mp4') or 
                    filename.lower().endswith('.avi') or 
                    filename.lower().endswith('.mkv')):
                continue

            # Calculate the MD5 hash of the file
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

            # If the hash already exists, the file is a duplicate
            if file_hash in hashes:
                duplicates.append(file_path)
                continue

            # Otherwise, store the hash and file path for future comparisons
            hashes[file_hash] = file_path

    return duplicates

def delete_files(file_paths):
    '''Deletes a list of files'''
    for file_path in file_paths:
        os.remove(file_path)

def select_folder():
    '''Opens a file dialog to select a folder'''
    root = Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path

def main():
    '''Main function'''
    # Prompt the user to select a folder
    folder_path = select_folder()

    if not folder_path:
        return

    # Find duplicate files in the selected folder
    duplicates = find_duplicate_files(folder_path)

    if not duplicates:
        # If no duplicates are found, inform the user and exit
        messagebox.showinfo('No duplicates found', 'No duplicate video or audio files found.')
        return

    # Otherwise, display a message box showing the list of files to be deleted
    message = 'The following files will be deleted:\n\n'
    for file_path in duplicates:
        message += f'{file_path}\n'
    message += '\nDo you want to continue?'

    # Ask the user for confirmation to delete the files
    if messagebox.askyesno('Delete duplicates', message):
        # If the user confirms, delete the files
        delete_files(duplicates)
        messagebox.showinfo('Duplicates deleted', f'{len(duplicates)} files deleted.')
    else:
        # If the user cancels, inform them that no files were deleted
        messagebox.showinfo('Duplicates not deleted', 'No files were deleted.')

if __name__ == '__main__':
    main()
