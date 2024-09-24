from typing import List
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import BaseOutputParser


system_prompt = "you are a exam question generating tutor, **you always answer in thai language**. **you always answer in json format** you are task with generating question from 4 categories (math, thai, english, legal) each question consisted of a question, 4 options, 1 correct answer and an explanation."

format_prompt = """
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
{ "properties": { "question": { "title": "Question", "description": "The question text", "type": "string" }, "options": { "title": "Options", "description": "The list of answer options", "type": "array", "items": { "type": "string" } }, "answer": { "title": "Answer", "description": "The correct answer", "type": "string" }, "explanation": { "title": "Explanation", "description": "The explanation of the correct answer", "type": "string" }, "question_category": { "title": "Question Category", "description": "The category of the question", "type": "string" } }, "required": ["question", "options", "answer", "explanation", "question_category"] }
"""


class Question(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: str
    question_category: str


memory = ConversationBufferMemory(
    memory_key='chat_history', return_messages=True)

embeddings = OpenAIEmbeddings()

store = FAISS.load_local(
    "faiss_index", embeddings, allow_dangerous_deserialization=True)

retriever = store.as_retriever(
    search_type="similarity",  # Also test "similarity", "mmr"
    search_kwargs={"k": 1},)

llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo-16k")
structured_llm = llm.with_structured_output(Question)


converstion = ConversationalRetrievalChain.from_llm(
    llm=structured_llm,
    retriever=retriever,
    memory=memory,
)

chain = converstion


def run(query: str) -> str:
    # output = chain.invoke("generate 1 question in math catergory",)
    output = chain.invoke(
        # Add the custom parser here })
        {"question": query, "chat_history": [
            system_prompt, format_prompt]})
    print(output)
    output = structured_llm.invoke(f"turn this into JSON format ${output}")
    print(output)

    return output


if __name__ == "__main__":
    print("--------------------------")
    print(run("generate 3 question in math catergory"))
    # print(structured_llm.invoke("generate 3 question"))
