from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
import json
from typing import List, Optional
from langchain.chains.openai_functions import create_structured_output_chain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic.json import pydantic_encoder


class Question(BaseModel):
    question: Optional[str] = Field(...,
                                    description="The text of the question")
    options: Optional[List[str]] = Field(...,
                                         description="The available options for the question")
    answer: Optional[str] = Field(...,
                                  description="The correct answer for the question")
    explanation: Optional[str] = Field(...,
                                       description="The explanation for the answer")
    question_category: Optional[str] = Field(...,
                                             description="The category of the question")


class QuestionList(BaseModel):
    questions: List[Question]


embeddings = OpenAIEmbeddings()

prompt_template = PromptTemplate(
    input_variables=["context", "category"],
    template="""
    Based on the context below, generate a JSON object in the following format:
    {{
        questions: [
            "question": <generated question>,
            "options": [<generated options>],
            "answer": <generated answer>,
            "explanation": <generated explanation>,
            "question_category": {category}
        ]
    }}

    Context: {context}
    """,
    # output_parser=JsonOutputParser(pydantic_object=QuestionList),
)

llm = ChatOpenAI(model="gpt-4o-mini")

# Step 5: Create LLMChain
chain = prompt_template | llm

# Function to run RAG


def run_rag_model(query, category, subcategory):
    vectorstore = FAISS.load_local(
        f'vector_db\{category}\{subcategory}', embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()

    # Retrieve relevant context
    docs = retriever.get_relevant_documents(query)
    context = " ".join([doc.page_content for doc in docs])

    # Generate structured output
    structured_output = chain.invoke({
        "context": context,
        "category": category
    })
    return structured_output


def validate_output(json_data):
    try:
        validated_output = QuestionList.model_validate_json(json_data)
        return validated_output
    except Exception as e:
        print(f"Validation error: {e}")
        return None


def run(query: str, category: str, subcategory: str) -> str:
    json_output = run_rag_model(query, category, subcategory)
    print(json_output)
    strip_output = str(json_output.content.strip('```').strip('json'))
    print(strip_output)

    # Validate the output
    validated_output = validate_output(strip_output)
    if validated_output:
        return validated_output.model_dump_json(indent=2)

    return {"success": False}


if __name__ == "__main__":
    print(run("generate 3 question", "math", "data_analysis"))
