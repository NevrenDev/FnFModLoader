import os
import shutil
import tkinter as tk
from tkinter import messagebox
import subprocess

class ModLoader:
    def __init__(self, root):
        self.root = root
        self.root.title("Friday Night Funkin' Mod Loader")
        self.root.geometry("600x400")
        self.set_background_image("background.png")
        self.root.iconbitmap("icon.ico")

        self.mods_dir = "mods"
        self.create_widgets()

    def set_background_image(self, image_path):
        self.bg_image = tk.PhotoImage(file=image_path)
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_widgets(self):
        frame = tk.Frame(self.root, bg='#282c34')
        frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

        self.mods_listbox = tk.Listbox(frame, bg="#2e2e2e", fg="#ffffff", font=("Helvetica", 12), selectbackground="#4e9af1", selectforeground="#ffffff")
        self.mods_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.load_button = tk.Button(frame, text="Load Mod", command=self.load_selected_mod, bg="#61afef", fg="#282c34", font=("Helvetica", 12), bd=0, relief=tk.FLAT)
        self.load_button.pack(side=tk.BOTTOM, padx=(0, 5), pady=(0, 5))
        self.load_button.config(width=10, height=2, borderwidth=0, highlightthickness=0, padx=20, pady=10)
        self.load_button.bind("<Enter>", self.on_enter)
        self.load_button.bind("<Leave>", self.on_leave)

        self.update_mods_list()

    def on_enter(self, event):
        self.load_button.config(bg="#4e9af1")

    def on_leave(self, event):
        self.load_button.config(bg="#61afef")

    def update_mods_list(self):
        self.mods_listbox.delete(0, tk.END)
        self.mods_listbox.insert(tk.END, "  is exe?   |    mod name")
        self.mods_listbox.insert(tk.END, "-------------------------------------------------------------------------------------------------")
        self.mods_listbox.itemconfig(0, {'bg': '#4e4e4e', 'fg': '#ffffff', 'selectbackground': '#4e4e4e'})

        mods = []
        for mod in os.listdir(self.mods_dir):
            mod_path = os.path.join(self.mods_dir, mod)
            if os.path.isdir(mod_path):
                has_exe = any(file.endswith(".exe") for file in os.listdir(mod_path))
                if has_exe:
                    mods.append((mod, "     [✔]          "))
                else:
                    mods.append((mod, "     [✖]          "))

        for mod, status in mods:
            self.mods_listbox.insert(tk.END, f"{status} {mod}")

    def load_selected_mod(self):
        selected_index = self.mods_listbox.curselection()
        if not selected_index or selected_index[0] < 2:
            messagebox.showerror("Error", "No mod selected!")
            return

        mod_item = self.mods_listbox.get(selected_index[0])
        mod_name = mod_item.split(" ", 1)[1]

        mod_path = os.path.join(self.mods_dir, mod_name)
        engine_mods_dir = os.path.join("engine", "mods")
        mod_engine_path = os.path.join(engine_mods_dir, mod_name)

        exe_found = False
        for file in os.listdir(mod_path):
            if file.endswith(".exe"):
                exe_found = True
                exe_path = os.path.join(mod_path, file)
                subprocess.run([exe_path], cwd=mod_path)
                break

        if not exe_found:
            try:
                shutil.rmtree(engine_mods_dir)
                os.makedirs(engine_mods_dir)
                shutil.copytree(mod_path, mod_engine_path, dirs_exist_ok=True)
                subprocess.Popen([os.path.join("engine", "PsychEngine.exe")], cwd='engine')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load mod '{mod_name}' to engine\\mods folder: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModLoader(root)
    root.mainloop()
