import requests
import base64

url = "http://192.168.137.1:8000/get_questions/"


def send_request_(file, start, end, difficulty):
    with open(file, "rb") as file:
        book_data = file.read()

    encoded_book_data = base64.b64encode(book_data).decode("utf-8")

    payload = {
        "book": encoded_book_data,
        "spage": start,
        "epage": end,
        "qnumber": 10,
        "difficulty": difficulty,
    }

    response = requests.post(url, json=payload)
    questions = response.json()
    print(questions)
    return questions["questions"]
