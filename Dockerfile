FROM python:3.10.13

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001

CMD [ "python", "app.py" ]
