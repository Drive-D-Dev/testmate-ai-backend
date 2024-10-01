import os
from fastapi import Body, FastAPI, Response
from fastapi.responses import JSONResponse
import app.gen_redo as gen_redo
import app.gen_study_from_category as gen_study_from_category
import app.gen_multiple_exam as gen_multiple_exam

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "sk-********")

# app = create_service("mistake_gen:run")
# app = create_service("example:chain")

app = FastAPI()


@app.get("/")
async def hello():
    return Response(content="Hello From FastAPI")


@app.post("/gen_exam")
async def update_item(data: dict = Body(...)):
    query = data.get("query")
    category = data.get("category")
    subcategory = data.get("subcategory")

    results = gen_study_from_category.run(query, category, subcategory)

    return Response(content=results)


@app.post("/gen_multiple_exam")
async def generate_multiple_exam(data: dict = Body(...)):
    response = gen_multiple_exam.run(data)
    return JSONResponse(content=response)


@app.post("/gen_redo")
async def update_item(data: str = Body(...)):
    query = data
    print(query)
    results = gen_redo.run(query)

    return Response(content=results)
