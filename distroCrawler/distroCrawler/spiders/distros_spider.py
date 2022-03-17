import scrapy
from scrapy.mail import MailSender
import logging
import datetime
import os

class DistrosSpider(scrapy.Spider):
    name = "distros"
    are_distros_updated = {}
    
    #Find the previous month
    first_day_of_month = datetime.date.today().replace(day=1)
    last_month = first_day_of_month - datetime.timedelta(days=1)
    
    target_date = ""

    def start_requests(self):
        urls = []
        # Change this list to include whatever distros are needed. 
        distro_names = ["ubuntu", "redhat", "sle", "centos", "debian", "oracle", "fedora"]

        #Add all distros we want to crawl
        for name in distro_names:
            urls.append("https://distrowatch.com/index.php?distribution={}&release=all&month=all&year=all".format(name))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #Get distro name:
        page = response.url.split("distribution=")[-1].split("&")[0]

        #Provide a date until which to scrape data
        #If no data is provided, default to previous month.
        self.target_date = getattr(self,'date', self.last_month.strftime("%Y-%m-%d"))

        #Create a txt file to store new distros:
        filename = f'distros-{page}.txt'
        dir_name = 'distroData' 
        full_path = os.path.join(dir_name, filename)
        
        #Dict in the form {distroName:isUpdated}
        self.are_distros_updated.update({filename: False})

        with open(full_path, 'w') as f:            
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
                input_date_tokens = self.target_date.split("-")
                
                if distro_link_field == None:
                    continue

                #Write only the info which is after the provided as input date
                if int(input_date_tokens[0]) <= int(date_tokens[0]) and int(input_date_tokens[1]) <= int(date_tokens[1]):
                    self.are_distros_updated[filename] = True
                    if date_text != "" and distro_link_text != "": 
                        f.write("**********************************************************************************\n")
                        f.write("Release date: {0} {1} \n".format(date_text, distro_link_text))
                        f.write("**********************************************************************************\n")
                    else:
                        logging.debug("No new info for {}".format(distro_name))
        

    def construct_email_body(self, updated_file_names):
        email_body = "<b>The following distros have been released:</b><ul>"
        for filename in os.scandir('distroData'):
            if filename.is_file() and filename.name in updated_file_names:
                with open(filename.path, 'r') as f:
                    for line in f.readlines():
                        if "*" not in line:
                            email_body += "<li>" + line + "</li>"
        email_body += "</ul>"
        return email_body


    def closed(self, reason):
        # will be called when the crawler process ends
        # Keep only modified files
        updated_file_names = dict(filter(lambda file: file[1],self.are_distros_updated.items()))

        if len(updated_file_names) == 0:
            logging.debug("There aren't any new distro releases - No need to send an email...")
            return 

        email_body = self.construct_email_body(updated_file_names)
        print(email_body)
        mailer = MailSender(mailfrom="chatroomsmail@gmail.com",smtphost="smtp.gmail.com",smtpport=465,smtpuser="chatroomsmail@gmail.com",smtppass="G1antP1g", smtpssl=True)
        return mailer.send(to=["f.kucherenkov@gmail.com"],mimetype='text/html', subject="Newly released Linux distros from {} to {}".format(self.target_date, datetime.date.today().strftime("%Y-%m")),body="{}".format(email_body))
    
    