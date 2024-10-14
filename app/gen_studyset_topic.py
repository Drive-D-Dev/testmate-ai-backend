from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from app.libs.validation import validate_topic
import json

prompt_template = PromptTemplate(
    input_variables=["query"],
    template="""
    Base on the context below, a JSON object in the following format in thai language:
    {{
        topic: generated topic,
        describe: generated topic description
    }}
    
    Context: generate the question set topic and topic description as given example below from these question set: {query}
    Example of topic and description:
    {{
    [
        {{
            topic: การสนทนาในชีวิตประจำวัน,
            describe: ข้อสอบนี้ประกอบด้วยสถานการณ์ต่างๆในชีวิตประจำวัน และถามเกี่ยวกับการสนทนาในสถานการณ์นั้นๆ พร้อมตัวเลือก 4 ข้อ ให้เลือกคำตอบที่ถูกต้องและเหมาะสมที่สุด,
        }},
        {{
            topic: Grammar and Vocabulary Exam,
            describe: Complete the following passages by choosing the best answer. Each question has four options. Select the correct one.,
        }},
        {{
            topic: ความรู้ความสามารถด้านภาษาอังกฤษที่เกี่ยวข้องกับการปฏิบัติงาน,
            describe: ข้อสอบชุดนี้ประกอบด้วยคำถามเกี่ยวกับการใช้ภาษาอังกฤษในบริบทต่าง ๆ ทั้งในแง่ของไวยากรณ์ คำศัพท์ และการสื่อสารที่เกี่ยวข้องกับการปฏิบัติงาน พร้อมเฉลยที่อธิบายละเอียดและเข้าใจง่าย,
        }},
        {{
            topic: การทดสอบความรู้ทั่วไป,
            describe: ข้อสอบฉบับนี้ประกอบด้วยคำถาม 20 ข้อที่ครอบคลุมเนื้อหาที่หลากหลาย เพื่อทดสอบความรู้ทั่วไปของผู้เข้าสอบ กรุณาเลือกคำตอบที่ถูกต้องที่สุดจากตัวเลือกที่ให้มา,
        }},
        {{
            topic: ชุดข้อสอบคณิตศาสตร์และภาษาอังกฤษ,
            describe: ชุดข้อสอบเตรียมความพร้อมภาษาอังกฤษและคณิตศาสตร์,
        }},
        {{
            topic: ชุดข้อสอบคณิตศาสตร์
            describe: ประกอบไปด้วย เซ็ต จำนวนจริง และ อสมการ
        }}
    ]
    }}
    """,
)

llm = ChatOpenAI(model="gpt-4o")

chain = prompt_template | llm


def run(query: list) -> dict:
    query_str = json.dumps(query)

    json_output = chain.invoke(
        {
            "query": query_str,
        }
    )
    strip_output = str(json_output.content.strip("```").strip("json"))
    validate_output = validate_topic(strip_output)
    if validate_output:
        return validate_output.model_dump()
    return {"success": False}


example_questions = [
    {
        "question": "ดินสอ : กระดาษ ? : ?",
        "options": ["ปากกา : สมุด", "ยางลบ : น้ำ", "ไม้บรรทัด : ผ้า", "ปากกา : กระดาษ"],
        "answer": "1",
        "explanation": "เพราะดินสอต้องการกระดาษในการเขียน เสมือนกับปากกาต้องการสมุดในการเขียน",
        "question_category": "thai",
        "question_subcategory": "analogy",
    },
    {
        "question": "กำแพง : บ้าน ? : ?",
        "options": ["หนังสือ : ห้องสมุด", "จอภาพ : คอมพิวเตอร์", "ล้อ : รถยนต์", "ไม้ : ป่า"],
        "answer": "3",
        "explanation": "เพราะกำแพงเป็นส่วนหนึ่งของบ้าน เสมือนกับล้อเป็นส่วนหนึ่งของรถยนต์",
        "question_category": "thai",
        "question_subcategory": "analogy",
    },
    {
        "question": "น้ำ : ทะเล ? : ?",
        "options": ["ปลา : แม่น้ำ", "ทราย : ชายหาด", "ไม้ : ป่า", "ดิน : ภูเขา"],
        "answer": "2",
        "explanation": "เพราะน้ำเป็นส่วนประกอบของทะเล เสมือนกับทรายเป็นส่วนประกอบของชายหาด",
        "question_category": "thai",
        "question_subcategory": "analogy",
    },
    {
        "question": "(d/dx) cos(3x^3) = ?",
        "options": ["1", "9x^2", "-9x^2 sin(3x^3)", "not from above"],
        "answer": "3",
        "explanation": " = -9x^2 sin(3x^3)",
        "question_category": "math",
        "question_subcategory": "calculus",
    },
]
