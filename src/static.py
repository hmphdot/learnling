import sys
import os
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt

gravestones = []

def stitchedWindow(image_path1, image_path2):
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

    # Load and stitch images
    pixmap1 = QPixmap(image_path1)
    pixmap2 = QPixmap(image_path2)

    width = max(pixmap1.width(), pixmap2.width())
    height = pixmap1.height() + pixmap2.height()
    stitched = QPixmap(width, height)
    stitched.fill(Qt.GlobalColor.transparent)

    painter = QPainter(stitched)
    painter.drawPixmap(0, 0, pixmap1)
    painter.drawPixmap(0, pixmap1.height(), pixmap2)
    painter.end()

    label = QLabel(window)
    label.setPixmap(stitched)
    window.resize(stitched.size())

    # Center the window on the screen
    screen_geometry = app.primaryScreen().availableGeometry()
    x = (screen_geometry.width() - window.width()) // 2
    y = (screen_geometry.height() - window.height()) // 2
    window.move(x, y)

    # Exit button
    exit_button = QPushButton("", window)
    exit_button.setStyleSheet("""
        QPushButton {
            background-color: rgba(255, 0, 0, 0);
            color: 3EB2FF;
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
        window.close()       # Close the stitched window
        clear_gravestones()  # Close all gravestones
        app.quit()

    exit_button.clicked.connect(on_exit)

    return {
        "app": app,
        "window": window,
        "label": label,
        "exit_button": exit_button,
        "stitched_pixmap": stitched,
        "pixmap1": pixmap1,
        "pixmap2": pixmap2,
    }


def show_gravestone(x=200, y=200):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    gravestone_path = os.path.join(BASE_DIR, "visuals", "statics", "gravestone.png")

    window = QWidget()
    window.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    pixmap = QPixmap(gravestone_path)
    label = QLabel(window)
    label.setPixmap(pixmap)
    window.resize(pixmap.size())
    window.move(x, y)
    window.show()

    return {
        "window": window,
        "label": label,
        "pixmap": pixmap
    }


def spawn_gravestone(x=500, y=200, multiplier=1.5):
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


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    image1_path = os.path.join(BASE_DIR, "visuals", "statics", "big_chat.png")
    image2_path = os.path.join(BASE_DIR, "visuals", "statics", "small_chat.png")

    if not os.path.exists(image1_path) or not os.path.exists(image2_path):
        raise FileNotFoundError(f"Cannot find images at:\n{image1_path}\n{image2_path}")

    # Show stitched window in the center
    ui = stitchedWindow(image1_path, image2_path)
    ui["window"].show()

    # Example gravestones
    grav_ui = show_gravestone(x=1400, y=755)
    grav_ui["window"].show()

    sys.exit(ui["app"].exec())
