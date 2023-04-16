import tkinter as tk
from tkinter import HORIZONTAL, filedialog as fd
from PIL import Image


def open_file():
    filetypes = (("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*"))
    filepath = fd.askopenfilename(filetypes=filetypes)
    if filepath:
        image = Image.open(filepath).convert('RGBA')
        alpha = Image.new('L', image.size, 255)
        image.putalpha(alpha)
        return image


class PopupWindowImageInput:
    def __init__(self, parent):
        self.parent = parent

        # Create the popup window on top of main window
        self.window = tk.Toplevel(parent.window)
        self.window.title("Add Watermark as image")

        tk.Label(self.window, text="Watermark Image:").grid(row=0, column=0, padx=5, pady=5)
        self.image_entry = tk.Button(self.window, text='Choose Image', command=self.choose_logo)
        self.image_entry.grid(row=0, column=1, padx=5, pady=0)

        # size
        tk.Label(self.window, text="Image Size: ").grid(row=1, column=0, padx=5, pady=5)
        v2 = tk.StringVar(self.window, value=self.parent.size)
        self.size_entry = tk.Entry(self.window, textvariable=v2)
        self.size_entry.grid(row=1, column=1, padx=5, pady=5)

        # opacity
        tk.Label(self.window, text="Image Opacity:").grid(row=2, column=0, padx=5, pady=5)
        self.opacity_entry = tk.Scale(self.window, from_=0, to=100, orient=HORIZONTAL)
        self.opacity_entry.grid(row=2, column=1, padx=5, pady=5)

        # rotation
        # tk.Label(self.window, text="Image Rotation:").grid(row=3, column=0, padx=5, pady=5)
        # self.rotation_entry = tk.Scale(self.window, from_=0, to=360, orient=HORIZONTAL)
        # self.rotation_entry.grid(row=3, column=1, padx=5, pady=5)

        # save button
        tk.Button(self.window, text='Save', command=self.save_properties).grid(row=4, column=0, padx=5, pady=5,
                                                                               columnspan=2)

    def choose_logo(self):
        logo = open_file()
        self.parent.logo = logo

    def save_properties(self):
        size = int(self.size_entry.get())
        opacity = int(self.opacity_entry.get())
        # rotation = int(self.rotation_entry.get())

        # pass properties to parent
        self.parent.save_image_input(size, opacity)
        # close window
        self.window.destroy()
