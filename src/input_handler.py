import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt6.QtCore import QTimer

miliToSec = 1000
answerTimer = 5
secToMin = 60
quizLoopTimer = 25
course = ""
units = []
studyDuration = 0
currentUnit = 0
loopCount = 0
totalLoops = 0
currentState = "init_course"

app = QApplication(sys.argv)
window = QWidget()
boxLayout = QVBoxLayout()
inputBox = QLineEdit()

def displayText(titleText):
    window.setWindowTitle(titleText)
    inputBox.clear()

def inputProcessing():
    global course, units, studyDuration, currentState, totalLoops, loopCount, currentUnit

    userInput = inputBox.text().strip()
    if not userInput:
        return

    if currentState == "init_course":
        course = userInput
        currentState = "init_units"
        displayText(f"Which units would you like to study? (Use ,)")

    elif currentState == "init_units":
        units[:] = [u.strip() for u in userInput.split(",") if u.strip()]
        currentState = "init_time"
        displayText("How long do you want to study for? (Minutes)")

    elif currentState == "init_time":
        try:
            studyDurationValue = int(userInput)
            if studyDurationValue < quizLoopTimer:
                displayText("Oh hell naw, study longer!")
                return
            studyDuration = studyDurationValue
            totalLoops = studyDuration // quizLoopTimer
            loopCount = 0
            currentState = "studying"
            studyTimer()
        except ValueError:
            displayText("Please enter a valid number")

    elif currentState == "quiz":
        inputHandler(userInput)

def studyTimer():
    global studyTimerValue
    studyTimerValue = QTimer()
    studyTimerValue.setSingleShot(True)
    studyTimerValue.timeout.connect(unitQuestion)
    studyTimerValue.start(quizLoopTimer * secToMin * miliToSec)  # 25 mins in miliseconds

def unitQuestion():
    global loopCount, totalLoops, currentUnit, currentState, units, answerTimerValue

    if loopCount >= totalLoops:
        displayText("Good job keeping me alive!")
        currentState = "done"
        return

    if currentUnit >= len(units):
        currentUnit = 0

    unitName = units[currentUnit]
    displayText(f"Psssst question time!")
    currentState = "quiz"

    global answerTimerValue
    answerTimerValue = QTimer()
    answerTimerValue.setSingleShot(True)
    answerTimerValue.timeout.connect(noTime)
    answerTimerValue.start(answerTimer * secToMin * miliToSec)  # 5 mins in miliseconds

def inputHandler(userInput):
    global loopCount, currentUnit, currentState, answerTimerValue
    answerTimerValue.stop()
    loopCount += 1
    currentUnit += 1
    currentState = "studying"
    studyTimer()

def noTime():
    global loopCount, currentUnit, currentState
    loopCount += 1
    currentUnit += 1
    currentState = "studying"
    studyTimer()


window.setGeometry(900, 700, 500, 15)
boxLayout.addWidget(inputBox)
window.setLayout(boxLayout)

inputBox.returnPressed.connect(inputProcessing)

displayText("What is the course you want to study?")

window.show()
sys.exit(app.exec())
