import tkinter as tk
from simple_downloader import get_images

FONT = ("Lato", 12)


def on_submit():
    num = 0
    values = []

    test_size = test_slider.get()/100
    valid_size = valid_slider.get()/100

    if categories.get() != '':
        values = categories.get().split(';')
        values = [v.strip() for v in values]

    if number.get() != '':
        num = int(number.get())

    print("Categories: ", values)
    print("Number: ", num)
    print("Test set size: ", test_size)
    print("Valid set size: ", valid_size)

    get_images(values, num, test_size, valid_size)


root = tk.Tk()
root.geometry("500x500")
root.title("Google images downloader")

title = tk.Label(root, text="Downloading parameters", font=("Lato", 18))
title.pack(padx=10, pady=10)

categories_label = tk.Label(root, text="Categories separated by semicolons", font=FONT)
categories_label.pack(pady=(15, 0))
categories = tk.Entry(root, font=FONT, width=50)
categories.pack()

number_label = tk.Label(root, text="Number of photos in each category", font=FONT)
number_label.pack(pady=(15, 0))
number = tk.Entry(root, font=("Lato", 15), width=8)
number.pack()

test_label = tk.Label(root, text="Test set size (%) ", font=FONT)
test_label.pack(pady=(25, 0))
test_slider = tk.Scale(root, from_=0, to=50, orient='horizontal', width=20, length=300)
test_slider.set(20)
test_slider.pack()

valid_label = tk.Label(root, text="Validation set size (%) ", font=FONT)
valid_label.pack(pady=(25, 0))
valid_slider = tk.Scale(root, from_=0, to=50, orient='horizontal', width=20, length=300)
valid_slider.set(10)
valid_slider.pack()

submit = tk.Button(text='Submit', command=on_submit, width=20, height=2)
submit.pack(pady=(15, 0))

root.mainloop()
