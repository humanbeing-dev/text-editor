"""Python Tkinter GUI Tutorial
#104 Build a Text Editor
#105 Open and Save as File
#106 Save files
#107 Cut Copy Paste
#108 Undo Redo and Horizontal Scrollbar
#109 Creating bold and italic
#110 Change text colors
#111 Print a file - not implemented
#112 Select all and clear
#115 Night Mode
"""
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import colorchooser

import pathlib
import os


class TextEditor(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("ProMCS - TextEditor")
        self.master.geometry("600x700")

        # Create toolbar frame
        self.toolbar_frame = Frame(self.master)
        self.toolbar_frame.pack(fill=X)

        # Create main frame
        self.main_frame = Frame(
            master=self.master,
        )
        self.main_frame.pack(fill=BOTH, expand=1)

        ## Create scroll button
        self.scrolly = Scrollbar(self.main_frame)
        self.scrolly.pack(fill=Y, side=RIGHT)

        self.scrollx = Scrollbar(self.main_frame, orient=HORIZONTAL)
        self.scrollx.pack(fill=X, side=BOTTOM)

        ## Create multiline text box
        self.editor = Text(
            master=self.main_frame,
            font="Arial",
            selectbackground="yellow",
            selectforeground="black",
            undo=True,
            yscrollcommand=self.scrolly.set,
            xscrollcommand=self.scrollx.set,
            wrap="none",
        )
        self.editor.pack(fill=Y, expand=1, side=LEFT)

        ## Config scroll
        self.scrolly.config(command=self.editor.yview)
        self.scrollx.config(command=self.editor.xview)

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
        self.file_menu.add_command(label="Print", command=self.print_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.destroy)

        ## Set edit menu labels
        self.edit_menu = Menu(self.main_menu, tearoff=False)
        self.edit_menu.add_command(
            label="Cut", command=lambda: self.cut_text(False), accelerator="(ctrl+x)"
        )
        self.edit_menu.add_command(
            label="Copy", command=lambda: self.copy_text(False), accelerator="(ctrl+c)"
        )
        self.edit_menu.add_command(
            label="Paste",
            command=lambda: self.paste_text(False),
            accelerator="(ctrl+v)",
        )
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Change all text color",
            command=self.change_editor_text_color,
            accelerator="(ctrl+v)",
        )
        self.edit_menu.add_command(
            label="Change background color",
            command=self.change_background_color,
            accelerator="(ctrl+v)",
        )
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Undo", command=self.editor.edit_undo, accelerator="(ctrl+z)"
        )
        self.edit_menu.add_command(
            label="Redo", command=self.editor.edit_redo, accelerator="(ctrl+y)"
        )
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Select all", command=lambda: self.select_all(True), accelerator="(ctrl+a)"
        )
        self.edit_menu.add_command(
            label="Clear all", command=self.clear_all
        )

        ## Set file menu labels
        self.options_menu = Menu(self.main_menu, tearoff=False)
        self.options_menu.add_command(label="Night Mode", command=self.night_mode)
        self.options_menu.add_command(label="Day Mode", command=self.day_mode)

        ## Add file and edit menu to main menu
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.main_menu.add_cascade(label="Options", menu=self.options_menu)

        ## Add status bar to the bottom of an App
        self.status_bar = Label(master=self.master, text="Ready")
        self.status_bar.pack(side=BOTTOM, anchor=E, ipadx=20)

        # Create toolbars buttons
        self.bold_button = Button(self.toolbar_frame, text="Bold", command=self.bold_it)
        self.bold_button.grid(row=0, column=0, sticky=W)
        self.italic_button = Button(
            self.toolbar_frame, text="Italics", command=self.italics_it
        )
        self.italic_button.grid(row=0, column=1, sticky=W)
        self.undo_button = Button(
            self.toolbar_frame, text="Undo", command=self.editor.edit_undo
        )
        self.undo_button.grid(row=0, column=2, sticky=W)
        self.redo_button = Button(
            self.toolbar_frame, text="Redo", command=self.editor.edit_redo
        )
        self.redo_button.grid(row=0, column=3, sticky=W)
        self.color_button = Button(
            self.toolbar_frame, text="Text color", command=self.change_selected_text_color
        )
        self.color_button.grid(row=0, column=4, sticky=W)

        # Handling saved file
        self.selected = ""
        self.saved = False
        self.saved_name = ""

        # Edit bindings
        self.master.bind("<Control-x>", self.cut_text)
        self.master.bind("<Control-c>", self.copy_text)
        self.master.bind("<Control-v>", self.paste_text)
        self.master.bind("<Control-a>", self.select_all)

    @staticmethod
    def get_file_to_load():
        options = dict(
            initialdir=pathlib.Path().absolute(),
            title="Choose file to load",
            filetypes=(
                ("txt files", "*.txt"),
                ("html files", "*.html"),
                ("python files", "*.py"),
                ("all files", "*"),
            ),
        )
        return filedialog.askopenfilename(**options)

    @staticmethod
    def get_path_to_save():
        options = dict(
            defaultextension=".*",
            initialdir=pathlib.Path().absolute(),
            title="Choose file to save",
            filetypes=(
                ("txt files", "*.txt"),
                ("html files", "*.html"),
                ("python files", "*.py"),
                ("all files", "*"),
            ),
        )
        return filedialog.asksaveasfilename(**options)

    def new_file(self):
        self.saved = False
        self.saved_name = ""
        self.editor.delete(1.0, END)
        self.master.title("New File - TextEditor")
        self.status_bar.config(text="New File")

    def open_file(self):
        self.editor.delete(1.0, END)
        file = self.get_file_to_load()
        if file:
            self.saved = True
            self.saved_name = file
            self.status_bar.config(text=file)
            self.master.title(f"{os.path.basename(file)} - TextEditor")
            with open(file, "r") as f:
                self.editor.insert(1.0, f.read())

    def save_file(self):
        if self.saved_name:
            with open(self.saved_name, "w") as f:
                f.write(self.editor.get(1.0, END))
        else:
            self.save_as_file()

    def save_as_file(self):
        file = self.get_path_to_save()
        if file:
            self.saved = True
            self.saved_name = file
            self.status_bar.config(text=file)
            self.master.title(f"Saved: {os.path.basename(file)} - TextEditor")
            with open(file, "w") as f:
                f.write(self.editor.get(1.0, END))

    def cut_text(self, e):
        if e:
            self.selected = self.master.clipboard_get()
        else:
            if self.editor.selection_get():
                self.selected = self.editor.selection_get()
                self.editor.delete("sel.first", "sel.last")
                self.master.clipboard_clear()
                self.master.clipboard_append(self.selected)

    def copy_text(self, e):
        if e:
            self.selected = self.master.clipboard_get()

        if self.editor.selection_get():
            self.selected = self.editor.selection_get()
            self.master.clipboard_clear()
            self.master.clipboard_append(self.selected)

    def paste_text(self, e):
        if e:
            self.selected = self.master.clipboard_get()
        else:
            if self.selected:
                position = self.editor.index(INSERT)
                self.editor.insert(position, self.selected)

    def bold_it(self):
        """Make selected text bold"""
        bold_font = font.Font(self.editor, self.editor.cget("font"))
        bold_font.configure(weight="bold")
        self.editor.tag_config("bold", font=bold_font)
        current_tags = self.editor.tag_names("sel.first")

        if "bold" in current_tags:
            self.editor.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.editor.tag_add("bold", "sel.first", "sel.last")

    def italics_it(self):
        """Make selected text italic"""
        italic_font = font.Font(self.editor, self.editor.cget("font"))
        italic_font.configure(slant="italic")
        self.editor.tag_config("italic", font=italic_font)
        current_tags = self.editor.tag_names("sel.first")

        if "italic" in current_tags:
            self.editor.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.editor.tag_add("italic", "sel.first", "sel.last")

    @staticmethod
    def pick_color():
        return colorchooser.askcolor()[1]

    def change_background_color(self):
        """Change color of the background"""
        my_color = self.pick_color()
        self.editor.config(background=my_color)

    def change_editor_text_color(self):
        """Change color of the entire text"""
        my_color = self.pick_color()
        self.editor.config(foreground=my_color)

    def change_selected_text_color(self):
        """Change color of the selected text"""
        # Pick color
        my_color = self.pick_color()

        if my_color:
            color_font = font.Font(self.editor, self.editor.cget("font"))
            self.editor.tag_config("colored", font=color_font, foreground=my_color)
            current_tags = self.editor.tag_names("sel.first")

            if "colored" in current_tags:
                self.editor.tag_remove("colored", "sel.first", "sel.last")
            else:
                self.editor.tag_add("colored", "sel.first", "sel.last")

    def select_all(self, e):
        self.editor.tag_add(SEL, 1.0, END)

    def clear_all(self):
        self.editor.delete(1.0, END)

    def print_file(self):
        ...

    def night_mode(self):
        second_color = "#373737"
        bg_color = "#585858"
        text_color = "white"
        self.master.config(bg=second_color)
        self.status_bar.config(fg=text_color, bg=second_color)
        self.editor.config(bg=bg_color, fg=text_color, selectbackground="blue", selectforeground=text_color)
        self.toolbar_frame.config(bg=second_color)
        for child in self.toolbar_frame.winfo_children():
            child.config(bg=second_color, fg=text_color)
        for child in self.main_menu.winfo_children():
            child.config(bg=second_color, fg=text_color)
        self.main_menu.config(bg=bg_color, fg=text_color)

    def day_mode(self):
        second_color = "gray"
        bg_color = "white"
        text_color = "black"
        self.master.config(bg=second_color)
        self.status_bar.config(fg=text_color, bg=second_color)
        self.editor.config(bg=bg_color, fg=text_color, selectbackground="yellow", selectforeground=text_color)
        self.toolbar_frame.config(bg=second_color)
        for child in self.toolbar_frame.winfo_children():
            child.config(bg=second_color, fg=text_color)
        for child in self.main_menu.winfo_children():
            child.config(bg=second_color, fg=text_color)
        self.main_menu.config(bg=bg_color, fg=text_color)


if __name__ == "__main__":
    root = Tk()
    app = TextEditor(master=root)
    app.mainloop()
