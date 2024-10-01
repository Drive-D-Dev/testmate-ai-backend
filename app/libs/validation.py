from app.libs.model import QuestionList, Topic


def validate_question_list(json_data):
    try:
        validated_output = QuestionList.model_validate_json(json_data)
        return validated_output
    except Exception as e:
        print(f"Validation error: {e}")
        return None


def validate_topic(json_data):
    try:
        validated_output = Topic.model_validate_json(json_data)
        return validated_output
    except Exception as e:
        print(f"Validation error: {e}")
        return None
