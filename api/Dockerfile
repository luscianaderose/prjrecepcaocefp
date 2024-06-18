FROM python:3.12

RUN pip install Flask

RUN apt-get update && apt-get install -y locales && \
    echo "pt_BR UTF-8" > /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=pt_BR

COPY . .

CMD [ "python", "app.py" ]

