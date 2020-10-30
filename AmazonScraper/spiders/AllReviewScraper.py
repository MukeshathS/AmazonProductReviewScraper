import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from scrapy import Selector
import csv


class AllreviewscraperSpider(CrawlSpider):
    name = 'AllReviewScraper'
    allowed_domains = ['www.amazon.in']

    def start_requests(self):

        urls = []
        urls.append(input("Enter a url: "))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_all_reviews)


    def parse(self, response):

        start_domain = "https://www.amazon.in"
        all_reviews_url = response.xpath('//a[contains(text(), "See all reviews")]/@href')

        for i in all_reviews_url:
            reviews_url = start_domain + i

            yield scrapy.Request(url=reviews_url, callback=self.parse_all_reviews)


    def parse_all_reviews(self, response):

        next = response.xpath('//a[contains(text(), "Next page")]/@href').extract()
        print(next)

        with open('all_reviews.csv', 'a', encoding='utf-8') as file:

            writer = csv.writer(file)

            for t in response.xpath('//span[@data-hook = "review-body"]/span').extract():

                review = []

                select_text = Selector(text=str(t))
                span_text = select_text.xpath('//*/text()').extract()
                seperator = ', '
                concat_text = seperator.join(span_text)
                print("Concat text --- ")
                print(concat_text)
                review.append(concat_text)
                writer.writerow(review)

        if next:
            for nxt in next:
                yield scrapy.Request(url = "https://www.amazon.in"+nxt, callback = self.parse_all_reviews)
