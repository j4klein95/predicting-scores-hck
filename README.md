# Predicting Hockey Scoring.

### Data Sources
* https://www.hockey-reference.com/

## Repository Format

```bash
├───cdk
│   ├───cdk
│   └───tests
│       └───unit
├───data
│   └───.ipynb_checkpoints
├───engineering
│   └───.ipynb_checkpoints
├───ML
│   └───.ipynb_checkpoints
└───storytelling
    └───.ipynb_checkpoints
```

## Requirements

* Python 3.10
* Selenium Web Driver
* Pandas
* Bokeh (for storytelling notebook)
* Ipywidgets
* Written for FireFox, use the *[Gecko Driver](https://github.com/mozilla/geckodriver/releases)*. If you do not want to use Firefox, rewrite data_scraper.py. Follow install instructions for your web driver.
* AWS CDK has its own Requirements.txt file.