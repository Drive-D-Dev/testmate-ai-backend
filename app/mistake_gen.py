from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
import json
from typing import List
from langchain.chains.openai_functions import create_structured_output_chain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class Question(BaseModel):
    question: str = Field(..., description="The text of the question")
    options: List[str] = Field(...,
                               description="The available options for the question")
    answer: str = Field(..., description="The correct answer for the question")
    explanation: str = Field(..., description="The explanation for the answer")
    question_category: str = Field(...,
                                   description="The category of the question")


class QuestionList(BaseModel):
    questions: List[Question]


embeddings = OpenAIEmbeddings()

vectorstore = FAISS.load_local(
    'faiss_index', embeddings, allow_dangerous_deserialization=True)
# Define the Question model
# Create conversation chain
llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o")
memory = ConversationBufferMemory(
    memory_key='chat_history', return_messages=True)
conversation_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
    memory=memory
)
# query = "สมมุติให้คุณเป็นอาจารย์ที่นำข้อสอบนี้ไปออกเป็นข้อสอบฉบับใหม่ของตัวเองที่มีเนื้อหาแตกต่างจากนี้ 3 ข้อ พร้อมเฉลยแบบละเอียดที่เข้าใจง่าย เป็นภาษาไทย พร้อมตรวจทานวิธีคิดว่าคำตอบที่เฉลยละเอียดตรงกับคำตอบที่ถูกต้องหรือไม่ ถ้าไม่มีคำตอบจงสร้างโจทย์ข้อใหม่ที่มีคำตอบ และตอบให้อยู่ในรูป format json เช่น topic ( มีครั้งเดียวในไฟล์ละอยู่บนสุด เป็นชื่อหัวข้อของไฟล์นั้น ) , describe ( ถ้ามีคำคำสั่ง ขอคำอธิบายที่ชัดเจนและยาวพอที่จะอธิบายได้ครอบครุม ) และที่มีทุกข้อคือ question: , options , answer , explanation และ {type (  math, thai , eng , social)} โดยคำตอบเป็น ช้อย 1 2 3 4 และ เฉลยเป็น เลข 1 2 3 4  และ ตั้งหัวข้อจาก หัวข้อที่มีมาให้ ถ้าไม่มีให้ตั้งจากเนื้อหาโดยรวมแบบสั้นๆ และกระซับได้ใจความ"
result = conversation_chain()
answer = result["answer"]

# Setup LLM and the prompt template
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a world-class algorithm for extracting information in structured formats and ."),
        ("human",
         "Use the given format to extract information from the following input: {input}"),
        ("human", "Tip: Make sure to answer in the correct format"),
    ]
)

# Create the chain
chain = create_structured_output_chain(QuestionList, llm, prompt)

final_chain = chain | conversation_chain
