# quick_chat (quick_chat)
#### Live Chat with Stock Bot
_________

### Backend setup
docker-compose up -d
pip3 install -r requirements.txt

python3 manage.py makemigrations
python3 manage.py migrate

python manage.py collectstatic

run server:
daphne -b localhost -p 9000 quick_chat.asgi:application

### Web app setup
`cd front`

`yarn install`

`quasar build -m spa`

`quasar serve dist/spa`
_____
it will serve the frontend at port 4000
the backend will be served at port 9000
