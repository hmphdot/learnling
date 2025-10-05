import os
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt

# TeX settings for output window
plt.rcParams["text.usetex"] = True
plt.rcParams['toolbar'] = 'None'
fig, ax = plt.subplots()
ax.axis('off')
manager = fig.canvas.manager
manager.set_window_title("Question Time!")
manager.window.setGeometry(1200, 630, 500, 200)

# tkinter initialization
frame_folder = "live_frames"
frame_index = 0
frame_delay = 100
TRANSPARENT_COLOR = "black"
root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.attributes('-alpha', 0.5)
root.geometry("+1780+900")
frames = []
for file in sorted(os.listdir(frame_folder)):
    if file.endswith(".png"):
        path = os.path.join(frame_folder, file)
        img = Image.open(path).convert("RGBA")
        frames.append(ImageTk.PhotoImage(img))
death_index = 0
death_frames = []
frame_folder = "death_frames"
for file in sorted(os.listdir(frame_folder)):
    if file.endswith(".png"):
        path = os.path.join(frame_folder, file)
        img = Image.open(path).convert("RGBA")
        frames.append(ImageTk.PhotoImage(img))
label = tk.Label(root, bg=TRANSPARENT_COLOR)
label.pack()

def display_question(question: str) -> None:
    ax.text(0.5, 0.5, question, fontsize=20, horizontalalignment='center', verticalalignment='center')
    plt.show()
    
# below will be for fish -> needs testing
def fish_update() -> None:
    global frame_index
    label.config(image=frames[frame_index])
    frame_index = (frame_index + 1) % len(frames)
    root.after(frame_delay, fish_update)
    
def start_fish() -> None:
    fish_update()
    root.mainloop()

def fish_death() -> None:
    global death_index
    if death_index == len(death_frames):
        death_index = 0
    label.config(image=death_frames[death_index])
    death_index += 1
    if death_index < len(frames):
        root.after(frame_delay, fish_death)
    else:
        root.after(frame_delay, root.destroy)
    start_fish()