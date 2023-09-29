import os
import logging
import scrapy
from scrapy.crawler import CrawlerProcess


class ScrapyBooking(scrapy.Spider):
    # Name of your spider
    name = "booking"

    # Starting URL
    start_urls = ["https://www.booking.com/index.fr.html"]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                "ss": "Rouen",
                "ssne": "Rouen",
                "ssne_untouched": "Rouen",
                "dest_type": "city",
                "ac_langcode": "fr",
                "search_selected": "true",
                "group_adults": "1",
                "no_rooms": "1",
                "group_children": "0",
            },
            # Function to be called once logged in
            callback=self.after_search,
        )

    # Callback used after search
    def after_search(self, response):
        print(response.url)
        hotels = response.xpath(
            "/html/body/div[5]/div/div[4]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div[3]/div"
        )

        for hotel in hotels:
            name = hotel.xpath(
                "div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a/div[1]/text()"
            ).get()
            url = hotel.xpath(
                "div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a"
            ).attrib["href"]
            score = hotel.xpath(
                "div[1]/div[2]/div/div[1]/div/div[2]/div/div/div/a/span/div/div[1]/text()"
            ).get()
            try:
                desc = hotel.xpath(
                    "div[1]/div[2]/div/div[2]/div[1]/div/div/div/div/text()"
                ).get()
            except:
                desc = None

            try:
                price = hotel.xpath(
                    "div[1]/div[2]/div/div[2]/div[2]/div/div[1]/div[2]/text()"
                ).get()
            except:
                price = None

            yield {
                "name": name,
                "url": url,
                "score": score,
                "description": desc,
                "price": price,
            }
        # Select the NEXT button and store it in next_page
        # try:
        #     next_page = response.xpath('/html/body/div/div[2]/div[1]/nav/ul/li[@class="next"]/a').attrib["href"]
        # except KeyError:
        #     # In the last page, there won't be any "href" and a KeyError will be raised
        #     logging.info('No next page. Terminating crawling process.')
        # else:
        #     # If a next page is found, execute the parse method once again
        #     yield response.follow(next_page, callback=self.after_login)


# Name of the file where the results will be saved
filename = "hotel-rouen.json"

# If file already exists, delete it before crawling (because Scrapy will
# concatenate the last and new results otherwise)
if filename in os.listdir("src/"):
    os.remove("src/" + filename)

## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(
    settings={
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "LOG_LEVEL": logging.INFO,
        "FEEDS": {
            "src/" + filename: {"format": "json"},
        },
        "DOWNLOAD_DELAY": 5,
        "AUTOTHROTTLE_ENABLED": True,
        "COOKIES_ENABLED": False,
    }
)

# Start the crawling using the spider you defined above
process.crawl(ScrapyBooking)
process.start()
