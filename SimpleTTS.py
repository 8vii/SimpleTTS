
 
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from gtts import gTTS
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 

LANGUAGE_CODES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
}
 
main = tk.Tk()
 
main.title("SimpleTTS")
main.config(bg="#dfdfdf")
main.geometry("700x345")
main.update_idletasks()
 
geometryX = 0
geometryY = 0
 
main.geometry("+%d+%d" % (geometryX, geometryY))
 
style = ttk.Style(main)
style.theme_use("clam")
 
 
style.configure("entry.TEntry", fieldbackground="#dfdfdf", foreground="#000000")
 
entry = ttk.Entry(master=main, style="entry.TEntry")
entry.place(x=6, y=82, width=686, height=48)
 
style.configure("title.TLabel", background="#d7d7d7", foreground="#6e6e6e", font=("TkTextFont", 15, "bold"), anchor="center")
title = ttk.Label(master=main, text="Simple TTS", style="title.TLabel")
title.configure(anchor="center")
title.place(x=5, y=25, width=685, height=44)
 
style.configure("language_option.TCombobox", fieldbackground="#e2e2e2", foreground="#6e6e6e", font=("TkHeadingFont", 13, ))
language_option_options = list(LANGUAGE_CODES.keys())
language_option_var = tk.StringVar(value="English")
language_option = ttk.Combobox(main, textvariable=language_option_var, values=language_option_options, style="language_option.TCombobox", state="readonly")
language_option.place(x=10, y=152, width=679, height=40)
 
style.configure("button.TButton", background="#ececec", foreground="#6e6e6e", relief=tk.FLAT, font=("TkFixedFont", 31, "bold"), cursor="arrow")
style.map("button.TButton", background=[("active", "#d9d9d9")], foreground=[("active", "#000")])
 
 
def generate():

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
 
    try:
        tts = gTTS(text=message, lang=lang_code, slow=False)
        tts.save(output_path)
    except Exception as error:
        messagebox.showerror("Simple TTS", f"Could not generate audio:\n{error}")
        return
 
    messagebox.showinfo("Simple TTS", f"Audio saved to:\n{output_path}")
 

    try:
        os.startfile(output_path)
    except Exception as error:
        messagebox.showwarning("Simple TTS", f"The file was saved, though it could not be opened automatically:\n{error}")
 
 
button = ttk.Button(master=main, text="Generate!", style="button.TButton", command=generate)
button.place(x=8, y=219, width=679, height=93)
 
main.mainloop()
 
