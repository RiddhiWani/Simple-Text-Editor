import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

current_font_size = 12

def new_file():
    text.delete(1.0, tk.END)

def open_file():
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text.get(1.0, tk.END))
        messagebox.showinfo("Info", "File saved successfully!")

def change_font_size(increase=True):
    global current_font_size
    current_font_size = max(6, current_font_size + 2) if increase else current_font_size - 2
    text.config(font=("Helvetica", current_font_size))

def undo_redo(action):
    try:
        getattr(text, f"edit_{action}")()
    except tk.TclError:
        pass

def highlight_word():
    word = simpledialog.askstring("Highlight Word", "Enter word to highlight:")
    if word:
        text.tag_remove('highlight', '1.0', tk.END)
        start_pos = '1.0'
        while start_pos := text.search(word, start_pos, stopindex=tk.END, nocase=True):
            end_pos = f"{start_pos}+{len(word)}c"
            text.tag_add('highlight', start_pos, end_pos)
            start_pos = end_pos
        text.tag_config('highlight', background='yellow')

def show_counts():
    content = text.get(1.0, tk.END)
    words, chars = len(content.split()), len(content) - 1
    messagebox.showinfo("Word and Character Count", f"Words: {words}\nCharacters: {chars}")

def find_replace(action):
    text_content = text.get(1.0, tk.END)
    find_str = simpledialog.askstring("Find" if action == 'Find' else "Replace", "Enter text to find:")

    if find_str:
        if action == 'Replace':
            replace_str = simpledialog.askstring("Replace", "Enter replacement text:")
            text_content = text_content.replace(find_str, replace_str)
        start_pos = '1.0'
        while start_pos := text.search(find_str, start_pos, stopindex=tk.END):
            end_pos = f"{start_pos}+{len(find_str)}c"
            text.tag_add('highlight', start_pos, end_pos)
            start_pos = end_pos
        text.delete(1.0, tk.END)
        text.insert(tk.END, text_content)
        text.tag_config('highlight', background='yellow')

def change_case(to_upper=True):
    selected_text = text.get(tk.SEL_FIRST, tk.SEL_LAST)
    text.delete(tk.SEL_FIRST, tk.SEL_LAST)
    text.insert(tk.INSERT, selected_text.upper() if to_upper else selected_text.lower())

root = tk.Tk()
root.title("Smart Text Editor")
root.geometry("800x600")

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

edit_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=lambda: undo_redo('undo'), accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo", command=lambda: undo_redo('redo'), accelerator="Ctrl+Y")
edit_menu.add_separator()
edit_menu.add_command(label="Copy", command=lambda: text.event_generate("<<Copy>>"), accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=lambda: text.event_generate("<<Paste>>"), accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="Increase Font", command=lambda: change_font_size(True))
edit_menu.add_command(label="Decrease Font", command=lambda: change_font_size(False))
edit_menu.add_separator()
edit_menu.add_command(label="Highlight Word", command=highlight_word, accelerator="Ctrl+H")
edit_menu.add_separator()
edit_menu.add_command(label="Word/Character Count", command=show_counts)
edit_menu.add_command(label="Find", command=lambda: find_replace('Find'), accelerator="Ctrl+F")
edit_menu.add_command(label="Replace", command=lambda: find_replace('Replace'), accelerator="Ctrl+R")
edit_menu.add_command(label="To Uppercase", command=lambda: change_case(True))
edit_menu.add_command(label="To Lowercase", command=lambda: change_case(False))

text = tk.Text(root, wrap=tk.WORD, font=("Helvetica", current_font_size), undo=True)
text.pack(expand=tk.YES, fill=tk.BOTH)

# Bind keyboard shortcuts
root.bind("<Control-n>", lambda e: new_file())
root.bind("<Control-o>", lambda e: open_file())
root.bind("<Control-s>", lambda e: save_file())
root.bind("<Control-z>", lambda e: undo_redo('undo'))
root.bind("<Control-y>", lambda e: undo_redo('redo'))
root.bind("<Control-c>", lambda e: text.event_generate("<<Copy>>"))
root.bind("<Control-v>", lambda e: text.event_generate("<<Paste>>"))
root.bind("<Control-h>", lambda e: highlight_word())
root.bind("<Control-f>", lambda e: find_replace('Find'))
root.bind("<Control-r>", lambda e: find_replace('Replace'))
root.bind("<Control-u>", lambda e: change_case(True))
root.bind("<Control-l>", lambda e: change_case(False))

root.mainloop()