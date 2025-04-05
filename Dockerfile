FROM python:3.10

WORKDIR /archipelago-manager-node
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["fastapi", "run", "app/main.py"]
CMD ["--port", "8000"]
