FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apk update && apk add --no-cache gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev
RUN pip3 install --upgrade pip
RUN pip3 install virtualenv

RUN virtualenv -p python3 venv
ENV PATH=/venv/bin:$PATH

RUN mkdir -p /source/starlette_context
WORKDIR /source/starlette_context

ENV PYTHONPATH=/source/starlette_context
COPY requirements* ./

RUN pip3 install -r requirements-dev.txt

ADD tests ./
ADD starlette_context ./

