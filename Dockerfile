FROM alpine:latest

RUN apk add --no-cache python py-pip ca-certificates \
    && pip install Jinja2
ADD templated.py /templated.py
WORKDIR /data
CMD  python /templated.py
