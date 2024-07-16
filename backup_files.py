"""
Script made by Brandon Anderson, July 2024
Allows user to select two directories: a source directory and a backup directory
The script will compare all files in the two directories, and if any files don't exit in the backup directory that 
exists in the source directory, it will copy it to the backup directory.
Additionally, if any files in the source directory has a more recent "date modified" date, that file will be updated
in the backup directory.
A report will be generated detailing the files that were copied over.
"""

import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox

def opening_dialog_box():
    """
    Function in which the user defines the folder to copy and the backup location
    
    Input parameters: 
    None
    
    Returns: 
    None, but does define global variables:
    source_directory (str), backup_directory (str)

    Dialog box uses a grid system with 3 rows and 3 columns
    """

    # When the user clicks "OK"
    def on_ok_click(event=None):
        global source_directory, backup_directory
        source_directory = source_entry_var.get()
        backup_directory = backup_entry_var.get()
        window.destroy()
        root.destroy()

    # When the user exits the dialog box
    def on_close_window(event=None):
        exit()

    # Function to create a label and an entry field in a grid
    def create_label_entry_grid(row, column, text, default_value, entry_var):
        label = tk.Label(window, text=text)
        label.grid(row=row, column=column, padx=5, pady=0, sticky="w")

        entry_var.set(default_value)
        entry = tk.Entry(window, textvariable=entry_var, width=40)  # Initial width set to 40
        entry.grid(row=row, column=column + 1, padx=5, pady=0, sticky="ew")

        return entry  # Return the entry widget for further use if needed

    # Function to let the user select a directory
    def user_select_directory(entry_widget, entry_var):
        directory = filedialog.askdirectory()
        entry_var.set(directory)  # Update entry variable
        entry_widget.configure(width=len(directory))  # Adjust width based on directory length

    # Initial set up of window
    root = tk.Tk()
    root.withdraw() # Hide the initial window
    window = tk.Toplevel()
    window.title("User input")
    window.protocol("WM_DELETE_WINDOW", on_close_window)

    source_entry_var = tk.StringVar()
    backup_entry_var = tk.StringVar()

    source_entry = create_label_entry_grid(0, 0, "Source directory: ", "", source_entry_var)
    source_button = tk.Button(window, text="Choose", command=lambda: user_select_directory(source_entry, source_entry_var))
    source_button.grid(row=0, column=2, padx=5, pady=0, sticky="e")

    backup_entry = create_label_entry_grid(1, 0, "Backup folder: ", "", backup_entry_var)
    backup_button = tk.Button(window, text="Choose", command=lambda: user_select_directory(backup_entry, backup_entry_var))
    backup_button.grid(row=1, column=2, padx=5, pady=0, sticky="e")

    ok_button = tk.Button(window, text="OK", command=on_ok_click)
    ok_button.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="ew")

    window.bind("<Escape>", on_close_window)
    window.bind("<Return>", on_ok_click)

    root.mainloop()



#opening_dialog_box()
#print(f"Source directory: {source_directory}")
#print(f"Backup directory: {backup_directory}")

source_directory = "C:/Users/bran314/Desktop/Delete - test files/Sodium-iodate-induced GA"
backup_directory = "C:/Users/bran314/Desktop/Delete - test files/Backup 2 - Copy"

# Checks to make sure directory imput is proper
# Checks that user put in something for both directories
if source_directory == "" or backup_directory == "":
    print("Directory not specified")
    exit()
# Checks that directories aren't contained within one another
common_path = os.path.commonpath([source_directory, backup_directory])
if common_path == os.path.normpath(source_directory) or common_path == os.path.normpath(backup_directory):
    print("Directories cannot be located within each other")
    exit()
# Checks that directories actually exist
if not os.path.exists(source_directory):
    print(f"Source directory '{source_directory}' does not exist.")
    exit()    
elif not os.path.exists(backup_directory):
    print(f"Backup directory '{backup_directory}' does not exist.")
    exit()
    


def compare_and_copy_files_backup(source, backup):
    for root, _, files in os.walk(source):
        # Create corresponding directory structure in the backup directory
        relative_path = os.path.relpath(root, source)
        backup_root = os.path.join(backup, relative_path)
        os.makedirs(backup_root, exist_ok=True)
        
        for file in files:
            source_file = os.path.join(root, file)
            backup_file = os.path.join(backup_root, file)
            
            # Compare modification times and copy if necessary
            if not os.path.exists(backup_file) or os.path.getmtime(source_file) > os.path.getmtime(backup_file):
                try:
                    shutil.copy2(source_file, backup_file)
                    print(f'Transferred: {source_file} to {backup_file}')
                except Exception as e:
                    print(f'Error copying {source_file} to {backup_file}: {e}')


def compare_and_copy_files(source, backup):
    total_bytes_added = 0
    files_transferred = 0
    files_updated = 0
    files_skipped = 0
    files_failed = 0
    initial_directories = []
    created_directories = []
    for root, _, _ in os.walk(backup):
        relative_path = os.path.relpath(root, backup)
        initial_directories.append(relative_path)

    for root, _, files in os.walk(source):
        # Create corresponding directory structure in the backup directory
        relative_path = os.path.relpath(root, source)
        backup_root = os.path.join(backup, relative_path)
        os.makedirs(backup_root, exist_ok=True)
        if relative_path not in initial_directories:
            created_directories.append(relative_path)

        for file in files:
            source_file = os.path.join(root, file)
            backup_file = os.path.join(backup_root, file)
            
            # Copy if doesn't exist or is not updated in backup location
            if not os.path.exists(backup_file) or os.path.getmtime(source_file) > os.path.getmtime(backup_file):
                try:
                    shutil.copy2(source_file, backup_file)
                    files_transferred += 1
                    total_bytes_added += os.path.getsize(source_file)
                except Exception as e:
                    files_failed += 1
            else:
                files_skipped += 1
    




    # Summary of data transfer
    # When the user clicks "OK"
    def on_ok_click(event=None):
        exit()

    # When the user exits the dialog box
    def on_close_window(event=None):
        exit()



    # Create summary dialog
    root = tk.Tk()
    root.withdraw()  # Hide main window
    window = tk.Toplevel()
    window.title("Transfer summary")
    window.protocol("WM_DELETE_WINDOW", on_close_window)

    summary_message = (
        f"Directories created: {len(created_directories)}\n"
        f"Files transferred: {files_transferred}\n"
        f"Files updated: {files_updated}\n"
        f"Files skipped (up to date): {files_skipped}\n"
        f"Files failed to transfer: {files_failed}\n"
        f"Amount of GB added to backup: {total_bytes_added / (1024**3):.2f} GB"
    )

    def directory_details():
        details_window = tk.Toplevel()
        details_window.title("Details")
        text = ""
        for i in created_directories:
            text += f"{i} \n"
        label = tk.Label(details_window, text=text, justify=tk.LEFT)
        label.pack()

    # Add text to the window
    def create_text(row, text, details_box):
        label = tk.Label(window, text=text)
        label.grid(row=row, column=0, padx=5, pady=0, sticky="w")

    directory_label = tk.Label(window, text=f"Directories created: {len(created_directories)}")
    directory_label.grid(row=0, column=0, padx=5, pady=0, sticky="w")
    directory_details_button = tk.Button(window, text="Details", command=directory_details)
    directory_details_button.grid(row=0, column=2, padx=5, pady=0, sticky="e")



    ok_button = tk.Button(window, text="OK", command=on_ok_click)
    ok_button.grid(row=6, column=0, columnspan=3, padx=5, pady=10, sticky="ew")

    window.bind("<Escape>", on_close_window)
    window.bind("<Return>", on_ok_click)

    # Function to show detailed file information
    def show_file_details():
        file_details = tk.Toplevel()
        file_details.title("File Details")
        text_area = scrolledtext.ScrolledText(file_details, width=80, height=20)
        
        for root_dir in created_directories:
            text_area.insert(tk.END, f"\nDirectory: {root_dir}\n")
            for root, _, files in os.walk(root_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    text_area.insert(tk.END, f"{file_path}\n")
        
        text_area.configure(state='disabled')
        text_area.pack(expand=True, fill='both')

        close_button = tk.Button(file_details, text="Close", command=file_details.destroy)
        close_button.pack()


    root.mainloop()


compare_and_copy_files(source_directory, backup_directory)
