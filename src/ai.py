from google import genai
from google.genai import types
from dotenv import load_dotenv
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt

# get env variables, edit tex stuff
load_dotenv()
client = genai.Client()

# TeX settings for output window
plt.rcParams["text.usetex"] = True
plt.rcParams['toolbar'] = 'None'
fig, ax = plt.subplots()
ax.axis('off')
manager = fig.canvas.manager
manager.set_window_title("Question Time!")
manager.window.setGeometry(1200, 630, 500, 200)

def generate_question(course: str, unit: str) -> str:
    qna = "Course: " + course + ", Unit: " + unit
    input_params = "Create a question that can be solved in 3 minutes for someone currently studying the following topics, returning only the question string. It should be written in LaTeX notation if involving equations. -> " + qna
    question = client.models.generate_content(
        model="gemini-2.5-flash", contents=input_params
    )
    return question.text

def test_answer(question: str, answer: str) -> bool:
    pair = "Q: " + question + " A: " + answer
    answer_check = client.models.generate_content(
        model="gemini-2.5-flash", contents="Return one lowercase character (y/n) based on if this answer is correct for the given question: " + pair,
        config=types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_budget=0)) # save tokens
    )
    if answer_check.text == 'y':
        return True
    return False

# below is all test stuff
# c = "calculus 3 or math 251"
# u = "partial derivatives"
q = r"$$ \int\limits_a^bf(x)dx + \frac{\Delta}{\sigma} $$"

ax.text(0.5, 0.5, q, fontsize=20, horizontalalignment='center', verticalalignment='center')
plt.show()

answer = input()
correct = True # test_answer(q, answer)
if correct == True:
    print("correct")
else:
    print("incorrect")