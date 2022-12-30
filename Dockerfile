FROM python:3.8
WORKDIR /
COPY . .

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
