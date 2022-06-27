FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
COPY RedditStreamObserver.py RedditStreamObserver.py
RUN pip3 install -r requirements.txt

CMD ["python3", "./RedditStreamObserver.py"]