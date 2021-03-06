# DistroWatch_Scraper

* Simple Python Scraper used for extracting data from https://distrowatch.com for new **Linux** distributions.
* Uses [Scrapy](https://docs.scrapy.org/en/latest/) - look for more information on how to extend the project.

## Guide for setting up the project on MacOS:
* First Setup a virtual environment by running the following commands:
```
pip install virtualenv
virtualenv venv
```
* Use the following commands to activate/deactivate:
```
source venv/bin/activate # to activate the venv
deactivate # deactivate
```

* Inside the venv run the following command to install **scrapy**
```
pip install Scrapy
```

* Go to the top level folder of the scraper using the following command:
```
cd distroCrawler/
```
## Guide for Setting up the project on Ubuntu 14.04 or above:
* First Setup a virtual environment by running the following commands:
```
sudo apt install python3-venv
python3 -m venv distroScraper-venv
```
* Use the following commands to activate/deactivate:
```
source distroScraper-venv/bin/activate # activate the venv
deactivate # deactivate
```
* Inside the venv run the following commands to install **scrapy**
```
sudo apt-get install python3 python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
pip install scrapy
```

## Run the following command to scrape data:
* Note: **input_date** is the date until which you want to extract information.
* For example - "2021-3", which will scrape data for releases after and including March 2021
```
scrapy crawl distros -a date=<input_date> 
```
* If no arguments are provided, the default date is the previous month.
```
scrapy crawl distros 
```

* Data for each distribution is extracted in a separate txt file and placed in the **distroData** folder.

* Can also be configured to send an email to a specific address containing the crawled data. 

<img width="1361" alt="Screen Shot 2022-03-17 at 01 37 18" src="https://user-images.githubusercontent.com/72323426/158719348-d277d439-ef29-432e-94a3-5f119c0d2205.png">

