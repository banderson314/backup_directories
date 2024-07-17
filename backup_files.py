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
from collections import defaultdict
import time


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

    source_entry = create_label_entry_grid(0, 0, "Source folder: ", "", source_entry_var)
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



opening_dialog_box()
print(f"Source directory: {source_directory}")
print(f"Backup directory: {backup_directory}")


### Checks to make sure directory input is proper ###
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
    



def compare_and_copy_files(source, backup):
    """
    First compares the backup to the source, and if any files don't exist or are not as up to date in the backup,
    it will copy (shutil.copy2) it over to the backup folder. It will then give a report for the user, with 
    optional details.
    Input:
    Source and backup locations (str, written as paths)
    Output:
    None
    """
    start_time = time.time()

    total_bytes_added = 0
    files_transferred_count = 0
    files_updated_count = 0
    files_skipped_count = 0
    files_failed_count = 0

    files_transferred = []
    files_updated = []
    files_skipped = []
    files_failed = []

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
            #file_relative_path = os.path.relpath()
            source_file = os.path.join(root, file)
            backup_file = os.path.join(backup_root, file)
            
            # Copy if doesn't exist or is not updated in backup location
            if not os.path.exists(backup_file): # Copy if doesn't exit
                try:
                    shutil.copy2(source_file, backup_file)
                    files_transferred_count += 1
                    files_transferred.append(os.path.join(relative_path, file))
                    total_bytes_added += os.path.getsize(source_file)
                except Exception as e:
                    files_failed_count += 1
                    files_failed.append(os.path.join(relative_path, file))
            elif os.path.getmtime(source_file) > os.path.getmtime(backup_file): # Copy if not updated
                try:
                    backup_file_size = os.path.getsize(backup_file)
                    source_file_size = os.path.getsize(source_file)
                    change_in_file_size = source_file_size - backup_file_size
                    shutil.copy2(source_file, backup_file)
                    files_updated_count += 1
                    files_updated.append(os.path.join(relative_path, file))
                    total_bytes_added += change_in_file_size
                except Exception as e:
                    files_failed_count += 1
                    files_failed.append(os.path.join(relative_path, file))
            else:   # Don't copy if already there and updated
                files_skipped_count += 1
                files_skipped.append(os.path.join(relative_path, file))
    
    # Calculating time took to transfer files
    end_time = time.time()
    elapsed_time_seconds = round(end_time - start_time)
    if elapsed_time_seconds > 60:
        elapsed_time_minutes = elapsed_time_seconds // 60
        elapsed_time_remainder_seconds = elapsed_time_seconds % 60
        elapsed_time_statement = f"Time to transfer: {elapsed_time_minutes} m {elapsed_time_remainder_seconds} s"
    else:
        elapsed_time_statement = f"Time to transfer: {elapsed_time_seconds} s"
        

    ### Summary of data transfer ###
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


    # Add text to the window
    row_count = 0
    def create_report_row(summary_text, include_details_option, details_text):
        def details_window(text):
            details_window = tk.Toplevel()
            details_window.title("Details")
            
            text_area = scrolledtext.ScrolledText(details_window, wrap=tk.WORD, width=80, height=30)
            text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            text_area.insert(tk.END, text)
            text_area.config(state=tk.DISABLED)
        
        
        nonlocal row_count
        label = tk.Label(window, text=summary_text)
        label.grid(row=row_count, column=0, padx=10, pady=0, sticky="w")
        if include_details_option:
            details_button = tk.Button(window, text="Details", command=lambda: details_window(details_text))
            details_button.grid(row=row_count, column=1, padx=10, pady=0, sticky="e")
        row_count += 1



    def create_details_text(list_of_paths):
        """
        Converts a list of file paths into one text variable that is organized by directory tree
        Input:
        One list of strings that are file paths
        Output:
        One string with organized layout formatted to be used in details window of report dialog box
        """
        def build_tree(paths):
            tree = lambda: defaultdict(tree)
            root = tree()
            for path in paths:
                path = os.path.normpath(path)
                parts = path.split(os.sep)
                current = root
                for part in parts:
                    current = current[part]
            return root

        def format_tree(d, indent=0, is_top_level=True):
            result = []
            for key, value in sorted(d.items()):
                if is_top_level:
                    result.append(key)
                else:
                    result.append(' ' * indent + '├── ' + key)
                if isinstance(value, defaultdict):
                    result.extend(format_tree(value, indent + 4, is_top_level=False))
            return result

        tree = build_tree(list_of_paths)
        formatted_tree = format_tree(tree)
        return '\n'.join(formatted_tree)
    

    directory_details_text = create_details_text(created_directories)
    files_transferred_details_text = create_details_text(files_transferred)
    files_updated_details_text = create_details_text(files_updated)
    files_skipped_details_text = create_details_text(files_skipped)
    files_failed_details_text = create_details_text(files_failed)

    create_report_row(f"Directories created: {len(created_directories)}", True, directory_details_text)
    create_report_row(f"Files transferred: {files_transferred_count}\n", True, files_transferred_details_text)
    create_report_row(f"Files updated: {files_updated_count}\n", True, files_updated_details_text)
    create_report_row(f"Files skipped (up to date): {files_skipped_count}\n", True, files_skipped_details_text)
    create_report_row(f"Files failed to transfer: {files_failed_count}\n", True, files_failed_details_text)
    create_report_row(f"Amount of GB added to backup: {total_bytes_added / (1024**3):.2f} GB", False, "")
    create_report_row(elapsed_time_statement, False, "")


    ok_button = tk.Button(window, text="OK", command=on_ok_click)
    ok_button.grid(row=row_count, column=1, columnspan=1, padx=5, pady=10, sticky="ew")

    window.bind("<Escape>", on_close_window)
    window.bind("<Return>", on_ok_click)


    root.mainloop()


compare_and_copy_files(source_directory, backup_directory)
