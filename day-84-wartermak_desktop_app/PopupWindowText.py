import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import HORIZONTAL, filedialog as fd


class PopupWindowTextInput:
    def __init__(self, parent):
        self.parent = parent

        # Create the popup window on top of main window
        self.window = tk.Toplevel(parent.window)
        self.window.title("Add Watermark as text")

        # Label and entry widgets for the properties
        tk.Label(self.window, text="Watermark Text: ").grid(row=0, column=0, padx=5, pady=5)
        v1 = tk.StringVar(self.window, value=self.parent.text)
        self.text_entry = tk.Entry(self.window, textvariable=v1)
        self.text_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Text Color: ").grid(row=1, column=0, padx=5, pady=5)
        self.color_entry = tk.Button(self.window, text='Select color', command=self.change_color)
        self.color_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Text Size: ").grid(row=2, column=0, padx=5, pady=5)
        v2 = tk.StringVar(self.window, value=self.parent.size)
        self.size_entry = tk.Entry(self.window, textvariable=v2)
        self.size_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Text Opacity: ").grid(row=3, column=0, padx=5, pady=5)
        self.opacity_entry = tk.Scale(self.window, from_=0, to=100, orient=HORIZONTAL)
        self.opacity_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Text Rotation: ").grid(row=4, column=0, padx=5, pady=5)
        self.rotation_entry = tk.Scale(self.window, from_=0, to=360, orient=HORIZONTAL)
        self.rotation_entry.grid(row=4, column=1, padx=5, pady=5)

        # Button to save the properties and close the window
        tk.Button(self.window, text="Save", command=self.save_properties).grid(row=5, column=0, columnspan=2, padx=5,
                                                                               pady=5)

    def change_color(self):
        color = askcolor(title="Tkinter Color Chooser")
        self.parent.color = color

    def save_properties(self):
        # Get the properties entered by the user
        text = str(self.text_entry.get())
        color = self.parent.color
        size = int(self.size_entry.get())
        opacity = int(self.opacity_entry.get())
        rotation = int(self.rotation_entry.get())

        # Pass the properties back to the parent window
        self.parent.save_text_input(text, color, size, opacity, rotation)

        # Close the popup window
        self.window.destroy()
