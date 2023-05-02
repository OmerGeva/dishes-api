FROM python:alpine3.17

WORKDIR ./app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=8000
CMD ["flask", "run", "--host=0.0.0.0"]