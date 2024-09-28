from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationBufferMemory
import json
from langchain.chains.openai_functions import create_structured_output_chain
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic.json import pydantic_encoder

from libs.model import QuestionList


embeddings = OpenAIEmbeddings()

prompt_template = PromptTemplate(
    input_variables=["context", "category", "query"],
    template="""
    Based on the context below, {query} a JSON object in the following format:
    {{
        questions: [
            "question": <generated question >,
            "options": [<generated options only dont use ก. ข. ค. ง.],
            "answer": <generated answer choie only in str "1","2","3","4">,
            "explanation": <generated explanation>,
            "question_category": {category}
        ]
    }}

    Context: {context}
    """,
    # output_parser=JsonOutputParser(pydantic_object=QuestionList),
)

llm = ChatOpenAI(model="gpt-4o")

# Step 5: Create LLMChain
chain = prompt_template | llm

# Function to run RAG


def run_rag_model(query, category, subcategory):
    vectorstore = FAISS.load_local(
        f'vector_db/{category}/{subcategory}', embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()

    # Retrieve relevant context
    docs = retriever.get_relevant_documents(query)
    context = " ".join([doc.page_content for doc in docs])

    # Generate structured output
    structured_output = chain.invoke({
        "context": context,
        "query": query,
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
    # print(json_output)
    strip_output = str(json_output.content.strip('```').strip('json'))
    print(strip_output)

    # Validate the output
    validated_output = validate_output(strip_output)
    if validated_output:
        return validated_output.model_dump_json(indent=2)

    return {"success": False}


if __name__ == "__main__":
    print(run("make 10 new exam questions have question ", "thai", "logic"))
