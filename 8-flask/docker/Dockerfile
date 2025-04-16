FROM python:3.8

RUN pip install flask requests gunicorn

WORKDIR /8-flask

COPY ./web_app.py /8-flask/web_app.py

EXPOSE 5000

CMD ["gunicorn","web_app:app", \
      "-w", "4", "-b", "0.0.0.0:5000" \
    ]
