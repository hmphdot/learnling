from abc import update_abstractmethods
from src.ai import generate_question, test_answer
from src.input_handler import InputDialog, question_dialogue
from src.visualization import update_life, update_death, root_start, stop
from src.static import textPanel, show_gravestone, bowl_static_image
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import sys, math, threading, time, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
gravestone_path = os.path.join(BASE_DIR, "src", "visuals", "statics", "gravestone.png")
image_path = os.path.join(BASE_DIR, "src", "visuals", "statics", "big_chat.png")


# initialize settings
app = QApplication(sys.argv)
course = InputDialog("What course are you studying?").get_input()
unit_input = InputDialog("What units are you specifically looking at? (comma separated)").get_input()
study_time = InputDialog("How long are you studying for? (minutes)").get_input()

tombs = 0
units = []
units[:] = [u.strip() for u in unit_input.split(",") if u.strip()]
int_time = int(study_time)
loops = math.ceil(int_time / 25)
curr_loops = 0

# begin 
# add static stuff
bowl_image_path = os.path.join(BASE_DIR, "visuals", "statics", "bowl.png")
bowl_ui = bowl_static_image(bowl_image_path)

def start_question_sequence() -> None:
    global tombs
    print("question sequence started")
    ui = textPanel(image_path)
    ui["window"].show()
    unit = ""
    if len(units) > 1:
        unit = units[0]
        units.pop(0)
    else:
        unit = units[0]
    q = generate_question(course, unit)
    a = question_dialogue(q).get_input()
    correct = test_answer(q, a)
    if not correct: 
        update_death()
        root_start()
        grav_ui = show_gravestone(x=1700, y=950, multi=tombs)
        grav_ui["window"].show()
        tombs += 1
    else:
        question_dialogue("Correct! Input to continue!").get_input()
        
    threading.Thread(target=studyTimer, args=(2, ), daemon=True).start()
    update_life()
    root_start()
    start_question_sequence()
    sys.exit(ui["app"].exec())

def studyTimer(secs: int) -> None:
    print("timer started")
    time.sleep(secs)
    stop()

def main() -> None:
    global curr_loops
    while (curr_loops < loops):
        threading.Thread(target=studyTimer, args=(2, ), daemon=True).start()
        update_life()
        root_start()
        start_question_sequence()
        curr_loops += 1

if __name__ == "__main__":
    main()