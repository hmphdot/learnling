from google import genai
from google.genai import types
from dotenv import load_dotenv

# get env variables, edit tex stuff
load_dotenv()
client = genai.Client()

def generate_question(course: str, unit: str) -> str:
    qna = "Course: " + course + ", Unit: " + unit
    input_params = "Create a question that can be solved in 3 minutes for someone currently studying the following topics, returning only the question string. Add line breaks every 60 characters. -> " + qna
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