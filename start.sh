source bin/activate
gunicorn app:app --daemon
deactivate