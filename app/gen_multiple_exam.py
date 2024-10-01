import app.gen_study_from_category
import app.gen_studyset_topic
import json
from fastapi.encoders import jsonable_encoder
from app.gen_studyset_topic import example_questions


def run(body: dict):
    category_object = body.get("data")
    amount: int = body.get("amount")
    each_category: int = amount // len(category_object)
    extra = amount % len(category_object)
    is_first = True
    questions = []

    for item in category_object:
        category = item.get("category")
        subcategory = item.get("subcategory")
        if is_first:
            query = f"make {each_category + extra} questions"
            is_first = False
        else:
            query = f"make {each_category} questions"

        result = app.gen_study_from_category.run(query, category, subcategory)
        result_json = json.loads(result)

        for question in result_json.get("questions"):
            questions.append(question)
    topic = app.gen_studyset_topic.run(questions)
    response = jsonable_encoder(
        {
            "topic": topic.get("topic"),
            "describe": topic.get("describe"),
            "questions": questions,
        }
    )
    return response
