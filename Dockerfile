FROM python:3.13

WORKDIR /project

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY *.py ./

ENTRYPOINT ["python"]

CMD ["main.py"]
