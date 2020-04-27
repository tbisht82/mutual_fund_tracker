web: gunicorn mutual_fund_project.wsgi --log-file -
worker: celery -A mutual_fund_project worker -events -loglevel info
beat: celery -A mutual_fund_project beat