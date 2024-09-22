from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings

example_query = "สมมุติให้คุณเป็นอาจารย์ที่นำข้อสอบนี้ไปออกเป็นข้อสอบฉบับใหม่ของตัวเองที่มีเนื้อหา แต่ละข้อ คล้ายเคียงจากนี้ เช็คด้วยถ้าเหมือน เปลี่ยนโจทย์ เท่าจำนวนข้อที่มี พร้อมเฉลยแบบละเอียดที่เข้าใจง่าย เป็นภาษาไทย พร้อมตรวจทานวิธีคิดว่าคำตอบที่เฉลยละเอียดตรงกับคำตอบที่ถูกต้องหรือไม่ ถ้าไม่มีคำตอบจงสร้างโจทย์ข้อใหม่ที่มีคำตอบ และตอบให้อยู่ในรูป format json เช่น topic ( มีครั้งเดียวในไฟล์ละอยู่บนสุด เป็นชื่อหัวข้อของไฟล์นั้น ) , describe ( ถ้ามีคำคำสั่ง ขอคำอธิบายที่ชัดเจนและยาวพอที่จะอธิบายได้ครอบครุม ) และที่มีทุกข้อคือ question: , options , answer , explanation และ {type (  math, thai , eng , social)} โดยคำตอบเป็น ช้อย 1 2 3 4 และ เฉลยเป็น เลข 1 2 3 4  และ ตั้งหัวข้อจาก หัวข้อที่มีมาให้ ถ้าไม่มีให้ตั้งจากเนื้อหาโดยรวมแบบสั้นๆ และกระซับได้ใจความ และ สลับลำดับของข้อโจทย์และเรียงเลขข้อใหม่โดยเริ่มที่ 1 "

embeddings = OpenAIEmbeddings()

new_vector_store = FAISS.load_local(
    "faiss_index", embeddings, allow_dangerous_deserialization=True)

llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o")
memory = ConversationBufferMemory(
    memory_key='chat_history', return_messages=True)
chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type="stuff",
    retriever=new_vector_store.as_retriever(),
    memory=memory
)


# def run(url: str) -> str:
#     output = chain.run(query)
#     return output


# if __name__ == "__main__":
#     print(run("hello"))
