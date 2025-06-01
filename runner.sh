#!/bin/bash
python3 scraper/luxoft2.py&
python3 scraper/freelancer.py&
python3 scraper/runner.py&
python3 scraper/hhApi.py&
python3 scraper/salaries.py&
