# Predicting Hockey Scoring.

### Data Sources
* https://www.hockey-reference.com/

## Repository Format

```bash
├── data
   ├── 'location where stats are written once data_scraper is run.'
├── engineering
   ├── data_scraper.py
└── .gitignore
```

## Requirements

* Python 3.10
* Selenium Web Driver
* Pandas
* Written for FireFox, use the *[Gecko Driver](https://github.com/mozilla/geckodriver/releases)*. If you do not want to use Firefox, rewrite data_scraper.py. Follow install instructions for your web driver.
