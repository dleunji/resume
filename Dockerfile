FROM python:3.7-slim
WORKDIR /app
COPY . .
EXPOSE 8501
RUN pip install opyrator
CMD ["streamlit", "run", "app.py"]