#!/bin/bash
python3 luxoft/luxoft2.py&
python3 scraper/freelancer.py&
python3 scraper/runner.py&
python3 scraper/hhApi.py&
python3 salaries/salaries.py&
