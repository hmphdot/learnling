# input_window.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys

class InputDialog(QDialog):
    def __init__(self, prompt="Enter something:"):
        super().__init__()
        self.setWindowTitle("Input Dialog")
        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setGeometry(720, 360, 500, 15)
        
        # Prompt label
        self.label = QLabel(prompt)
        layout.addWidget(self.label)
        # Input box
        self.input = QLineEdit()
        layout.addWidget(self.input)
        # Submit button
        self.button = QPushButton("Submit")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.accept_input)
        # Store user input
        self.user_input = None

    def accept_input(self):
        text = self.input.text().strip()
        if text:
            self.user_input = text
            self.accept()  # closes the dialog and returns control to caller

    def get_input(self):
        """Display the dialog modally and return the entered text."""
        self.exec()
        return self.user_input

class question_dialogue(QDialog):
    def __init__(self, prompt="Enter something:"):
        super().__init__()
        self.setWindowTitle("Question:")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setGeometry(710, 400, 200, 200)
        
        # Prompt label
        self.label = QLabel(prompt)
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        layout.addWidget(self.label)
        # Input box
        self.input = QLineEdit()
        layout.addWidget(self.input)
        # Submit button
        self.button = QPushButton("Submit")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.accept_input)
        # Store user input
        self.user_input = None

    def accept_input(self):
        text = self.input.text().strip()
        if text:
            self.user_input = text
            self.accept()  # closes the dialog and returns control to caller

    def get_input(self):
        """Display the dialog modally and return the entered text."""
        self.exec()
        return self.user_input