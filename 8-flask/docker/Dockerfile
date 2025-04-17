FROM python:3.8

RUN pip install flask requests gunicorn flask_sqlalhemy

WORKDIR /8-flask

COPY ./web_app.py /8-flask/web_app.py
COPY ./duck_fox.py /8-flask/duck_fox.py
COPY ./models.py /8-flask/models.py

EXPOSE 5000

CMD ["gunicorn","web_app:app", \
      "-w", "4", "-b", "0.0.0.0:5000" \
    ]
