import tkinter as tk
import requests
import os
import sys
from tkinter import messagebox, OptionMenu
from threading import Thread
from PIL import Image, ImageTk
import subprocess

def rp(relative_path):
    try:
        bp = sys._MEIPASS
    except:
        bp = os.path.abspath(".")
    return os.path.join(bp, relative_path)

class LazyOSINTApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LazyOSINT")
        self.geometry("320x375")
        self.configure(bg="whitesmoke")
        self.resizable(False, False)
        self.init_components()

    def init_components(self):
        img = Image.open(rp("a.png")).resize((280, 150), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        tk.Label(self, image=self.photo).pack(padx=10, pady=10)

        tk.Label(self, text="Please enter a domain or username:", font=("Arial", 10, "bold")).pack()
        self.text_box = tk.Entry(self, font=("Arial", 10))
        self.text_box.pack(padx=10, pady=10)

        self.selected_option = tk.StringVar(self)
        self.selected_option.set("Domain")
        self.combo_box = OptionMenu(self, self.selected_option, "Domain", "Username")
        self.combo_box.config(font=("Arial", 10))
        self.combo_box.pack(padx=10, pady=10)

        bf = tk.Frame(self)
        bf.pack(pady=10)

        tk.Button(bf, text="OK", font=("Arial", 10), bg="LightGray", command=self.ok_button_click).pack(side=tk.LEFT, padx=10)
        tk.Button(bf, text="Cancel", font=("Arial", 10), bg="LightGray", command=self.destroy).pack(side=tk.LEFT, padx=10)

        tk.Label(self, text="Developed by Robot©", font=("Arial", 8), fg="gray").pack(side=tk.BOTTOM, pady=10)

    def ok_button_click(self):
        input_text = self.text_box.get().strip()
        selected_type = self.combo_box.cget("text")
        if not input_text:
            messagebox.showwarning("Input Required", "Please enter a domain or username.")
            return
        self.process_data(input_text, selected_type)

    def fetch_urls(self, filename):
        return requests.get(f"https://raw.githubusercontent.com/pentestfunctions/WindowsLazyOsint/main/{filename}.txt").text.splitlines()

    def process_data(self, data, data_type):
        def task(filename, placeholder):
            urls = self.fetch_urls(filename)
            for url_template in urls:
                url = url_template.replace(placeholder, data)
                # Use subprocess to open the default web browser
                subprocess.Popen(["xdg-open", url])
        Thread(target=task, args=(data_type + "s", "$" + data_type.lower())).start()

if __name__ == "__main__":
    app = LazyOSINTApp()
    app.mainloop()
