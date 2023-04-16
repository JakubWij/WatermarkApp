from PopupWindowText import PopupWindowTextInput
from PopupWindowImage import PopupWindowImageInput
from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as messagebox
import numpy as np


def open_file():
    file_path = fd.askopenfile(mode='r', defaultextension="png",
                               filetypes=[("jpeg", ".jpg"),
                                          ("png", ".png"),
                                          ("bitmap", "bmp"),
                                          ("gif", ".gif")])
    if file_path is not None:
        return Image.open(fr'{file_path.name}')


class AppWindow:
    def __init__(self, window):
        self.original_image = None
        self.background_image = None
        self.canvas = None
        self.logo = None
        self.mode = None

        self.window = window
        self.window.title("Watermark App")
        self.set_background()
        self.create_canvas()

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

        # save file
        save_button = tk.Button(self.window, text="Save Watermark Image", command=self.save_file)
        save_button.grid(row=2, column=0, padx=10, pady=10, columnspan=3)

        # Label to display the current properties
        self.properties_label = tk.Label(self.window, text="No properties set")
        self.properties_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    @staticmethod
    def aspect_ratio(image):
        width, height = image.size
        if width > 900 or height > 600:
            ratio = min(900 / width, 600 / height)
            width = int(width * ratio)
            height = int(height * ratio)
        return width, height

    def save_file(self):
        if self.background_image is not None:
            file_path = fd.asksaveasfilename(confirmoverwrite=True,
                                             defaultextension="png",
                                             filetypes=[("png", ".png"),
                                                        ("bitmap", "bmp"),
                                                        ("gif", ".gif")])
            if file_path is not None:  # if dialog not closed with "cancel".
                # Convert to PIL Image object
                pil_image = ImageTk.getimage(self.background_image)
                # Convert to numpy array
                np_image = np.array(pil_image)
                # Save file
                Image.fromarray(np_image).save(fp=file_path)
        else:
            messagebox.showerror('Error', 'Error: First choose image to watermark')

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

    def change_image(self):
        self.background_image = open_file()
        if self.background_image is not None:
            self.canvas.delete('all')
            width, height = self.aspect_ratio(self.background_image)
            resized = self.background_image.resize((width, height))
            self.original_image = self.background_image
            self.background_image = ImageTk.PhotoImage(resized)
            self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')
            # that way we can always go back to original image after failed watermark
        else:
            self.canvas.create_text(450, 300, text="Image not chosen", font=('Arial', 30, "bold"))

    def popup_window_text(self):
        # Create a new instance of the popup window
        if self.background_image is not None:
            self.popup = PopupWindowTextInput(self)
        elif self.mode == 'image':
            # if mode is text error message when clicking on this button
            messagebox.showerror('Error', 'Error: You need to reset before adding another type of watermark!')
        else:
            messagebox.showerror('Error', 'Error: Image is not chosen!')

    def popup_window_image(self):
        # Create a new instance of the popup window
        if self.background_image is not None:
            self.popup = PopupWindowImageInput(self)
        elif self.mode == 'text':
            messagebox.showerror('Error', 'Error: You need to reset before adding another type of watermark!')
        else:
            messagebox.showerror('Error', 'Error: Image is not chosen!')

    def save_text_input(self, text, color, size, opacity, rotation):
        self.text = text  # that way user won't need to remember inputs if he wants to change anything
        self.color = color
        self.size = size
        self.opacity = opacity
        self.rotation = rotation
        self.properties_label.config(text=f"Watermark Text: {text}\nText Color: {color[1]}\nText Size: {size}"
                                          f"\nText Opacity:{opacity}Text Rotation: {self.rotation}")
        self.mode = 'text'
        self.watermark(self.mode)

    def save_image_input(self, size, opacity):
        self.size = size
        self.opacity = opacity
        # self.rotation = rotation
        self.mode = 'image'
        self.properties_label.config(text=f'Watermark Image Size: {size}\nImage Opacity: {opacity}\n')
        # f'Image Rotation: {rotation}'
        self.watermark(self.mode)

    def watermark(self, mode):
        # one day I will add option to choose position of watermark
        watermark_image = self.original_image.copy()
        if mode == "text":
            # create a new transparent RGBA image with the same size as the original image
            text = Image.new('RGBA', watermark_image.size, (255, 255, 255, 0))

            # create a draw object to draw on the text image
            draw = ImageDraw.Draw(text)

            # to draw on the middle
            w, h = watermark_image.size
            x, y = int(w / 2), int(h / 2)

            font = ImageFont.truetype("arial.ttf", int(self.size))

            # add watermark
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

        elif mode == 'image':
            size = (self.size, self.size)
            cropped_image = self.logo.copy()
            cropped_image.thumbnail(size)
            watermark_size = watermark_image.size
            cropped_size = cropped_image.size
            # rotated_image = cropped_image.rotate(self.rotation, expand=True)

            # create a new image with a transparent background of the same size as the rotated image
            transparent_image = Image.new('RGBA', cropped_image.size, (0, 0, 0, 0))

            # paste the rotated image onto the transparent image
            transparent_image.paste(cropped_image, (0, 0), cropped_image)

            # calculate center point of watermark image
            center_x = watermark_size[0] // 2
            center_y = watermark_size[1] // 2

            # calculate top-left point of cropped image
            top_left_x = center_x - cropped_size[0] // 2
            top_left_y = center_y - cropped_size[1] // 2

            # add alpha channel to the transparent image
            alpha = transparent_image.split()[-1]
            alpha.putdata([round((100 - int(self.opacity)) * 2.55)] * (alpha.size[0] * alpha.size[1]))
            transparent_image.putalpha(alpha)
            watermark_image.alpha_composite(transparent_image, dest=(top_left_x, top_left_y))

            # resize the watermarked image to fit the canvas
            width, height = self.aspect_ratio(watermark_image)
            resized = watermark_image.resize((width, height))
            self.background_image = ImageTk.PhotoImage(resized)
            self.canvas.delete('all')
            self.canvas.create_image(0, 0, image=self.background_image, anchor='nw')


# Create the tkinter window
window = tk.Tk()

# Create the MainWindow instance
app = AppWindow(window)

# Start the tkinter event loop
window.mainloop()
