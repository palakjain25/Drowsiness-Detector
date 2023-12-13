#libraries
import tkinter as tk
import customtkinter as ctk
import torch
import numpy as np
import cv2
from PIL import Image, ImageTk
import vlc
import time

ctk.set_appearance_mode("light")

app = tk.Tk()
app.geometry("700x800")
app.title("Drowsy Detection App")
app.iconbitmap('images/sleeping-face.ico')

#video frame widget
vidFrame = tk.Frame(height=480, width=600)
vidFrame.pack()
vid = ctk.CTkLabel(vidFrame, text="")
vid.pack()

#counter widget
counter = 0
counter_var = tk.StringVar()
counterLabel = ctk.CTkLabel(master=app, height=30, width=140,text_color="black", fg_color="transparent", textvariable=counter_var)
counterLabel.configure(font=("Arial", 16))
counterLabel.pack()
counter_var.set(f"Sleep Counter: {counter}")

def reset_counter():
  global counter
  counter = 0
  counter_var.set(f"Sleep Counter: {counter}")
  counterLabel.configure(text=f"Sleep Counter: {counter}")
  
#Reset Button widget 
resetButton = ctk.CTkButton(master=app, text="Reset Counter", command=reset_counter, height=30, width=140, text_color="white", fg_color="#5f31f3", hover_color="#815AFF", corner_radius=6)
resetButton.configure(font=("Arial", 16))
resetButton.pack(pady=(0, 10))

#function to set sound
ans=None
def change_handler(value):
    global ans
    if value == "English":
        ans = 1
        print(ans)
    elif value == "Hindi":
        ans = 2
        print(ans)
    elif value == "Marathi":
        ans = 3
        print(ans)
    elif value == "None":
        ans = 0
        print(ans)
    elif value == "Japanese":
        ans = 4
        print(ans)
    elif value == "Ghastly":
        ans = 5
        print(ans)
    elif value == "Bird":
        ans = 6
        print(ans)
    elif value == "Classic":
        ans = 7
        print(ans)
        
    return ans
    
#Select Sound widget 
combobox_title = ctk.CTkLabel(master=app, text="Select Sound", height=30, width=140, text_color="black", fg_color="transparent")
combobox_title.configure(font=("Arial", 16))
combobox_title.pack()

#Set widget 
combobox = ctk.CTkComboBox(master=app,height=30, width=140, values=["None","English", "Hindi", "Marathi","Japanese","Ghastly","Bird","Classic"], command=change_handler)
combobox.place(relx=0.5, rely=0.5, anchor="center")
combobox.configure(font=("Arial", 16))
combobox.pack(pady=(0, 10))

#function to set time
set_input_time = 20
def click_handler():
    global set_input_time
    input_value = entry.get()
    try:
        set_input_time = int(input_value)
        print(f"Entered value: {set_input_time}")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

#alarm widget
entry = ctk.CTkEntry(master=app, placeholder_text="Set Alarm time (sec)")
btn = ctk.CTkButton(master=app, text="Set", command=click_handler, text_color="white", fg_color="#5f31f3", hover_color="#815AFF", corner_radius=6 )
btn.configure(font=("Arial", 16))
entry.pack(pady=(7, 3))
btn.pack(pady=(0, 10))

#Volume aduster widget
slider_title = ctk.CTkLabel(master=app, text="Adjust Volume", height=30, width=140, text_color="black", fg_color="transparent")
slider_title.configure(font=("Arial", 16))
slider_title.pack(pady=(4,10))
slider_value = tk.DoubleVar()
slider = ctk.CTkSlider(master=app, from_=0, to=100, number_of_steps=50,variable=slider_value,button_color="#5f31f3" , progress_color="#5e5e5e", orientation="horizontal")
slider.pack()

#load model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp6/weights/last.pt', force_reload=True)

#real time detection
cap = cv2.VideoCapture(0)
start_time = time.time()
def detect():
    global ans
    global counter
    global start_time
    global set_input_time
    ret, frame = cap.read()
    frame = cv2.cvtColor (frame, cv2.COLOR_BGR2RGB)
    results= model(frame)
    img=np.squeeze(results.render())
#   print(results.xywh[0])
    if len(results.xywh[0]) > 0:
        dconf = results.xywh[0][0][4]
        dclass = results.xywh[0][0][5]
        elapsed_time = time.time() - start_time

        if dconf.item() > 0.70 and dclass.item() == 16.0 and elapsed_time >= set_input_time:
            # filechoice = random.choice([1])
            filechoice = ans
            print(set_input_time)
            
            # Adjusting volume using slider_value.get()
            volume = slider_value.get()
            p = vlc.MediaPlayer(f"file:///{filechoice}.wav")
            media = vlc.Media(f"file:///{filechoice}.wav")
            media.get_mrl()
            p.set_media(media)
            
            p.audio_set_volume(int(volume))  # Set volume level
            p.play()
            
            counter+=1 
            elapsed_time=0
            start_time = time.time()
             
    # Updating both counter_var and counter
    counter_var.set(f"Sleep Counter: {counter}")
    counterLabel.configure(text=counter_var.get())
    imgarr = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(imgarr)
    vid.imgtk = imgtk
    vid.configure(image=imgtk)
    vid.after(10, detect)

detect()
app.mainloop()