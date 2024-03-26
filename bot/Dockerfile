FROM python:3.10-slim

WORKDIR /vacancy_bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "bot.py"]