import tkinter as tk
from simple_downloader import get_images

FONT = ("Lato", 12)
COLOR = "#8fd9d9"


class View:
    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("500x500")
        self.root.title("Google images downloader")

        self.title = tk.Label(self.root, text="Downloading parameters", font=("Lato", 18))
        self.title.pack(padx=10, pady=10)

        self.categories_label = tk.Label(self.root, text="Categories separated by semicolons", font=FONT)
        self.categories_label.pack(pady=(15, 0))
        self.categories = tk.Entry(self.root, font=FONT, width=50)
        self.categories.pack()

        self.number_label = tk.Label(self.root, text="Number of photos in each category", font=FONT)
        self.number_label.pack(pady=(15, 0))
        self.number = tk.Entry(self.root, font=("Lato", 15), width=8)
        self.number.pack()

        self.test_label = tk.Label(self.root, text="Test set size (%) ", font=FONT)
        self.test_label.pack(pady=(25, 0))
        self.test_slider = tk.Scale(self.root, from_=0, to=50, orient='horizontal', width=20, length=300,
                                    troughcolor="white", activebackground=COLOR)
        self.test_slider.set(20)
        self.test_slider.pack()

        self.valid_label = tk.Label(self.root, text="Validation set size (%) ", font=FONT)
        self.valid_label.pack(pady=(25, 0))
        self.valid_slider = tk.Scale(self.root, from_=0, to=50, orient='horizontal', width=20, length=300,
                                     troughcolor="white", activebackground=COLOR)
        self.valid_slider.set(10)
        self.valid_slider.pack()

        self.submit = tk.Button(text='Submit', command=self.on_submit, width=20, height=2, font=("Lato", 9), bg=COLOR)
        self.submit.pack(pady=(25, 0))

        self.communicate = tk.StringVar()
        self.communicate.set("")
        self.communicate_label = tk.Label(self.root, textvariable=self.communicate, font=("Lato", 9))
        self.communicate_label.pack(pady=(15, 0))

        self.root.mainloop()

    def on_submit(self):
        self.communicate.set("")

        test_size = self.test_slider.get() / 100
        valid_size = self.valid_slider.get() / 100

        if self.categories.get().strip() == '':
            self.communicate.set("Categories field is empty!")
            self.categories.delete(0, 'end')
            return

        elif ',' in self.categories.get() and ';' not in self.categories.get():
            self.communicate.set("Categories should be separated by ' ; '!")
            return

        else:
            values = self.categories.get().split(';')
            values = [v.strip() for v in values]

        if self.number.get().isnumeric():
            num = int(self.number.get())
        else:
            self.communicate.set("Something is wrong with number field!")
            self.number.delete(0, 'end')
            return

        print("Categories: ", values)
        print("Number: ", num)
        print("Test set size: ", test_size)
        print("Valid set size: ", valid_size)

        get_images(values, num, test_size, valid_size)
        self.communicate.set("Downloading completed!")
