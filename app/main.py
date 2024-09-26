from langcorn import create_service
import os
from fastapi import Body, FastAPI, Response
import mistake_gen

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "sk-********")

# app = create_service("mistake_gen:run")
# app = create_service("example:chain")

app = FastAPI()


@app.get("/")
async def hello():
    return Response(content="Hello From FastAPI")


@app.post("/generate_mistake")
async def update_item(query: str, category: str):
    results = mistake_gen.run(query, category)

    return Response(content=results)
