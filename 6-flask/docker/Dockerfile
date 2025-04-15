FROM python:3.8

RUN pip install flask requests gunicorn

WORKDIR /6-flask

COPY ./web_app.py /6-flask/web_app.py

EXPOSE 5000

CMD ["gunicorn","web_app:app", \
      "-w", "4", "-b", "0.0.0.0:5000" \
    ]
