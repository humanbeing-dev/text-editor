"""Python Tkinter GUI Tutorial
#104 Build a Text Editor
#105 Open and Save as File
"""
from tkinter import *
from tkinter import filedialog
from tkinter import font
import pathlib, os


class TextEditor(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("ProMCS - TextEditor")
        self.master.geometry("600x700")

        # Create main menu
        self.main_menu = Menu(self.master)
        self.master.config(menu=self.main_menu)

        ## Set file menu labels
        self.file_menu = Menu(self.main_menu, tearoff=False)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.destroy)

        ## Set edit menu labels
        self.edit_menu = Menu(self.main_menu, tearoff=False)
        self.edit_menu.add_command(label="Cut", command=self.open_file)
        self.edit_menu.add_command(label="Copy", command=self.save_file)
        self.edit_menu.add_command(label="Paste", command=self.save_file)
        self.edit_menu.add_command(label="Undo", command=...)
        self.edit_menu.add_command(label="Redo", command=...)

        ## Add file and edit menu to main menu
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)

        ## Add status bar to the bottom of an App
        self.status_bar = Label(master=self.master, text="Ready")
        self.status_bar.pack(side=BOTTOM, anchor=E, ipadx=20)

        # Create main frame
        self.main_frame = Frame(
            master=self.master,
        )
        self.main_frame.pack(fill=BOTH, expand=1)

        ## Create scroll button
        self.scroll = Scrollbar(self.main_frame)
        self.scroll.pack(fill=Y, expand=1, side=RIGHT)

        ## Create multiline text box
        self.editor = Text(
            self.main_frame,
            font="Arial",
            selectbackground="yellow",
            selectforeground="black",
            undo=True,
            yscrollcommand=self.scroll.set
        )
        self.editor.pack(fill=Y, expand=1, side=LEFT)

        ## Config scroll
        self.scroll.config(command=self.editor.yview)

    @staticmethod
    def get_file_to_load():
        options = dict(
            initialdir=pathlib.Path().absolute(),
            title="Choose file to load",
            filetypes=(("txt files", "*.txt"),
                       ("html files", "*.html"),
                       ("python files", "*.py"),
                       ("all files", "*")),
        )
        return filedialog.askopenfilename(**options)

    @staticmethod
    def get_path_to_save():
        options = dict(
            defaultextension='.*',
            initialdir=pathlib.Path().absolute(),
            title="Choose file to save",
            filetypes=(("txt files", "*.txt"),
                       ("html files", "*.html"),
                       ("python files", "*.py"),
                       ("all files", "*")),
        )
        return filedialog.asksaveasfilename(**options)

    def new_file(self):
        self.editor.delete(1.0, END)
        self.master.title("New File - TextEditor")
        self.status_bar.config(text="New File")

    def open_file(self):
        self.editor.delete(1.0, END)
        file = self.get_file_to_load()
        if file:
            self.status_bar.config(text=file)
            self.master.title(f"{os.path.basename(file)} - TextEditor")
            with open(file, 'r') as f:
                self.editor.insert(1.0, f.read())

    def save_file(self):
        file = self.get_path_to_save()
        if file:
            with open(file, 'w') as f:
                f.write(self.editor.get(1.0, END))

    def save_as_file(self):
        file = self.get_path_to_save()
        if file:
            self.status_bar.config(text=file)
            self.master.title(f"Saved: {os.path.basename(file)} - TextEditor")
            with open(file, 'w') as f:
                f.write(self.editor.get(1.0, END))


if __name__ == "__main__":
    root = Tk()
    app = TextEditor(master=root)
    app.mainloop()
