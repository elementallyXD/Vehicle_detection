import tkinter as tk
from tkinter import filedialog, Text, BOTH, NW
from PIL import ImageTk, Image
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, bg='white', width=1024, height=720)
        self.canvas.pack()

        self.open_file = tk.Button(self)
        self.open_file["text"] = "Open File"
        self.open_file["command"] = self.addFile
        self.open_file.pack(side="bottom")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")


    def addFile(self):
        filename = filedialog.askopenfilename(initialdir="/NTUU/Py/Vehicle_detection/CarsDataset/car_ims/car_ims",
                                              title="Select File",
                                              filetypes=(('image files', '.jpg'),
                                                         ('image files', '.png'),
                                                         ("all video format", ".mp4"),
                                                         ("all video format", ".flv"),
                                                         ("all video format", ".avi"),
                                                         ("all files", "*.*")))

        self.openFile(filename)
        # files.append(filename)
        # print(filename)
        # for file in files:
        #     label = tk.Label(canvas, text=file, bg="gray")
        #     label.pack()


    def openFile(self, filename):
        self.img = ImageTk.PhotoImage(Image.open(filename))
        self.canvas.create_image(20,20, anchor=NW, image=self.img)
        self.canvas.image = self.img


root = tk.Tk()
root.title("Car Detection")
root.geometry("1024x1000")
app = Application(master=root)
app.mainloop()