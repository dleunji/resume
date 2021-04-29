FROM python:3.7-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["opyrator", "launch-ui", "app:gen_resume"]