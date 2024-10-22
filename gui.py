import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Listbox, scrolledtext
import os
import json
import subprocess  # To open folders in file explorer
import reee  # Import your random image script (reee.py)
from ttkthemes import ThemedTk  # Import for applying themes

# File where folder paths will be saved
CONFIG_FILE = "config.json"

# Function to load folder paths from the config file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return []

# Function to save folder paths to the config file
def save_config(folder_paths):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(folder_paths, f)

# Function to browse and add folders
def add_folder():
    folder = filedialog.askdirectory(title="Select Folder")
    if folder:
        folder_paths.append(folder)
        update_folder_listbox()
        save_config(folder_paths)  # Save updated folder paths

# Function to remove the selected folder
def remove_selected_folder():
    selected_idx = folder_listbox.curselection()
    if selected_idx:
        folder_paths.pop(selected_idx[0])
        update_folder_listbox()
        save_config(folder_paths)  # Save updated folder paths

# Function to update the listbox displaying folder paths
def update_folder_listbox():
    folder_listbox.delete(0, tk.END)
    for folder in folder_paths:
        folder_listbox.insert(tk.END, folder)

# Function to run random image selection
def run_random_selection():
    try:
        num_images = int(num_images_entry.get())
        reee.copy_random_images(folder_paths, num_images)
        update_refs()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to refresh the reference folder list
def update_refs():
    ref_folder = os.path.join(os.getcwd(), "ref")
    if os.path.exists(ref_folder):
        ref_listbox.delete(0, tk.END)  # Clear the reference list
        ref_folders = sorted([d for d in os.listdir(ref_folder) if os.path.isdir(os.path.join(ref_folder, d))])
        for folder in ref_folders:
            ref_listbox.insert(tk.END, folder)

# Function to open the selected reference folder in file explorer
def open_ref_folder(event):
    selected_ref = ref_listbox.get(ref_listbox.curselection())
    ref_folder = os.path.join(os.getcwd(), "ref", selected_ref)
    if os.path.exists(ref_folder):
        if os.name == 'nt':  # For Windows
            subprocess.Popen(f'explorer "{ref_folder}"')
        else:  # For Mac or Linux
            subprocess.Popen(['open', ref_folder])

# Function to open the logs folder in file explorer
def open_logs_folder():
    logs_folder = os.path.join(os.getcwd(), "logs")
    if os.path.exists(logs_folder):
        if os.name == 'nt':  # For Windows
            subprocess.Popen(f'explorer "{logs_folder}"')
        else:  # For Mac or Linux
            subprocess.Popen(['open', logs_folder])
            
# Function to open the ref folder in file explorer
def open_refs_folder():
    ref_folder = os.path.join(os.getcwd(), "ref")
    if os.path.exists(ref_folder):
        if os.name == 'nt':  # For Windows
            subprocess.Popen(f'explorer "{ref_folder}"')
        else:  # For Mac or Linux
            subprocess.Popen(['open', ref_folder])

# Create the main window with the Equilux theme
# window = tk.Tk()
window = ThemedTk(theme="yaru")
window.title("Random Image Selector")
window.geometry("460x580")

# Load folder paths from config file
folder_paths = load_config()

# Set up the main frame for layout
main_frame = ttk.Frame(window, padding="20")
main_frame.pack(fill='both', expand=True)

# Configure the grid columns to have equal weight
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)

# Label and Entry for number of images
num_images_label = ttk.Label(main_frame, text="Number of images to copy:")
num_images_label.grid(row=0, column=0, sticky='w')

num_images_entry = ttk.Entry(main_frame, width=10)
num_images_entry.grid(row=0, column=1, padx=10, pady=10)

# Create the "Random!" button
random_button = ttk.Button(main_frame, text="Random!", command=run_random_selection)
random_button.grid(row=0, column=2, padx=20, pady=10)

# Create a Listbox to display folder paths
folder_listbox = Listbox(main_frame, font=("Consolas", 12), height=5, width=40)
folder_listbox.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)

# Buttons to add and remove folders (placed under the folder list)
add_folder_button = ttk.Button(main_frame, text="Add Folder", command=add_folder)
add_folder_button.grid(row=2, column=0, padx=10, pady=20, sticky='ew')

remove_folder_button = ttk.Button(main_frame, text="Remove Selected", command=remove_selected_folder)
remove_folder_button.grid(row=2, column=1, padx=10, pady=20, sticky='ew')

# Initial loading of folder paths
update_folder_listbox()

# Create a listbox to display the reference folders
ref_listbox = Listbox(main_frame, font=("Consolas", 12), height=10, width=40, justify="center")
ref_listbox.grid(row=4, column=0, columnspan=3, sticky='nsew', padx=10, pady=5)

# Bind double-click action to open the reference folder
ref_listbox.bind('<Double-Button-1>', open_ref_folder)

# Scrollbar for reference listbox
ref_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=ref_listbox.yview)
ref_scrollbar.grid(row=4, column=3, sticky="ns")
ref_listbox.config(yscrollcommand=ref_scrollbar.set)

# Buttons to refresh, open logs, and ref folders, spaced equally
refresh_button = ttk.Button(main_frame, text="Refresh", command=update_refs)
refresh_button.grid(row=5, column=0, padx=10, pady=20, sticky="ew")

logs_button = ttk.Button(main_frame, text="Logs", command=open_logs_folder)
logs_button.grid(row=5, column=1, padx=10, pady=20, sticky="ew")

ref_button = ttk.Button(main_frame, text="Ref", command=open_refs_folder)
ref_button.grid(row=5, column=2, padx=10, pady=20, sticky="ew")

# Load reference folders at startup
update_refs()

# Start the GUI loop
window.mainloop()
