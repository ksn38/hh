@echo off
python luxoft/luxoft2.py
python scraper/runner.py
python scraper/freelancer.py
python scraper/hhApi.py
python salaries/salaries.py
pause
