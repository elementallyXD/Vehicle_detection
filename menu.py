import tkinter as tk
from tkinter import filedialog, Text, BOTH, NW
from PIL import ImageTk, Image
import os
from CarsDataset.tf_oda_stanford_cars import predict_image as pi


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.open_file = tk.Button(self)
        self.label = tk.Label(self, text="Choose your file",
                              fg="white",
                              bg="black",
                              font="Helvetica 11 bold italic")

        self.canvas = tk.Canvas(self, bg='white', width=1024, height=720)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.create_widgets()

    def create_widgets(self):
        self.quit.pack(side="bottom")
        self.open_file.pack(side="bottom")
        self.label.pack(fill=BOTH, expand=1, side="bottom")
        self.canvas.pack(side="top")

        self.open_file["text"] = "Open File"
        self.open_file["command"] = self.addFile

    def addFile(self):
        self.label["text"] = "Computing... Wait a few minutes."
        filename = filedialog.askopenfilename(initialdir="/NTUU/Py/Vehicle_detection/CarsDataset/car_ims/car_ims",
                                              title="Select File",
                                              filetypes=(('image files', '.jpg'),
                                                         ('image files', '.png'),
                                                         # ("all video format", ".mp4"),
                                                         # ("all video format", ".flv"),
                                                         # ("all video format", ".avi"),
                                                         ("all files", "*.*")))
        if filename:
            self.openFile(filename)

    def openFile(self, filename):
        text = pi.main(filename)
        myim_basename = os.path.basename(filename)
        self.img = ImageTk.PhotoImage(Image.open("E:/NTUU/Py/Vehicle_detection/detected_vehicles/" + myim_basename))
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)
        self.canvas.image = self.img
        self.label["text"] = text


root = tk.Tk()
root.title("Car Detection")
root.geometry("1024x1000")
app = Application(master=root)
app.mainloop()
