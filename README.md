# DistroWatch_Scraper

* Simple Pyhon Scraper used for extracting data from https://distrowatch.com for new **Linux** distributions.
* Uses [Scrapy](https://docs.scrapy.org/en/latest/), look for more information on how to extend the project.


## Guide for setting up the project:
* First install **scrapy** by running the following command: 
```
pip install Scrapy
```

* Go to the top level folder of the scraper using the following command:
```
cd distroCrawler/
```

* Run the following command to scrap data:
* Note: **input_date** is the date until which you want to extract information.
* If no arguments are provided, the default date is the previous month.
```
scrapy crawl distros -a date=<input_date> 
```

* Data for each distribution is extracted in a separate txt file and placed in the **distroData** folder.

