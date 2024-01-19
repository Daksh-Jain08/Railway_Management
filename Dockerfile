FROM python:3

WORKDIR /usr/src/app/

ENV PYTHONUNBUFFERED=1
COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app/

# ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]