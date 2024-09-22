
FROM python:3.12


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-deps --no-cache-dir --upgrade -r requirements.txt


COPY ./app /code/app
WORKDIR /code/app

CMD ["uvicorn", "main:app", "--port", "80"]