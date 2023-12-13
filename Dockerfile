FROM python:3.9-slim-buster
# Install JRE
RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2 && \
    apt-get update &&\
    apt-get install -y --no-install-recommends openjdk-11-jre && \
    apt-get install ca-certificates-java -y && \
    apt-get clean && \
    update-ca-certificates -f;
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
## Code
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
