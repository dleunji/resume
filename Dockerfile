FROM tensorflow/tensorflow:1.15.5-gpu-py3
RUN mkdir -p /app
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt-get install -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
CMD ["opyrator", "launch-ui", "app:generate_resume", "--port", "8501"]