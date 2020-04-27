# Mutual Fund Tracker

Django project to get the data for mutual fund. 2 cron jobs are scheduled using celery and redis.
1. One job will run in 12hr difference (8 AM, 8 PM), this job will download a csv file from provided URL and add new mutual funds to DB and featch it's historic data from provided API.
2. One job will run in 24hr (6PM), this job will get latest NAV value or all the historic data depending on the condition to the db. 

# Setup Steps:
1. Clone the repository
2. Create a virtual environment
3. Activate virtual environment
4. pip install -r requirements.txt
5. python manage.py migrate
6. python manage.py runserver

# For running the cron jobs:
1. Redis need to be installed on the system
2. In activated virtual environment run the following command:
celery -A mutual_fund_project worker -B -l INFO

# URLs:
1. http://127.0.0.1:xxxx
This url will automatically redirect the user to http://127.0.0.1:xxxx/mutualfunds/new/
2. http://127.0.0.1:xxxx/mutualfunds/new/
This url will display a form where we can add new ISIN to the DB
3. http://127.0.0.1:xxxx/mutualfunds/detail/<ISIN>
This url will show the historical data chart for provided ISIN

# Herouk URL:
1. https://mutual-fund-tracker.herokuapp.com/
