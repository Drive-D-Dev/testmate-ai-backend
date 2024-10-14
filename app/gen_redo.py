from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.libs.validation import validate_question_list


prompt_template = PromptTemplate(
    input_variables=["query"],
    template="""
    Based on the context below, a JSON object in the following format:
    {{
        questions: [
            "question": <generated question >,
            "options": [<generated options only dont use ก. ข. ค. ง.],
            "answer": <generated answer choie only in str "1","2","3","4">,
            "explanation": <generated explanation>,
            "question_category": <generated category>
            "question_subcategory": <generated subcategory>
        ]
    }}
    Note that question_category and question_subcategory will be one of the input questions do not make new category and subcategory.

    Context: generate set of similar questions as these: {query}
    """,
)

llm = ChatOpenAI(model="gpt-4o")

chain = prompt_template | llm


def run(query: str) -> str:
    json_output = chain.invoke(
        {
            "query": query,
        }
    )
    strip_output = str(json_output.content.strip("```").strip("json"))
    print(strip_output)

    # Validate the output
    validated_output = validate_question_list(strip_output)
    if validated_output:
        return validated_output.model_dump_json(indent=2)

    return {"success": False}


if __name__ == "__main__":
    print(
        run(
            """{
  "questions": [
    {
      "question": "เข็ม : ? จักร : ผ้า",
      "options": [
        "สน",
        "ด้าย",
        "แทง",
        "เชือก"
      ],
      "answer": "2",
      "explanation": "เพราะเข็มต้องมีด้าย เสมือนกับจักรต้องมีผ้าถึงจะทำงานได้",
      "question_category": "thai"
    },
    {
      "question": "หมู่บ้าน : ตำบล ? : ?",
      "options": [
        "เปรี้ยว : เค็ม",
        "หลับ : ตื่น",
        "วัน : สัปดาห์",
        "ดู : โรงเรียน"
      ],
      "answer": "3",
      "explanation": "เพราะหมู่บ้านเป็นส่วนหนึ่งของตำบล เสมือนกับวันเป็นส่วนหนึ่งของสัปดาห์",
      "question_category": "thai"
    },
    {
      "question": "ดู : เห็น ? : ?",
      "options": [
        "ดม : หอม",
        "ชิม : รส",
        "หู : เสียง",
        "ฟัง : ได้ยิน"
      ],
      "answer": "4",
      "explanation": "เพราะการมองดูทำให้เห็น เสมือนกับการฟังทำให้ได้ยินเสียง",
      "question_category": "thai"
    }
  ]
"""
        )
    )
