from google import genai
from dotenv import load_dotenv

# get env variables
load_dotenv()
client = genai.Client()

def generate_question(course: str, unit: str) -> str:
    qna = "Course: " + course + ", Unit: " + unit
    input_params = "Create a question that can be solved in 3 minutes for someone currently studying the following topics, returning only the question string -> " + qna
    question = client.models.generate_content(
        model="gemini-2.5-flash", contents=input_params
    )    
    return question

def test_answer(question: str, answer: str) -> bool:
    pair = "Q: " + question + " A: " + answer
    answer_check = client.models.generate_content(
        model="gemini-2.5-flash", contents="Return one lowercase character (y/n) based on if this answer is correct for the given question: " + pair
    )
    if answer_check == 'y':
        return True
    return False

c = "calculus 3 or math 251"
u = "partial derivatives"
q = print(generate_question(c, u))
answer = input(q)
correct = test_answer(q, answer)
if correct == True:
    print("correct")
else:
    print("incorrect")