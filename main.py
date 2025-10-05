from src.ai import generate_question, test_answer
from src.input_handler import InputDialog, question_dialogue
from src.visualization import update_life, update_death, root_start, stop
from PyQt6.QtWidgets import QApplication
import sys, math, threading, time

# initialize settings
app = QApplication(sys.argv)
course = InputDialog("What course are you studying?").get_input()
unit_input = InputDialog("What units are you specifically looking at? (comma separated)").get_input()
study_time = InputDialog("How long are you studying for? (minutes)").get_input()

lives = 1
units = []
units[:] = [u.strip() for u in unit_input.split(",") if u.strip()]
int_time = int(study_time)
loops = math.ceil(int_time / 25)

# begin 
# add static stuff

def start_question_sequence() -> None:
    print("question sequence started")
    unit = ""
    if len(units) != 0:
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
        #implement a wait, and spawn a gravestone
    else:
        # implement correct scene
        w = 1
    studyTimer(10)

def studyTimer(secs: int) -> None:
    print("timer started")
    time.sleep(secs)
    stop()

def main() -> None:
    while lives > 0:
        threading.Thread(target=studyTimer, args=(10, ), daemon=True).start()
        update_life()
        root_start()
        start_question_sequence()

if __name__ == "__main__":
    main()