from tkinter import *
from functools import partial
import customtkinter
from tkinter import messagebox
from tkinter import filedialog
from ultralytics import YOLO
import os
import subprocess

product_dict = {}
selected_product = None
product_buttons = {}
product_frames = {}

def print_dict():
    global product_dict
    with open("product_dict.txt", "w") as file:
        file.write(str(product_dict))
    print("Product dictionary saved to product_dict.txt")

def select(product_name):
    global selected_product, product_buttons
    
    if selected_product is not None:
        product_buttons[selected_product].config(bg='SystemButtonFace')
    
    selected_product = product_name
    product_buttons[selected_product].config(bg='lightblue')
    update_product_frame(product_name)

def class_button(key):
    global selected_product
    if selected_product is None:
        messagebox.showwarning("Warning", "No product selected")
    else:
        def submit():
            count = e1.get()
            product_dict[selected_product][key] = int(count)
            update_product_frame(selected_product)
            print(product_dict)
            root.destroy()

        root = Tk()
        root.geometry('400x250')
        root.title("Class entry")
        title_label = Label(root, text="Enter the number of Class", font=("Helvetica", 16, "bold"), pady=20)
        title_label.pack()
        Label(root, text=f'{key}:', font=("Helvetica", 14, 'bold')).place(x=20, y=88)
        e1 = Entry(root, width=30, relief="sunken", bd=2)
        e1.place(x=170, y=92)
        Button(root, height=2, width=15, text="submit", relief="solid", bd=2, command=submit).place(y=158, x=129)
        root.mainloop()

def update_product_frame(product_name):
    global product_frames
    frame = product_frames.get(product_name)
    if frame:
        for widget in frame.winfo_children():
            if not isinstance(widget, Button):
                widget.destroy()
        Label(frame, text=product_name, font=("Helvetica", 20, "bold")).place(relx=0, rely=0)
        y_position = 30
        for key, value in product_dict[product_name].items():
            Label(frame, text=f'{key}: {value}', font=("Helvetica", 14)).place(x=10, y=y_position)
            y_position += 30


def load_product(product_name):
    def close_frame():
        new_frame.destroy()
        del product_buttons[product_name]
        del product_frames[product_name]
        del product_dict[product_name]

    global product_holder_frame1, product_dict

    if product_name not in product_dict:
        product_dict[product_name] = {}
        new_frame = Frame(product_holder_frame1, width=278, height=340, bd=3, relief="solid")
        new_frame.pack_propagate(False)
        Label(new_frame, text=product_name, font=("Helvetica", 20, "bold")).place(relx=0, rely=0)
        close_button = Button(master=new_frame, text='X', height=2, width=2, bg='red', fg='white', command=close_frame)
        close_button.pack(anchor='ne', side=TOP)
        select_button = Button(master=new_frame, text='Select', height=2, width=6, bg='#D9D9D9', fg='black',command=partial(select, product_name))
        select_button.pack(side='bottom', padx=25, pady=5)
        new_frame.pack(padx=2, side='left')
        product_buttons[product_name] = select_button
        product_frames[product_name] = new_frame
    else:
        messagebox.showwarning("Warning", "Product already present")

def add_model():
    global class_holder_frame1, list_model_holder_frame1
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("all files", "*.*"),))
    if filename:
        model_path = rf"{filename}"
        model = YOLO(model_path)
        num_classes = model.model.nc
        class_names = None
        if hasattr(model, 'names') and isinstance(model.names, (list, dict)):
            class_names = model.names if isinstance(model.names, list) else list(model.names.values())
        class_names = class_names[:num_classes]
        for key in class_names:
            new_button = Button(class_holder_frame1, text=key, width=20, height=4, bd=3, relief="solid",
                                command=partial(class_button, key))
            new_button.pack(side="left", pady=2, padx=2)
        
        # Extracting just the filename from the path
        model_filename = os.path.basename(filename)
        
        Label(list_model_holder_frame1, text=f'{model_filename}', font=("Helvetica", 14), bg='#454342', fg='white').pack(pady=5)
        print(class_names)

def add_product():
    def submit():
        global list_product_holder_frame1
        product_name = e1.get()
        new_button = Button(list_product_holder_frame1, text=product_name, width=25, height=2, bd=3, relief="solid",
                            command=partial(load_product, product_name))
        new_button.pack(pady=2, padx=25)

    root = Tk()
    root.geometry('400x250')
    root.title("Add Product")

    title_label = Label(root, text="Add Product", font=("Helvetica", 16, "bold"), pady=20)
    title_label.pack()

    Label(root, text='Product Name:', font=("Helvetica", 14, 'bold')).place(x=20, y=88)

    e1 = Entry(root, width=30, relief="sunken", bd=2)
    e1.place(x=170, y=92)

    Button(root, height=2, width=15, text="submit", relief="solid", bd=2, command=submit).place(y=158, x=129)

    root.mainloop()

def train_model():
    try:
        subprocess.run(["python", "traingui2.py"], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to execute traingui2.py: {e}")

window = Tk()
window.geometry('1300x900')
window.config(bg="#454342")
window.title("config")

Siemens_frame = Frame(master=window, width=325, height=139, background='#454342', relief='raised', bd=3)
Siemens_frame.place(x=975, y=0)
Siemens_label = Label(master=window, text="SIEMENS", font=("Inter", 64 * -1, "bold"), background='#454342', fg='white').place(x=991, y=34)

list_product_holder_frame = Canvas(master=window, height=432, width=325, background='#454342', relief='sunken', bd=3, highlightbackground='black')
list_product_holder_frame.place(x=975, y=139)
list_product_holder_frame1 = Canvas(master=window, height=350, width=256, highlightbackground='#454342', background='#454342')
list_product_holder_frame1.place(x=1009, y=187)

list_model_holder_frame = Canvas(master=window, height=378, width=325, background='#454342', relief='solid', bd=3, highlightbackground='black')
list_model_holder_frame.place(x=976, y=572)
list_model_holder_frame1 = customtkinter.CTkScrollableFrame(master=window, width=256, height=250, fg_color='#454342', orientation="vertical")
list_model_holder_frame1.place(x=1010, y=600)

class_holder_frame = Canvas(master=window, height=139, width=965, background='#454342', relief='solid', bd=3, highlightbackground='black')
class_holder_frame.place(x=0, y=0)
class_holder_frame1 = customtkinter.CTkScrollableFrame(master=window, width=940, height=104, fg_color="#454342", orientation="horizontal")
class_holder_frame1.place(x=18, y=17)
new_button = Button(class_holder_frame1, text='Barcode', width=20, height=4, bd=3, relief="solid",command=partial(class_button, 'Barcode'))
new_button.pack(side="left", pady=2, padx=2)

product_holder_frame = Canvas(master=window, width=965, height=432, bg="#D9D9D9", relief='sunken', bd=3, highlightbackground='black')
product_holder_frame.place(x=0, y=139)
product_holder_frame1 = customtkinter.CTkScrollableFrame(master=window, width=945, height=380, fg_color="#D9D9D9", orientation="horizontal")
product_holder_frame1.place(x=12, y=164, )

button1 = Button(height=4, width=30, bg='white', relief='solid', bd=3, text='Train model', font=("Inter", 12 * -1, "bold"), command=train_model)
button1.place(x=40, y=708)

button2 = Button(height=4, width=30, bg='white', relief='solid', bd=3, text='Add Model', font=("Inter", 12 * -1, "bold"), command=add_model)
button2.place(x=267, y=708)

button3 = Button(height=4, width=30, bg='white', relief='solid', bd=3, text='Add product', font=("Inter", 12 * -1, "bold"), command=add_product)
button3.place(x=494, y=708)

button4 = Button(height=4, width=30, bg='white', relief='solid', bd=3, text='Submit', font=("Inter", 12 * -1, "bold"),command=print_dict)
button4.place(x=721, y=708)

Label(window, text='Product:', font=("Inter", 24 * -1, "bold"), fg='white', bg='#454342').place(x=1090, y=154)
Label(window, text='Models:', font=("Inter", 24 * -1, "bold"), fg='white', bg='#454342').place(x=1090, y=577)

window.mainloop()
