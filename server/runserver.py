from waitress import serve
from django.core.management import call_command
from config.wsgi import application

if __name__ == '__main__':
    call_command('makemigrations')
    call_command('migrate')
    serve(application, host='0.0.0.0', port=8000)
