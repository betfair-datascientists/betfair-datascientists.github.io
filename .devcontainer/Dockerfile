FROM squidfunk/mkdocs-material:latest

RUN apk add --no-cache libc-dev linux-headers zeromq-dev gcc g++
RUN pip install --no-cache-dir markdown-include cython nbconvert
RUN pip install --no-cache-dir mknotebooks