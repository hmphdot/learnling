import os
import tkinter as tk
from PIL import Image, ImageTk
# import matplotlib
# matplotlib.use('QtAgg')
# import matplotlib.pyplot as plt

# TeX settings for output window -> doesn't work due to threading limitations
# plt.rcParams["text.usetex"] = True
# plt.rcParams['toolbar'] = 'None'
# fig, ax = plt.subplots()
# ax.axis('off')
# manager = fig.canvas.manager
# manager.set_window_title("Question Time!")
# manager.window.setGeometry(1100, 630, 500, 200)

# tkinter initialization - general settings
frame_index = 0
death_index = 0
frame_delay = 100
death_delay = 1000
# tk settings
root = tk.Tk()
root.config(bg="lightblue")
root.overrideredirect(True)
#root.attributes('-alpha', 0.3)
root.attributes("-topmost", True)
root.wm_attributes('-transparentcolor', 'black')
root.geometry("+1780+900")

# load images
life_path = os.path.join("src", "visuals", "life")
death_path = os.path.join("src", "visuals", "death")
paths = [life_path, death_path]
all_frames = list()
for i in paths:
    frames = []
    for file in sorted(os.listdir(i)):
        if file.endswith(".png"):
            path = os.path.join(i, file)
            img = Image.open(path).convert("RGBA")
            frames.append(ImageTk.PhotoImage(img))
    all_frames.append(frames)
fish_frames = all_frames[0]
death_frames = all_frames[1]
label = tk.Label(root)
label.pack()

# def display_question(question: str) -> None:
#     ax.text(0.5, 0.5, question, fontsize=20, horizontalalignment='center', verticalalignment='center')
#     plt.show()

# def remove_equation() -> None:
#     plt.close()
    
# below will be for fish -> needs testing
def update_life() -> None:
    global frame_index
    label.config(image=fish_frames[frame_index]) 
    frame_index = (frame_index + 1) % len(fish_frames)
    root.after(frame_delay, update_life)
    
def update_death() -> None:
    global death_index
    label.config(image=death_frames[death_index])
    death_index += 1
    if death_index < len(frames):
        root.after(death_index, update_death)
    else:
        death_index = 0
        root.after(death_delay, root.quit)

def root_start() -> None:
    global frame_index
    frame_index = 0
    root.mainloop()
    
def stop() -> None:
    if root is not None:
        root.quit()