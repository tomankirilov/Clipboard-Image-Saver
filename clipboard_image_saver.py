import json
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import ImageGrab

# -------------------------------------
# App Metadata & Local Paths
# -------------------------------------

APP_NAME = "ClipboardImageSaver"

# Config lives here — typical AppData path for Windows
CONFIG_DIR = Path.home() / "AppData" / "Local" / APP_NAME
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_FILE = CONFIG_DIR / "config.json"

# Icon setup — ICO for Windows, PNG for Tkinter photoimage
ICON_ICO_PATH = Path(__file__).parent / "app.ico"
ICON_PNG_PATH = Path(__file__).parent / "app.png"

# Fallback dir if nothing is chosen
DEFAULT_IMAGE_DIR = Path.home() / "Pictures"

# -------------------------------------
# UI Text & Color Constants
# -------------------------------------

PLACEHOLDER_TEXT = "(optional)"
COLOR_PLACEHOLDER = "gray"
COLOR_NORMAL = "black"

# -------------------------------------
# Config read/write
# -------------------------------------

def load_user_config():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading config file:", e)
    return {}

def save_user_config():
    # Basic settings snapshot
    prefs = {
        "directory": dir_var.get(),
        "extension": ext_var.get(),
        "silent_save": silent_var.get(),
    }
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=2)
    except Exception as e:
        print("Failed to write config file:", e)

# -------------------------------------
# UI behavior helpers
# -------------------------------------

def open_folder_browser():
    chosen = filedialog.askdirectory()
    if chosen:
        dir_var.set(chosen)
        save_user_config()

def apply_placeholder(entry_widget):
    entry_widget.delete(0, tk.END)
    entry_widget.insert(0, PLACEHOLDER_TEXT)
    entry_widget.config(foreground=COLOR_PLACEHOLDER)

def handle_focus_in(_):
    if name_entry.get() == PLACEHOLDER_TEXT:
        name_entry.delete(0, tk.END)
        name_entry.config(foreground=COLOR_NORMAL)

def handle_focus_out(_):
    if not name_entry.get().strip():
        apply_placeholder(name_entry)

# -------------------------------------
# Actual save logic
# -------------------------------------

def save_image_from_clipboard(event=None):
    folder_path = dir_var.get().strip()
    file_ext = ext_var.get()
    name_input = name_var.get().strip()

    if name_input == PLACEHOLDER_TEXT:
        name_input = ""

    # If no folder set, use default
    if not folder_path:
        folder_path = str(DEFAULT_IMAGE_DIR)
        dir_var.set(folder_path)

    # Try to fetch an image from clipboard
    img_clip = ImageGrab.grabclipboard()
    if img_clip is None:
        messagebox.showerror("Oops!", "Clipboard doesn't contain an image.")
        return

    # If no name provided, timestamp it
    if not name_input:
        name_input = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    full_file_path = Path(folder_path) / f"{name_input}.{file_ext}"

    try:
        # JPG needs conversion to RGB — learned this the hard way
        if file_ext == "jpg":
            img_clip = img_clip.convert("RGB")
            img_clip.save(full_file_path, "JPEG", quality=95)
        else:
            img_clip.save(full_file_path, "PNG")  # Default to PNG

        save_user_config()

        if not silent_var.get():
            messagebox.showinfo("Saved", f"Image saved to:\n{full_file_path}")

    except Exception as e:
        messagebox.showerror("Save failed", str(e))

# -------------------------------------
# Setup GUI
# -------------------------------------

root = tk.Tk()
root.title("Clipboard Image Saver")
root.resizable(False, False)

# --- ICONS (had some issues with icon loading on other OS) ---
try:
    if ICON_PNG_PATH.exists():
        root._icon_image = tk.PhotoImage(file=str(ICON_PNG_PATH))  # Hold a reference
        root.iconphoto(True, root._icon_image)

    if ICON_ICO_PATH.exists():
        root.iconbitmap(default=str(ICON_ICO_PATH))
except Exception as e:
    print("Icon load failed:", e)

padding_opts = {"padx": 10, "pady": 5}

# Shared UI state
dir_var = tk.StringVar()
name_var = tk.StringVar()
ext_var = tk.StringVar(value="png")
silent_var = tk.BooleanVar(value=False)

# Load any existing settings
settings = load_user_config()
dir_var.set(settings.get("directory", str(DEFAULT_IMAGE_DIR)))
ext_var.set(settings.get("extension", "png"))
silent_var.set(settings.get("silent_save", False))

# --- UI Layout ---
ttk.Label(root, text="Directory").grid(row=0, column=0, sticky="w", **padding_opts)
ttk.Entry(root, textvariable=dir_var, width=40).grid(row=0, column=1, **padding_opts)
ttk.Button(root, text="Browse", command=open_folder_browser).grid(row=0, column=2, **padding_opts)

ttk.Label(root, text="File name").grid(row=1, column=0, sticky="w", **padding_opts)
name_entry = ttk.Entry(root, textvariable=name_var, width=40)
name_entry.grid(row=1, column=1, columnspan=2, sticky="w", **padding_opts)

apply_placeholder(name_entry)
name_entry.bind("<FocusIn>", handle_focus_in)
name_entry.bind("<FocusOut>", handle_focus_out)

ttk.Label(root, text="Extension").grid(row=2, column=0, sticky="w", **padding_opts)
ttk.Combobox(
    root,
    textvariable=ext_var,
    values=["png", "jpg"],
    state="readonly",
    width=10,
).grid(row=2, column=1, sticky="w", **padding_opts)

ttk.Checkbutton(
    root,
    text="Silent save (no success popup)",
    variable=silent_var,
    command=save_user_config,
).grid(row=3, column=1, sticky="w", **padding_opts)

save_btn = ttk.Button(
    root,
    text="Save (Ctrl + S)",
    command=save_image_from_clipboard,
)
save_btn.grid(row=4, column=0, columnspan=3, pady=15)

# Keyboard shortcut for saving
root.bind("<Control-s>", save_image_from_clipboard)
root.bind("<Control-S>", save_image_from_clipboard)

# Final sizing
root.update_idletasks()
root.minsize(root.winfo_width(), root.winfo_height())

root.mainloop()
