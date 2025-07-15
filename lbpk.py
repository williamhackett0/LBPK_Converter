import tkinter as tk
from tkinter import filedialog, Label
from converter import convert_files
import webbrowser

ARCHIVE_PATH = ""  # Placeholder for archive path
OUTPUT_PATH = ""    # Placeholder for output path

def select_archive_path():
    global ARCHIVE_PATH
    directory_path = filedialog.askdirectory()

    if directory_path:
        archive_path_label.config(text=f"Selected: {directory_path}")
        ARCHIVE_PATH = directory_path
    else:
        archive_path_label.config(text="No directory selected.")
def select_output_path():
    global OUTPUT_PATH
    directory_path = filedialog.askdirectory()

    if directory_path:
        output_path_label.config(text=f"Selected: {directory_path}")
        OUTPUT_PATH = directory_path
    else:
        output_path_label.config(text="No directory selected.")
        output_path_label.config(text="No directory selected.")

def convert():
    """
    This function is called when the Convert button is clicked.
    It will call the convert_files function with the selected paths.
    """
    print("Convert button clicked.")
    write_to_console("Starting conversion...")
    write_to_console(f"Archive path: {ARCHIVE_PATH}\nOutput path: {OUTPUT_PATH}")

    if ARCHIVE_PATH and OUTPUT_PATH:
        convert_files(ARCHIVE_PATH, OUTPUT_PATH, write_to_console)
    else:
        write_to_console("Please select both archive and output directories.")

# --- Setup the main window ---
window = tk.Tk()
window.title("LBPK Community Track Converter")
window.geometry("650x650")

top_frame = tk.Frame(window)
top_frame.pack(pady=10)

path_label = Label(
    top_frame,
    text="This tool converts Little Big Planet Karting archieved community tracks (https://archive.org/details/LBPKServer) into local game saves. \n\n Select a handful of community tracks to convert at a time! \n\n Please select the archive directory and the output directory.",
    wraplength=500
)
path_label.pack(side=tk.TOP, padx=10)

# Select Archive Directory row
row1 = tk.Frame(top_frame)
row1.pack(fill=tk.X, pady=15)

select_button1 = tk.Button(
    row1,
    text="Select Archive Directory",
    command=select_archive_path,
    width=20
)
select_button1.pack(side=tk.LEFT, padx=5)

archive_path_label = Label(
    row1,
    text="No directory selected yet.",
    wraplength=500,
    anchor="w",
    justify="left"
)
archive_path_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

# Select Output Directory row
row2 = tk.Frame(top_frame)
row2.pack(fill=tk.X, pady=5)

select_button2 = tk.Button(
    row2,
    text="Select Output Directory",
    command=select_output_path,
    width=20
)
select_button2.pack(side=tk.LEFT, padx=5)

output_path_label = Label(
    row2,
    text="No directory selected yet.",
    wraplength=500,
    anchor="w",
    justify="left"
)
output_path_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

# Convert button row
row3 = tk.Frame(top_frame)
row3.pack(fill=tk.X, pady=15)

convert_button = tk.Button(
    row3,
    text="Convert",
    width=20,
    command=convert
)
convert_button.pack(side=tk.LEFT, padx=5)

# Info label under the Convert button
ftp_info_label = Label(
    top_frame,
    text="In your output folder you will find track folders containing 6 track files. Transfer the 6 files to your PS3 via FTP: \n\n '/dev_hdd0/game/NPEA00421_UCC/USRDIR/1/DATA/LOCAL/TRACK'",
    wraplength=500,
    anchor="w",
    justify="left"
)
ftp_info_label.pack(pady=(0, 10), padx=10, anchor="w")

# Console output row
console_frame = tk.Frame(window)
console_frame.pack(fill=tk.BOTH, expand=True, padx=10)

console_label = Label(console_frame, text="Console Output:", anchor="w", justify="left")
console_label.pack(anchor="w")

console_text = tk.Text(console_frame, height=6, wrap="word", state="disabled")
console_text.pack(fill=tk.BOTH, expand=True)

# Author info row with clickable GitHub link
def open_github(event=None):
    webbrowser.open_new("https://github.com/williamhackett0/LBPK_Converter")

author_frame = tk.Frame(window)
author_frame.pack(side=tk.BOTTOM, pady=5, anchor="w", fill=tk.X)

author_label = Label(
    author_frame,
    text="This tool was made by William Hackett.",
    anchor="w",
    justify="left",
    fg="gray"
)
author_label.pack(side=tk.LEFT)

github_link = Label(
    author_frame,
    text="GitHub: LBPK_Converter",
    fg="gray",
    cursor="hand2",
    anchor="w",
    justify="right"
)
github_link.pack(side=tk.LEFT)
github_link.bind("<Button-1>", open_github)

def write_to_console(message):
    console_text.config(state="normal")
    console_text.insert(tk.END, message + "\n")
    console_text.see(tk.END)
    console_text.config(state="disabled")

# --- Start the application ---
window.mainloop()