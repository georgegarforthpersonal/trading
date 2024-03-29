FROM python:3.9.12

EXPOSE 8501

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app.py .

ENTRYPOINT [ "streamlit", "run"]
CMD ["app.py"]