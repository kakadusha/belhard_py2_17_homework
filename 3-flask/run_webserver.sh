# ручной запуск
#
# на сервере запускать 
#   cd docker
#   docker-compose up
###
source ../venv/bin/activate
gunicorn 3:app -w 4 -b 134.209.194.133:8000