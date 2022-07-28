from python:3.10-bullseye
RUN apt-get update &&  apt-get upgrade -y 
RUN apt install libpq-dev gcc -y
RUN python3.10 -m pip install --upgrade pip
COPY . /app
COPY localhost+3-key.pem /app/localhost+3-key.pem
COPY localhost+3.pem /app/localhost+3.pem
RUN pip install -r /app/requirements.txt
WORKDIR /app
EXPOSE 8000
CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
