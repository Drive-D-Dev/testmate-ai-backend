from langcorn import create_service
import os
from fastapi import Body, FastAPI, Response
import gen_redo
import gen_study_from_category

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "sk-********")

# app = create_service("mistake_gen:run")
# app = create_service("example:chain")

app = FastAPI()


@app.get("/")
async def hello():
    return Response(content="Hello From FastAPI")


@app.post("/gen_exam")
async def update_item(query: str, category: str, subcategory: str):
    results = gen_study_from_category.run(query, category, subcategory)

    return Response(content=results)


@app.post("/gen_redo")
async def update_item(query: str):
    results = gen_redo.run(query)

    return Response(content=results)
