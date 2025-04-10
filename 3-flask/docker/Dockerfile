FROM python:3.8

RUN pip install flask requests gunicorn

WORKDIR /3-flask

COPY ./3.py /3-flask/3.py

EXPOSE 5000

CMD ["gunicorn","3:app", \
      "-w", "4", "-b", "0.0.0.0:5000" \
    ]
