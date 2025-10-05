import sys
import os
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

gravestones = []

def textPanel(image_path):
    """
    Creates a frameless transparent window that stitches two images together vertically.
    Returns a dictionary containing references to all key components.
    """
    

    # Ensure QApplication exists
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    pixmap = QPixmap(image_path)

    label = QLabel(window)
    label.setPixmap(pixmap)
    window.resize(pixmap.size())

    # Center the window on the screen
    screen_geometry = app.primaryScreen().availableGeometry()
    x = (screen_geometry.width() - window.width()) // 2
    y = (screen_geometry.height() - window.height()) // 2
    window.move(x, y)
    #3EB2FF
    # Exit button
    exit_button = QPushButton("x", window)
    exit_button.setStyleSheet("""
        QPushButton {
            background-color: rgba(255, 0, 0, 0);
            color: blue;
            border: none;
            font-weight: bold;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: rgba(255, 0, 0, 0);
        }
    """)
    exit_button.setFixedSize(30, 30)
    exit_button.move(window.width() - 33, 4)

    def on_exit():
        window.close()       
        clear_gravestones()  # Close all gravestones
        app.exit()

    exit_button.clicked.connect(on_exit)

    return {
        "app": app,
        "window": window,
        "label": label,
        "pixmap": pixmap
    }


def show_gravestone(x, y, multi):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    gravestone_path = os.path.join(BASE_DIR, "visuals", "statics", "gravestone.png")

    window = QWidget()
    window.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    pixmap = QPixmap(gravestone_path)
    label = QLabel(window)
    label.setPixmap(pixmap)
    window.resize(pixmap.size())
    window.move(x - 15*multi, y)
    window.show()

    return {
        "window": window,
        "label": label,
        "pixmap": pixmap
    }

def spawn_gravestone(x, y, multiplier):
    global gravestones

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    gravestone_path = os.path.join(BASE_DIR, "visuals", "statics", "gravestone.png")

    pixmap = QPixmap(gravestone_path)

    # Determine x position based on previous gravestone
    if gravestones:
        last = gravestones[-1]
        x = last["window"].x() - int(last["pixmap"].width() * multiplier)

    window = QWidget()
    window.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    label = QLabel(window)
    label.setPixmap(pixmap)
    window.resize(pixmap.size())
    window.move(x, y)
    window.show()

    gravestones.append({
        "window": window,
        "label": label,
        "pixmap": pixmap
    })


def clear_gravestones():
    global gravestones
    for grave in gravestones:
        grave["window"].close()
    gravestones = []
    
def bowl_static_image(image_path, x=None, y=None):

    app = QApplication.instance()
    if not app:
        raise RuntimeError("QApplication must be created before showing images.")

    window = QWidget()
    window.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    pixmap = QPixmap(image_path)
    label = QLabel(window)
    label.setPixmap(pixmap)
    window.resize(pixmap.size())

    # Default position → bottom-right corner
    screen_geometry = app.primaryScreen().availableGeometry()
    if x is None:
        x = screen_geometry.width() - pixmap.width() - 20  # 20 px margin
    if y is None:
        y = screen_geometry.height() - pixmap.height() - 20

    window.move(x, y)
    window.show()

    return {"window": window, "label": label, "pixmap": pixmap}


if __name__ == "__main__":
    app = QApplication(sys.argv)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    image_path = os.path.join(BASE_DIR, "visuals", "statics", "big_chat.png")

    if not os.path.exists(image_path) or not os.path.exists(image_path):
        raise FileNotFoundError(f"Cannot find images at:\n{image_path}\n{image_path}")

    ui = textPanel(image_path)
    ui["window"].show()

    bowl_image_path = os.path.join(BASE_DIR, "visuals", "statics", "bowl.png")
    bowl_ui = bowl_static_image(bowl_image_path)

    grav_ui = show_gravestone(x=1400, y=755)
    grav_ui["window"].show()

    sys.exit(app.exec())