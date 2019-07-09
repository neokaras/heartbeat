FROM alpine:latest
RUN apk update && apk add python3 && apk add --update tzdata
ENV TZ=America/New_York
WORKDIR /data
ADD /app/heartbeat.py heartbeat.py
ADD /app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /data
EXPOSE 80
ENTRYPOINT ["python3", "heartbeat.py"]
CMD ["--port=80"]
