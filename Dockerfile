FROM python:3.8
RUN mkdir -p /app
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get install -y && \
    apt-get install -y apt-utils wget
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["opyrator", "launch-ui", "app:generate_resume", "--port", "8501"]