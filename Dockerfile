FROM python:3.10-slim
WORKDIR /app
COPY public /app/public
RUN mkdir -p /app/bot/database/data
RUN mkdir -p /app/bot/database
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/app
EXPOSE 8080
CMD ["python", "bot/main.py"]



