import scrapy
import json

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    start_urls = ["https://directory.ntschools.net/#/schools"]
    headers = {
        'Accept':'application/json',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9,hi;q=0.8,lb;q=0.7',
        'Referer':'https://directory.ntschools.net/',
        'Sec-Fetch-Mode':'cors',
        'Sec-Fetch-Site':'same-origin',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With':'Fetch',
    }

    def parse(self, response):
        url = 'https://directory.ntschools.net/api/System/GetAllSchools'
        request= scrapy.Request(url,callback=self.parse_api, headers=self.headers)
        yield request
    def parse_api(self,response):
        raw_data = response.body
        data = json.loads(raw_data)
        for school in data:
            school_code = school['itSchoolCode']
            request = scrapy.Request(f'https://directory.ntschools.net/api/System/GetSchool?itSchoolCode={school_code}',headers=self.headers,callback=self.parse_school)
            yield request
    def parse_school(self,response):
        raw_data = response.body
        data = json.loads(raw_data)

        with open('list.txt','a') as file:
            file.write(f'{data["physicalAddress"]}\n')

