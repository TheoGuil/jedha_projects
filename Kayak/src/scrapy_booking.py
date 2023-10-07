import os
import logging
import scrapy
import json
import sys
import datetime
from scrapy.crawler import CrawlerProcess


class ScrapyBooking(scrapy.Spider):
    name = "booking"

    start_urls = ["https://www.booking.com/index.fr.html"]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                "ss": city,
                "ssne": city,
                "ssne_untouched": city,
                "checkin": (datetime.datetime.now() + datetime.timedelta(days=5)).strftime("%Y-%m-%d"),
                "checkout": (datetime.datetime.now() + datetime.timedelta(days=6)).strftime("%Y-%m-%d"),
            },
            callback=self.after_search,
        )

    # Callback used after search
    def after_search(self, response):
        print(response.url)

        # with open("./src/rouen-booking.html", "w") as fp:
        #     fp.write(response.text)

        hotels = response.xpath(
            '//*[@id="search_results_table"]/div[2]/div/div/div[3]/div'
        )

        for hotel in hotels:
            try:
                url = hotel.xpath(
                    "div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a"
                ).attrib["href"]

                yield scrapy.Request(url, callback=self.get_detail)

            except Exception:
                pass

    # Callback use to scrap detail page
    def get_detail(self, response):
        print(response.url)

        name = response.xpath('//*[@id="hp_hotel_name"]/div/h2/text()').get()

        score = response.xpath(
            '//*[@id="js--hp-gallery-scorecard"]/a/div/div/div/div[1]/text()'
        ).get()

        desc = response.xpath(
            '//*[@id="property_description_content"]/div/p/text()'
        ).get()

        latlong = response.xpath(
            '//*[@id="hotel_sidebar_static_map"]/@data-atlas-latlng'
        ).get()

        price = response.xpath(
            '//*[@id="hprt-table"]/tbody/tr[1]/td[3]/div/div/div[1]/div[2]/div/span/text()'
        ).get()

        yield {
            "name": name,
            "url": response.url,
            "score": score,
            "description": desc,
            "latitude": latlong.split(",")[0],
            "longitude": latlong.split(",")[1],
            "price": price,
            "city": city
        }

city = sys.argv[1].replace('_', ' ')
print(city)

# Name of the file where the results will be saved
filename = f"hotel-{city}.json"

# If file already exists, delete it before crawling (because Scrapy will
# concatenate the last and new results otherwise)
if filename in os.listdir("src/"):
    os.remove("src/" + filename)

process = CrawlerProcess(
    settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "LOG_LEVEL": logging.INFO,
        "FEEDS": {
            "src/" + filename: {
                "format": "json"
            },
            "s3://jedha-project-kayak/booking/" + filename: {
                "format": "json"
            },
        },
        "FEED_EXPORT_ENCODING": "utf-8",
        "AWS_ACCESS_KEY_ID": 'AWS_ACCESS_KEY_ID',
        "AWS_SECRET_ACCESS_KEY": 'AWS_SECRET_ACCESS_KEY',
        "DOWNLOAD_DELAY": 2,
        "AUTOTHROTTLE_ENABLED": True,
        "COOKIES_ENABLED": False,
    }
)

# Start the crawling using the spider you defined above
process.crawl(ScrapyBooking)
process.start()
