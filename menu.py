import tkinter as tk
from tkinter import filedialog, BOTH, NW, Scrollbar, SUNKEN, HORIZONTAL, Y, X

from PIL import ImageTk, Image
import os
from CarsDataset.tf_oda_stanford_cars import predict_image as pi


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # creating button panel
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.open_file = tk.Button(self, text="Open File", command=self.detection_add_file)
        self.label = tk.Label(self, text="Choose your file",
                              fg="white",
                              bg="black",
                              font="Helvetica 11 bold italic")

        # creating canvas for reflection file
        self.canvas = tk.Canvas(self, relief=SUNKEN, bg='white',
                                width=1280,
                                height=720)
        self.canvas.config(highlightthickness=0)

        # creating scrollbar for canvas
        self.xscrollbar = Scrollbar(self, orient=HORIZONTAL)
        self.xscrollbar.config(command=self.canvas.xview)
        self.yscrollbar = Scrollbar(self)
        self.yscrollbar.config(command=self.canvas.yview)

        self.canvas.config(xscrollcommand=self.xscrollbar.set)
        self.canvas.config(yscrollcommand=self.yscrollbar.set)

        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.create_widgets()

    def create_widgets(self):
        self.quit.pack(side="bottom")
        self.open_file.pack(side="bottom")
        self.label.pack(fill=BOTH, expand=1, side="bottom")

        self.xscrollbar.pack(side="bottom", fill=X)
        self.yscrollbar.pack(side="right", fill=Y)
        self.canvas.pack(side="top", expand=1, fill=BOTH)

    def detection_add_file(self):
        self.label["text"] = "Computing... Wait a few minutes."
        filename = filedialog.askopenfilename(initialdir="/NTUU/Py/Vehicle_detection/CarsDataset/car_ims",
                                              title="Select File",
                                              filetypes=(('image files', '.jpg'),
                                                         ('image files', '.png'),
                                                         # ("all video format", ".mp4"),
                                                         # ("all video format", ".flv"),
                                                         # ("all video format", ".avi"),
                                                         ("all files", "*.*")))
        if filename:
            self.detection_open_file(filename)

    def detection_open_file(self, filename):
        # getting result from image detection
        if os.path.splitext(filename)[1] == '.jpg' or '.png':
            result = pi.main(filename)
            if result:
                self.label["text"] = result

                # showing detected car
                basename = os.path.basename(filename)
                photo = Image.open("E:/NTUU/Py/Vehicle_detection/detected_vehicles/" + basename)
                width, height = photo.size
                img = ImageTk.PhotoImage(photo)
                self.canvas.create_image(0, 0, anchor=NW, image=img)
                self.canvas.config(scrollregion=(0, 0, width, height))
                self.canvas.image = img


root = tk.Tk()
root.title("Car Detection")
root.geometry("1200x1000")
app = Application(master=root)
app.mainloop()
