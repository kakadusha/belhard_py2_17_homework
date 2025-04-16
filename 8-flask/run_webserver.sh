############################
# ручной запуск
#
# на сервере запускать: 
#   > cd docker
#   > docker-compose up
###

#source $(pwd)/../venv/bin/activate
source $(pwd)/../py11_3_env/bin/activate
# gunicorn web_app:app -w 4 -b 134.209.194.133:5000
gunicorn web_app:app -w 4 -b 127.0.0.1:5000