FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENTRYPOINT ["uvicorn",  "api.main:app", "--root-path=/api", "--reload", "--host=0.0.0.0"]
