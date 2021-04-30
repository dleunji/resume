FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
#CMD ["opyrator", "launch-ui", "app:generate_resume"]
CMD ["/bin/bash"]