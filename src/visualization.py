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

def display_question(question: str) -> None:
    ax.text(0.5, 0.5, question, fontsize=20, horizontalalignment='center', verticalalignment='center')
    plt.show()