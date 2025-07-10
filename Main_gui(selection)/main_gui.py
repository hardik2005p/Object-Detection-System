from tkinter import *
import customtkinter
from functools import partial
import os
import threading
from test3 import process_frame
from PIL import Image, ImageTk
import cv2

def check_barcode():
    def on_key_press(event):
        barcode = entry.get()
        global scanned_barcode
        scanned_barcode = barcode
        barcode_window.destroy()
        product_barcode_prefix = str(product_dict[current_product].get('Barcode', ''))  # Convert to string
        if product_barcode_prefix in scanned_barcode:
            check_barcode_button.config(bg='green')
            start_detection_button.config(state=NORMAL)
        else:
            check_barcode_button.config(bg='red')
            start_detection_button.config(state=DISABLED)
            print("Scanned barcode does not match the product's barcode prefix.")

    barcode_window = Toplevel(window)
    barcode_window.title("Barcode Scanner")
    barcode_window.geometry("300x100")

    Label(barcode_window, text="Scan the barcode:").pack(pady=10)
    entry = Entry(barcode_window, font=("Helvetica", 18))
    entry.pack(pady=5)
    entry.bind("<Return>", on_key_press)  # Bind the Enter key to the on_key_press function
    entry.focus_set()

def read_product_dict():
    if os.path.exists("product_dict.txt"):
        with open("product_dict.txt", "r") as file:
            data = file.read()
            return eval(data)
    else:
        return {}

def load_product(product_name):
    global product_holder_frame1, current_product, product_specs, ok_button_active, detection_active, stop_detection
    current_product = product_name
    product_specs = product_dict[product_name]
    ok_button_active = False  # Reset OK button active status
    detection_active = False  # Reset detection active status

    stop_detection = True  # Stop current detection thread
    start_detection_button.config(state=DISABLED)
    check_barcode_button.config(state=DISABLED)

    for widget in product_holder_frame1.winfo_children():
        widget.destroy()
    product_holder_frame1.config(bg='#454342')
    Label(product_holder_frame1, text=product_name, font=("Helvetica", 30, "bold"), bg='#454342', fg='white').place(x=169, rely=0.3)
    
    # Reset button colors
    okay_button.config(bg='white')
    not_okay_button.config(bg='white')
    check_barcode_button.config(bg='white')

    # Enable the barcode detection button when a product is loaded if 'Barcode' key exists
    if 'Barcode' in product_specs:
        check_barcode_button.config(state=NORMAL)
    else:
        start_detection_button.config(state=NORMAL)

def normalize_dict(d):
    return {k.lower(): int(v) for k, v in d.items()}

def update_gui():
    global cap, class_counts, ok_button_active, stop_detection
    while cap.isOpened() and not stop_detection:
        ret, frame = cap.read()
        if not ret:
            break

        if detection_active:
            # Process the frame using the refactored function from test3.py
            frame, class_counts = process_frame(frame)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)

            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)

            # Normalize and debug output for class counts and product specs
            norm_class_counts = normalize_dict(class_counts)
            norm_product_specs = normalize_dict({k: v for k, v in product_specs.items() if k.lower() != 'barcode'})
            print(f"Normalized Class Counts: {norm_class_counts}")
            print(f"Normalized Product Specs: {norm_product_specs}")

            # Compare class counts with product specs
            if not ok_button_active:
                if norm_class_counts == norm_product_specs:
                    okay_button.config(bg='green')
                    not_okay_button.config(bg='white')
                    ok_button_active = True
                else:
                    not_okay_button.config(bg='red')
        
        # To ensure the GUI is responsive
        video_label.update()

def start_detection():
    global cap, detection_active, stop_detection
    detection_active = True  # Set detection active status to True
    stop_detection = False  # Allow detection to run
    if cap is None:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return

    not_okay_button.config(bg='red')  # Turn 'Not Okay' button red when detection starts
    threading.Thread(target=update_gui, daemon=True).start()

product_dict = read_product_dict()
current_product = None
product_specs = None
class_counts = {}
ok_button_active = False
detection_active = False  # Initialize detection active status
stop_detection = False  # Initialize stop detection flag
cap = None
scanned_barcode = None  # Variable to store the scanned barcode

window = Tk()
window.geometry('1300x800')
window.title("Parts Detection System")

Siemens_frame = Frame(master=window, width=325, height=149, background='#454342', relief='raised', bd=3)
Siemens_frame.place(x=975, y=0)
Siemens_label = Label(master=window, text="SIEMENS", font=("Inter", 48, "bold"), background='#454342', fg='white').place(x=991, y=34)

class_holder_frame = Canvas(master=window, height=139, width=965, background='#454342', relief='solid', bd=3, highlightbackground='black')
class_holder_frame.place(x=0, y=0)
class_holder_frame1 = customtkinter.CTkScrollableFrame(master=window, width=940, height=104, fg_color="#454342", orientation="horizontal")
class_holder_frame1.place(x=18, y=17)

webcam_frame = Frame(master=window, width=525, height=525, background='#454342', relief='solid', bd=3)
webcam_frame.place(x=722, y=188)
video_label = Label(webcam_frame)
video_label.pack(expand=True, fill=BOTH)  # Make sure video_label is within webcam_frame

product_holder_frame1 = Frame(master=window, width=553, height=117, background='#454342', relief='raised', bd=3)
product_holder_frame1.place(x=75, y=195)

okay_button = Button(window, height=3, width=20, bg='white', relief='solid', bd=3, text='Okay', font=("Inter", 18, "bold"))
okay_button.place(x=164, y=350)
not_okay_button = Button(window, height=3, width=20, bg='white', relief='solid', bd=3, text='Not Okay', font=("Inter", 18, "bold"))
not_okay_button.place(x=164, y=490)
start_detection_button = Button(window, height=3, width=12, bg='white', fg='black', relief='solid', bd=3, text='Start Detection', font=("Inter", 12, "bold"), state=DISABLED, command=start_detection)
start_detection_button.place(x=350, y=645)
check_barcode_button = Button(window, height=3, width=12, bg='white', fg='black', relief='solid', bd=3, text='Check Barcode', font=("Inter", 12, "bold"), state=DISABLED, command=check_barcode)
check_barcode_button.place(x=150, y=645)

for key in product_dict:
    new_button = Button(class_holder_frame1, text=key, width=20, height=4, bd=3, relief="solid", command=partial(load_product, key))
    new_button.pack(side="left", pady=2, padx=2)

window.mainloop()

if cap:
    cap.release()
cv2.destroyAllWindows()
