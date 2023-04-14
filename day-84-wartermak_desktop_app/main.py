import tkinter as tk
from tkinter import HORIZONTAL, filedialog as fd
from PIL import Image, ImageTk, ImageFont, ImageDraw
from tkinter.colorchooser import askcolor
from tkinter import messagebox
import os
import io
#

class PopupWindowTextInput:
    def __init__(self, parent):
        self.parent = parent

        # Create the popup window on top of main window
        self.window = tk.Toplevel(parent.window)
        self.window.title("Add Watermark as text")

        # Label and entry widgets for the properties
        tk.Label(self.window, text="Watermark Text: ").grid(row=0, column=0, padx=5, pady=5)
        v = tk.StringVar(self.window, value=self.parent.text)
        self.text_entry = tk.Entry(self.window, textvariable=v)
        self.text_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Text Color: ").grid(row=1, column=0, padx=5, pady=5)

        self.color_entry = tk.Button(self.window, text='Select color', command=self.change_color)
        self.color_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Text Size: ").grid(row=2, column=0, padx=5, pady=5)
        self.size_entry = tk.Entry(self.window)
        self.size_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Text Opacity: ").grid(row=3, column=0, padx=5, pady=5)
        self.opacity_entry = tk.Scale(self.window, from_=0, to=100, orient=HORIZONTAL)
        self.opacity_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Text Rotation: ").grid(row=4, column=0, padx=5, pady=5)
        self.rotation_entry = tk.Scale(self.window, from_=0, to=100, orient=HORIZONTAL)
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


class PopupWindowImageInput:
    def __init__(self, parent):
        self.parent = parent

        # Create the popup window on top of main window
        self.window = tk.Toplevel(parent.window)
        self.window.title("Add Watermark as image")

        tk.Label(self.window, text="Place your image inside logo folder and click save:").grid(row=0, column=0, padx=5,
                                                                                               pady=5)
        tk.Button(self.window, text='Save', command=...).grid(row=1, column=0, padx=5, pady=5)


class AppWindow:
    def __init__(self, window):

        self.original_image = None
        self.background_image = None
        self.canvas = None

        self.window = window
        self.window.title("Watermark App")
        self.set_background()
        self.create_canvas()

        # later we can modify bg image with our logo/watermark

        self.rotation = None
        self.text = None
        self.color = None
        self.size = None
        self.opacity = None

        # Button to open set user's image
        add_photo_button = tk.Button(self.window, text="Add Photo to watermark", command=self.change_image)
        add_photo_button.grid(row=1, column=0, padx=10, pady=10)

        # Button to open the popup window
        popup_button_text = tk.Button(self.window, text="Add Watermark as text", command=self.popup_window_text)
        popup_button_text.grid(row=1, column=1, padx=10, pady=10)

        # Button to open the popup window
        popup_button_image = tk.Button(self.window, text="Add Watermark as image", command=self.popup_window_image)
        popup_button_image.grid(row=1, column=2, padx=10, pady=10)
        #undo changes button
        #save file

        # Label to display the current properties
        self.properties_label = tk.Label(self.window, text="No properties set")
        self.properties_label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    @staticmethod
    def open_file():
        file_path = fd.askopenfile(mode='r', defaultextension="png",
                                   filetypes=[("jpeg", ".jpg"),
                                              ("png", ".png"),
                                              ("bitmap", "bmp"),
                                              ("gif", ".gif")])
        if file_path is not None:
            return Image.open(fr'{file_path.name}')

    @staticmethod
    def save_file():
        file_path = fd.asksaveasfilename(confirmoverwrite=True,
                                         defaultextension="png",
                                         filetypes=[("jpeg", ".jpg"),
                                                    ("png", ".png"),
                                                    ("bitmap", "bmp"),
                                                    ("gif", ".gif")])
        # if file_path is not None:  # if dialog not closed with "cancel".
        #     # Convert to RGB if saving as jpeg
        #     if os.path.splitext(file_path)[1] == ".jpg":
        #         image = image.convert("RGB")
        #     image.save(fp=file_path)

    @staticmethod
    def aspect_ratio(image):
        width, height = image.size
        if width > 900 or height > 600:
            ratio = min(900 / width, 600 / height)
            width = int(width * ratio)
            height = int(height * ratio)
        return width, height

    def set_background(self):
        image = Image.open('./image/Welcome_img.png')
        self.original_image = image

    def create_canvas(self):
        self.canvas = tk.Canvas(self.window, width=900, height=600)
        if self.original_image is not None:
            width, height = self.aspect_ratio(self.original_image)
            resized = self.original_image.resize((width, height))
            self.background_image = ImageTk.PhotoImage(resized)
            self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')
        self.canvas.grid(row=0, column=0, columnspan=3, sticky='nesw')
        self.c_text = self.canvas.create_text(400, 300, text="")

    def popup_window_text(self):
        # Create a new instance of the popup window
        if self.background_image is not None:
            self.popup = PopupWindowTextInput(self)
        else:
            messagebox.showerror('Error', 'Error: Image is not chosen!')

    def popup_window_image(self):
        # Create a new instance of the popup window
        if self.background_image is not None:
            self.popup = PopupWindowImageInput(self)
        else:
            messagebox.showerror('Error', 'Error: Image is not chosen!')

    def save_text_input(self, text, color, size, opacity, rotation):
        self.text = text  # that way user won't need to remember inputs if he wants to change anything
        self.color = color
        self.size = size
        self.opacity = opacity
        self.rotation = rotation
        self.properties_label.config(text=f"Watermark Text: {text}\nText Color: {color[1]}\nText Size: {size}"
                                          f"\nText Opacity:{opacity}Text Rotation: {rotation}")
        self.watermark()

    def watermark(self):
        watermark_image = self.original_image.copy()

        # create a new transparent RGBA image with the same size as the original image
        text = Image.new('RGBA', watermark_image.size, (255, 255, 255, 0))

        # create a draw object to draw on the text image
        draw = ImageDraw.Draw(text)

        # to draw on the middle
        w, h = watermark_image.size
        x, y = int(w / 2), int(h / 2)

        font = ImageFont.truetype("arial.ttf", int(self.size))

        # add watermark na większym obrazku rysujemy a potem go docinamy żeby się zmieścił w okienko
        self.opacity = round((100 - int(self.opacity)) * 2.55)  # Convert 0-100 opacity to 0-255 alpha value
        fill = self.color[0] + (self.opacity,)
        rounded_fill = tuple(round(val) for val in fill)

        # draw the text on the text image
        draw.text((x, y), f"{self.text}", fill=rounded_fill, font=font, anchor='mm')

        # rotate the text image
        text = text.rotate(self.rotation, expand=True)

        # resize the text image to match the size of the original image
        text = text.resize(watermark_image.size)

        # blend the text image with the original image using alpha_composite
        out = Image.alpha_composite(watermark_image, text)

        # resize the watermarked image to fit the canvas
        width, height = self.aspect_ratio(out)
        resized = out.resize((width, height))

        # update the background image on the canvas
        self.background_image = ImageTk.PhotoImage(resized)
        self.canvas.delete('all')
        self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')

    def change_image(self):
        self.background_image = self.open_file()
        if self.background_image is not None:

            self.canvas.delete('all')
            self.canvas.itemconfigure(self.c_text, text='Hi')
            width, height = self.aspect_ratio(self.background_image)
            resized = self.background_image.resize((width, height))
            self.original_image = self.background_image
            self.background_image = ImageTk.PhotoImage(resized)
            self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')
            # that way we can always go back to original image after failed watermark

        else:
            self.c_text = self.canvas.create_text(450, 300, text="Image not chosen", font=('Arial', 30, "bold"))





# Create the tkinter window
window = tk.Tk()

# Create the MainWindow instance
app = AppWindow(window)

# Start the tkinter event loop
window.mainloop()

# make folder and inside you put in photo and another folder for logo?
