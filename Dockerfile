FROM python:3.9
WORKDIR /wordle/

COPY requirements/prod.txt requirements.txt
RUN pip install -r requirements.txt

COPY alembic alembic
COPY alembic.ini .
COPY app app
COPY server.py .

CMD python server.py