import tkinter as tk
from tkinter import HORIZONTAL
from PIL import Image, ImageTk, ImageFont, ImageDraw
import os
import io


class PopupWindowTextInput:
    def __init__(self, parent):
        self.parent = parent

        # Create the popup window on top of main window
        self.window = tk.Toplevel(parent.window)
        self.window.title("Add Watermark as text")

        # Label and entry widgets for the properties
        tk.Label(self.window, text="Text:").grid(row=0, column=0, padx=5, pady=5)
        self.text_entry = tk.Entry(self.window)
        self.text_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Color:").grid(row=1, column=0, padx=5, pady=5)
        self.color_entry = tk.Entry(self.window)
        self.color_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Size:").grid(row=1, column=0, padx=5, pady=5)
        self.size_entry = tk.Entry(self.window)
        self.size_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.window, text="Opacity:").grid(row=2, column=0, padx=5, pady=5)
        self.opacity_entry = tk.Scale(self.window, from_=0, to=100, orient=HORIZONTAL)
        self.opacity_entry.grid(row=3, column=1, padx=5, pady=5)

        # Button to save the properties and close the window
        tk.Button(self.window, text="Save", command=self.save_properties).grid(row=4, column=0, columnspan=2, padx=5,
                                                                               pady=5)

    def save_properties(self):
        # Get the properties entered by the user
        text = str(self.text_entry.get())
        color = str(self.color_entry.get())
        size = int(self.size_entry.get())
        opacity = int(self.opacity_entry.get())

        # Pass the properties back to the parent window
        self.parent.set_properties(text, color, size, opacity)

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
        self.image_on_canvas = None
        self.background_image = None
        self.canvas = None
        # later we can modify bg image with our logo/watermark
        self.original_image = None
        self.window = window
        self.window.title("Main Window")
        self.set_background()
        self.create_canvas()

        # Button to open the popup window
        popup_button_text = tk.Button(self.window, text="Add Watermark as text", command=self.popup_window_text)
        popup_button_text.grid(row=1, column=0, padx=10, pady=10)

        # Button to open the popup window
        popup_button_image = tk.Button(self.window, text="Add Watermark as image", command=self.popup_window_image)
        popup_button_image.grid(row=1, column=1, padx=10, pady=10)

        # Label to display the current properties
        self.properties_label = tk.Label(self.window, text="No properties set")
        self.properties_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def popup_window_text(self):
        # Create a new instance of the popup window
        self.popup = PopupWindowTextInput(self)

    def popup_window_image(self):
        # Create a new instance of the popup window
        self.popup = PopupWindowImageInput(self)

    def set_properties(self, text, color, size, opacity):
        # Update the properties label with the new values
        self.properties_label.config(text=f"Width: {text}\nHeight: {color}\nColor: {size}")

        # Get the dimensions of the background image
        # width = self.background_image.width()
        # height = self.background_image.height()
        # # text Watermark
        # watermark = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        #
        # # set the font and text for the watermark img
        # font = ImageFont.truetype('arial.ttf', size=size)
        #
        # # Set the fill color and opacity
        # fill_color = (255, 255, 255)  # white text
        # opacity = int((100 - int(opacity)) * 2.55)  # Convert 0-100 opacity to 0-255 alpha value
        #
        # # Draw the text on the watermark image
        # draw = ImageDraw.Draw(watermark)
        # text_bbox = draw.textbbox((0, 0), text, font=font)
        # x = (watermark.width - text_bbox[2]) / 2
        # y = (watermark.height - text_bbox[3]) / 2
        # draw.text((x, y), text, font=font, fill=(fill_color[0], fill_color[1], fill_color[2], opacity))
        #
        # # Convert the PhotoImage object to a PIL Image object
        # # pil_image = Image.open(io.BytesIO(self.background_image.getvalue()))
        # # pil_image = Image.fromarray(self.background_image)
        # print(type(self.background_image))
        # print(type(self.original_image))
        # print(type(watermark))
        # # print(type(pil_image))
        # # Blend the watermark with the original image
        # result = Image.alpha_composite(self.original_image, watermark)

        # Convert the result image back to a PhotoImage object
        # image = Image.open('./logo/ss.png')
        # image.resize((800, 600))
        # watermarked_image = ImageTk.PhotoImage(image)
        # self.canvas.itemconfigure(self.image_on_canvas, image=watermarked_image)
        self.change_image()
    def change_image(self):
        image = Image.open('./logo/ss.png')
        image.resize((800, 600))
        watermarked_image = ImageTk.PhotoImage(image)
        print(self.background_image)
        print(watermarked_image)
        self.canvas.itemconfigure(self.image_on_canvas, image=watermarked_image)

    def set_background(self):
        # Load the first image from images directory - that way we don't need to change image name
        image_dir = '.\image'
        image_files = [f for f in os.listdir(image_dir) if f.endswith(".jgp") or f.endswith('.png')]
        if len(image_files) > 0:
            image_path = os.path.join(image_dir, image_files[0])
        else:
            # no image path
            image_path = None
        # load the image and create PhotoImage obj
        if image_path is not None:
            image = Image.open(image_path)
            # self.original_image = ImageTk.PhotoImage(image)
            self.original_image = image #shorten this later
        else:
            self.original_image = None

    def create_canvas(self):
        self.canvas = tk.Canvas(self.window, width=800, height=600)
        if self.original_image is not None:
            self.background_image = ImageTk.PhotoImage(self.original_image)
            self.image_on_canvas = self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')
        self.canvas.grid(row=0, column=0, columnspan=2, sticky='nesw')


# Create the tkinter window
window = tk.Tk()

# Create the MainWindow instance
app = AppWindow(window)

# Start the tkinter event loop
window.mainloop()

# make folder and inside you put in photo and another folder for logo?
