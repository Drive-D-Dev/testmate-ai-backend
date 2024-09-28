
from libs.model import QuestionList


def validate_question_list(json_data):
    try:
        validated_output = QuestionList.model_validate_json(json_data)
        return validated_output
    except Exception as e:
        print(f"Validation error: {e}")
        return None
