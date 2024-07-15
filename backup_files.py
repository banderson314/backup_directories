"""
Script made by Brandon Anderson, 2024
Allows user to select two directories: a source directory and a backup directory
The script will compare all files in the two directories, and if any files don't exit in the backup directory that 
exists in the source directory, it will copy it to the backup directory.
Additionally, if any files in the source directory has a more recent "date modified" date, that file will be updated
in the backup directory.
A report will be generated detailing the files that were copied over.
"""

import tkinter as tk
from tkinter import filedialog


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
        entry_widget.configure(width=len(directory) + 3)  # Adjust width based on directory length

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



opening_dialog_box()
print(f"Source directory: {source_directory}")
print(f"Backup directory: {backup_directory}")