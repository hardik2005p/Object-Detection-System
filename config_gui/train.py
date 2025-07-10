import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import os
import subprocess
import threading

class VideoToImagesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to Images Converter")
        self.root.geometry("700x500")  # Increase window size
        
        self.video_path = ""
        self.output_folder = ""
        self.data_yaml_folder = ""  # To store the path for data.yaml and train.py
        self.model_path = ""  # To store the model path for testing
        
        self.page_stack = []
        
        self.create_widgets()
    
    def create_widgets(self):
        self.clear_widgets()
        
        self.page_stack.append(self.create_widgets)
        
        self.add_heading_frame()
        
        self.browse_video_button = tk.Button(self.root, text="Browse Video", command=self.browse_video, width=20)
        self.browse_video_button.pack(pady=10)
        
        self.video_label = tk.Label(self.root, text="No video selected", wraplength=400)
        self.video_label.pack(pady=10)
        
        self.browse_folder_button = tk.Button(self.root, text="Select Output Folder", command=self.browse_folder, width=20)
        self.browse_folder_button.pack(pady=10)
        
        self.folder_label = tk.Label(self.root, text="No folder selected", wraplength=400)
        self.folder_label.pack(pady=10)
        
        self.start_button = tk.Button(self.root, text="Start Conversion", command=self.start_conversion, width=20)
        self.start_button.pack(pady=20)
        
        self.next_button = tk.Button(self.root, text="Next", command=self.open_next_page, width=10)
        self.next_button.place(x=580, y=450)
    
    def add_heading_frame(self):
        heading_frame = tk.Frame(self.root, bg="#009999")
        heading_frame.pack(fill=tk.X)
        
        heading_label = tk.Label(heading_frame, text="SIEMENS", fg="white", bg="#009999", font=("Arial", 16, "bold"))
        heading_label.pack(side=tk.RIGHT, padx=10, pady=5)
    
    def browse_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
        if self.video_path:
            self.video_label.config(text=os.path.basename(self.video_path))
        else:
            self.video_label.config(text="No video selected")
    
    def browse_folder(self):
        self.output_folder = filedialog.askdirectory()
        if self.output_folder:
            self.folder_label.config(text=self.output_folder)
        else:
            self.folder_label.config(text="No folder selected")
    
    def start_conversion(self):
        if not self.video_path:
            messagebox.showwarning("Warning", "Please select a video file.")
            return
        
        if not self.output_folder:
            messagebox.showwarning("Warning", "Please select an output folder.")
            return
        
        cap = cv2.VideoCapture(self.video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames < 250:
            messagebox.showerror("Error", "The video does not have enough frames (minimum 250 required).")
            cap.release()
            return
        
        count = 0
        while count < 250:
            ret, frame = cap.read()
            if not ret:
                break
            output_path = os.path.join(self.output_folder, f"frame_{count+1}.jpg")
            cv2.imwrite(output_path, frame)
            count += 1
        
        cap.release()
        messagebox.showinfo("Success", "250 images have been saved successfully.")
    
    def open_next_page(self):
        self.clear_widgets()
        self.create_annotate_page()
    
    def create_annotate_page(self):
        self.clear_widgets()
        
        self.page_stack.append(self.create_annotate_page)
        
        self.add_heading_frame()
        
        heading = tk.Label(self.root, text="Start Annotating", font=("Arial", 20))
        heading.pack(pady=20)
        
        instruction = tk.Label(self.root, text="Click Open to go to LabelImg", font=("Arial", 14))
        instruction.pack(pady=10)
        
        open_button = tk.Button(self.root, text="Open", command=self.open_labelimg, width=20)
        open_button.pack(pady=20)
        
        back_button = tk.Button(self.root, text="Back", command=self.go_back, width=10)
        back_button.place(x=50, y=450)
        
        next_button = tk.Button(self.root, text="Next", command=self.open_next_page_3, width=10)
        next_button.place(x=580, y=450)
    
    def read_labelimg_path(self):
        try:
            with open("path.txt", "r") as file:
                path = file.readline().strip()
                return path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read path.txt: {e}")
            return None
    
    def open_labelimg(self):
        labelimg_path = self.read_labelimg_path()
        if labelimg_path and os.path.exists(labelimg_path):
            try:
                subprocess.Popen([labelimg_path])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open LabelImg: {e}")
        else:
            messagebox.showerror("Error", "LabelImg executable not found at the specified path.")
    
    def open_next_page_3(self):
        self.clear_widgets()
        self.create_data_yaml_page()
    
    def create_data_yaml_page(self):
        self.clear_widgets()
        
        self.page_stack.append(self.create_data_yaml_page)
        
        self.add_heading_frame()
        
        heading = tk.Label(self.root, text="Create data.yaml", font=("Arial", 20))
        heading.pack(pady=20)
        
        folder_label = tk.Label(self.root, text="Path to folder to create data.yaml:")
        folder_label.pack(pady=5)
        
        self.folder_entry = tk.Entry(self.root, width=50)
        self.folder_entry.pack(pady=5)
        
        self.browse_folder_button = tk.Button(self.root, text="Browse", command=lambda: self.browse_path(self.folder_entry), width=10)
        self.browse_folder_button.pack(pady=5)
        
        train_label = tk.Label(self.root, text="Path to train images:")
        train_label.pack(pady=5)
        
        self.train_entry = tk.Entry(self.root, width=50)
        self.train_entry.pack(pady=5)
        
        self.browse_train_button = tk.Button(self.root, text="Browse", command=lambda: self.browse_path(self.train_entry), width=10)
        self.browse_train_button.pack(pady=5)
        
        classes_label = tk.Label(self.root, text="Number of classes:")
        classes_label.pack(pady=5)
        
        self.classes_entry = tk.Entry(self.root, width=10)
        self.classes_entry.pack(pady=5)
        
        names_label = tk.Label(self.root, text="Class names:")
        names_label.pack(pady=5)
        
        self.names_entry = tk.Entry(self.root, width=50)
        self.names_entry.pack(pady=5)
        
        create_button = tk.Button(self.root, text="Create data.yaml", command=self.create_data_yaml, width=20)
        create_button.pack(pady=20)
        
        back_button = tk.Button(self.root, text="Back", command=self.go_back, width=10)
        back_button.place(x=50, y=450)
        
        next_button = tk.Button(self.root, text="Next", command=self.open_next_page_4, width=10)
        next_button.place(x=580, y=450)
    
    def browse_path(self, entry):
        path = filedialog.askdirectory()
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)
    
    def create_data_yaml(self):
        folder_path = self.folder_entry.get()
        train_path = self.train_entry.get()
        num_classes = self.classes_entry.get()
        class_names = self.names_entry.get()

        if not folder_path or not train_path or not num_classes or not class_names:
            messagebox.showwarning("Warning", "Please fill in all the fields.")
            return

        data_yaml_content = f"""
train: {train_path}
val: {train_path}
nc: {num_classes}
names: [{class_names}]
"""

        train_py_content = f"""
import os
import torch
from ultralytics import YOLO

model = YOLO('yolov8.yaml')  # Replace with your YOLOv8 model configuration

data_yaml_path = os.path.join('{folder_path}', 'data.yaml')

model.train(data=data_yaml_path, epochs=100)
"""

        try:
            data_yaml_path = os.path.join(folder_path, "data.yaml")
            train_py_path = os.path.join(folder_path, "train.py")
            self.data_yaml_folder = folder_path  # Update data_yaml_folder with the path
            
            with open(data_yaml_path, "w") as file:
                file.write(data_yaml_content)
            
            with open(train_py_path, "w") as file:
                file.write(train_py_content)
            
            messagebox.showinfo("Success", f"data.yaml and train.py have been created in {folder_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create data.yaml or train.py: {e}")
    
    def open_next_page_4(self):
        self.clear_widgets()
        self.create_train_model_page()
    
    def create_train_model_page(self):
        self.clear_widgets()
        
        self.page_stack.append(self.create_train_model_page)
        
        self.add_heading_frame()
        
        heading = tk.Label(self.root, text="Train the Model", font=("Arial", 20))
        heading.pack(pady=20)
        
        instruction = tk.Label(self.root, text="Press Start to begin training", font=("Arial", 14))
        instruction.pack(pady=10)
        
        start_button = tk.Button(self.root, text="Start Training", command=self.start_training, width=20)
        start_button.pack(pady=20)
        
        back_button = tk.Button(self.root, text="Back", command=self.go_back, width=10)
        back_button.place(x=50, y=450)
    
    def start_training(self):
        if not self.data_yaml_folder:
            messagebox.showwarning("Warning", "Data folder path is not set. Please create data.yaml first.")
            return
        
        data_yaml_path = os.path.join(self.data_yaml_folder, "data.yaml")
        train_script_path = os.path.join(self.data_yaml_folder, "train.py")
        
        if not os.path.exists(data_yaml_path):
            messagebox.showwarning("Warning", "data.yaml not found. Please create data.yaml first.")
            return

        if not os.path.exists(train_script_path):
            messagebox.showerror("Error", f"train.py not found in {self.data_yaml_folder}")
            return
        
        def run_training():
            try:
                subprocess.run(["python", train_script_path], check=True)
                messagebox.showinfo("Success", "Training completed successfully.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Training failed: {e}")
        
        threading.Thread(target=run_training).start()
    
    def go_back(self):
        if len(self.page_stack) > 1:
            self.page_stack.pop()  # Remove the current page
            previous_page = self.page_stack.pop()  # Get the previous page function
            previous_page()  # Call the previous page function
    
    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToImagesApp(root)
    root.mainloop()
