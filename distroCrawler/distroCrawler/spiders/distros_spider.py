
import scrapy

import datetime
import os

class DistrosSpider(scrapy.Spider):
    name = "distros"
    are_distros_updated = {}
    
    def start_requests(self):
        urls = []

        # Change this list to include whatever distros are needed. 
        distro_names = ["ubuntu", "redhat", "sle", "centos", "oracle", "debian", "fedora"]

        #Add all distros we want to crawl
        for name in distro_names:
            urls.append("https://distrowatch.com/index.php?distribution={}&release=all&month=all&year=all".format(name))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #Get distro name:
        page = response.url.split("distribution=")[-1].split("&")[0]
        
        #Find the previous month
        first_day_of_month = datetime.date.today().replace(day=1)
        last_month = first_day_of_month - datetime.timedelta(days=1)

        #Provide a date until which to scrape data
        #If no data is provided, default to previous month.
        date = getattr(self, 'date', last_month.strftime("%Y-%m-%d"))
        
        #Create a txt file to store new distros:
        filename = f'distros-{page}.txt'
        save_path = 'distroData' 
        full_path = os.path.join(save_path, filename)
        
        #Add distro file name
        self.are_distros_updated.update({filename: False})

        with open(full_path, 'w') as f:
            # f.write("**********************************************************************************\n")
            # f.write("Last modified: {}\n".format(datetime.date.today()))
            f.write("**********************************************************************************\n")
            #skip first as it contains unneeded info
            news = response.css("td.News1")[1::]

            for new in news:
                #Scrape the date of release
                rows = new.css("table.News > tr")
                date_field = rows[0].css("td.NewsDate")[0]
                date_text = date_field.css("::text").get()

                #Scrape the release name
                distro_name = rows[0].css("td.NewsHeadline")
                distro_link_field = None
                if len(distro_name.css("a")) > 1: 
                    distro_link_field = distro_name.css("a")[1]
                    distro_link_text = distro_link_field.css("::text").get()
                
                date_tokens =  date_text.split("-")
                 
                input_date_tokens = date.split("-")
                
                if distro_link_field == None:
                    continue
                #Write only the info which is after the provided as input date
                if int(input_date_tokens[0]) <= int(date_tokens[0]) and int(input_date_tokens[1]) <= int(date_tokens[1]):
                    self.are_distros_updated[filename] = True
                    f.write("Release date: {0} {1} \n".format(date_text, distro_link_text))
                    f.write("**********************************************************************************\n")
        
    def closed(self, reason):
        # will be called when the crawler process ends
        # Keep only modified files
        updated_file_names = dict(filter(lambda file: file[1],self.are_distros_updated.items()))
        if len(updated_file_names) is 0:
            print("No new releases...")
            return

        #File can be used to send an email
        email = open("newly_released.txt", "w")
        email.write("The following distros have been released: \n")
        for filename in os.scandir('distroData'):
            if filename.is_file() and filename.name in updated_file_names:
                with open(filename.path, 'r') as f:
                    email.write(f.read())
    
    