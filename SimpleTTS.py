import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from gtts import gTTS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LANGUAGE_CODES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
}

FONT_FAMILY = "Segoe UI" if sys.platform == "win32" else "Helvetica"

main = tk.Tk()
main.title("SimpleTTS")
main.config(bg="#dfdfdf")
main.resizable(False, False)

width, height = 700, 345
x = (main.winfo_screenwidth() - width) // 2
y = (main.winfo_screenheight() - height) // 2
main.geometry(f"{width}x{height}+{x}+{y}")

style = ttk.Style(main)
style.theme_use("clam")

style.configure("entry.TEntry", fieldbackground="#dfdfdf", foreground="#000000")
entry = ttk.Entry(master=main, style="entry.TEntry", font=(FONT_FAMILY, 14))
entry.place(x=6, y=82, width=686, height=48)
entry.focus_set()

style.configure("title.TLabel", background="#d7d7d7", foreground="#6e6e6e",
                font=(FONT_FAMILY, 15, "bold"), anchor="center")
title = ttk.Label(master=main, text="Simple TTS", style="title.TLabel")
title.place(x=5, y=25, width=685, height=44)

style.configure("language_option.TCombobox", fieldbackground="#e2e2e2", foreground="#6e6e6e")
language_option_var = tk.StringVar(value="English")
language_option = ttk.Combobox(
    main,
    textvariable=language_option_var,
    values=list(LANGUAGE_CODES.keys()),
    style="language_option.TCombobox",
    state="readonly",
    font=(FONT_FAMILY, 13),
)
language_option.place(x=10, y=152, width=679, height=40)

style.configure("button.TButton", background="#ececec", foreground="#6e6e6e",
                relief=tk.FLAT, font=(FONT_FAMILY, 24, "bold"))
style.map("button.TButton",
          background=[("disabled", "#e4e4e4"), ("active", "#d9d9d9")],
          foreground=[("disabled", "#a0a0a0"), ("active", "#000000")])


def open_file(path):
    if sys.platform == "win32":
        os.startfile(path)
    elif sys.platform == "darwin":
        subprocess.run(["open", path], check=True)
    else:
        subprocess.run(["xdg-open", path], check=True)


def _worker(message, lang_code, output_path):
    try:
        gTTS(text=message, lang=lang_code, slow=False).save(output_path)
    except Exception as exc:
        err = exc
        main.after(0, lambda: on_done(error=err))
        return
    main.after(0, lambda: on_done(path=output_path))


def on_done(path=None, error=None):
    button.config(state="normal", text="Generate!")

    if error:
        messagebox.showerror("Simple TTS", f"Could not generate audio:\n{error}")
        return

    messagebox.showinfo("Simple TTS", f"Audio saved to:\n{path}")
    try:
        open_file(path)
    except Exception as error:
        messagebox.showwarning(
            "Simple TTS",
            f"The file was saved, but could not be opened automatically:\n{error}",
        )


def generate(event=None):
    message = entry.get().strip()
    lang_code = LANGUAGE_CODES[language_option_var.get()]

    if not message:
        messagebox.showwarning("Simple TTS", "Please type some text first.")
        return

    output_path = filedialog.asksaveasfilename(
        title="Choose export location",
        initialdir=BASE_DIR,
        initialfile="output.mp3",
        defaultextension=".mp3",
        filetypes=[("MP3 audio", "*.mp3")],
    )
    if not output_path:
        return

    button.config(state="disabled", text="Generating...")
    threading.Thread(target=_worker, args=(message, lang_code, output_path), daemon=True).start()


button = ttk.Button(master=main, text="Generate!", style="button.TButton",
                    command=generate, cursor="arrow")
button.place(x=8, y=219, width=679, height=93)

entry.bind("<Return>", generate)

main.mainloop()
