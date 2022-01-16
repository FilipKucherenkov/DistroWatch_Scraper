import scrapy
import datetime


class DistrosSpider(scrapy.Spider):
    name = "distros"

    def start_requests(self):
        urls = []

        # Change this list to include whatever distros are needed. 
        distro_names = ["ubuntu", "redhat"]

        #Add all distros we want to crawl
        for name in distro_names:
            urls.append("https://distrowatch.com/index.php?distribution={}&release=all&month=all&year=all".format(name))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #Get distro name:
        page = response.url.split("distribution=")[-1].split("&")[0]
        
        #Create a txt file to store new distros:
        filename = f'distros-{page}.txt'

        #Find the previous month
        first_day_of_month = datetime.date.today().replace(day=1)
        last_month = first_day_of_month - datetime.timedelta(days=1)

        #Provide a date until which to scrape data
        #If no data is provided, default to previous month.
        date = getattr(self, 'date', last_month)


        #skip first as it contains unneeded info
        news = response.css("td.News1")[1::]
        with open(filename, 'w') as f:
            f.write("**********************************************************************************\n")
            for new in news:
                #Scrape the date of release
                rows = new.css("table.News > tr")
                date_field = rows[0].css("td.NewsDate")[0]
                date_text = date_field.css("::text").get()

                #Scrape the release name
                distro_name = rows[0].css("td.NewsHeadline")
                distro_link_field = distro_name.css("a")[1]
                distro_link_text = distro_link_field.css("::text").get()

                
                date_tokens =  date_text.split("-")
                input_date_tokens = date.split("-")

                #Write only the info which is after the provided as input date
                if int(input_date_tokens[0]) <= int(date_tokens[0]) and int(input_date_tokens[1]) <= int(date_tokens[1]):
                    f.write("Release date: {0} {1} \n".format(date_text, distro_link_text))
                    f.write("**********************************************************************************\n")
        
            