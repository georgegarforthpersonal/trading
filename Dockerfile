FROM python:3.9.12

EXPOSE 8080

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app.py .

ENTRYPOINT [ "streamlit", "run", "--server.port=8080"]
CMD ["app.py"]