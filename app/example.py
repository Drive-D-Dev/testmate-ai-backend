
from langchain.llms import OpenAI
from langchain.chains import LLMMathChain

# from langchain_openai import ChatOpenAI

llm = OpenAI(temperature=0, model_name="gpt-3.5-turbo-instruct")
chain = LLMMathChain.from_llm(llm, verbose=True)
