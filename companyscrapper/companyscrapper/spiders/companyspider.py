from typing import Iterable
import scrapy
from scrapy.http import Request
from companyscrapper.items import CompanyItem
class CompanyspiderSpider(scrapy.Spider):
    name = "companyspider"
    base_url = "https://www.ambitionbox.com"
    allowed_domains = ["www.ambitionbox.com"]
    start_urls = ["https://www.ambitionbox.com/list-of-companies?locations=kolkata&tags=startup&ratings=4.0&sortBy=popular&page=1"]
    stop_req = 1
    
    def parse_company_details(self, response):
        company_name = response.css('h1.newHInfo__cNtxt ::text').get()
        fields = response.css('a.aboutItem__link')
        item = CompanyItem()
        item['company_name'] = company_name.lstrip().rstrip()
        for field in fields:
            value = field.css('a.aboutItem__link ::text').get()
            if value is not None and '@' in value:
                item['company_email'] = value.strip()
            elif value is not None and '.com' in value:
                item['company_website'] = value.strip()
            elif value is not None and value.strip().isnumeric():
                item['company_contact'] = int(value.strip())
        
        yield item
        # item['company_website'] = scrapy.Field
        # item['company_email'] = scrapy.Field
        # item['company_contact'] = scrapy.Field
        
    
    def parse(self, response):
        # companies = response.css('h2.companyCardWrapper__companyName')
        companies = response.css('a.companyCardWrapper__companyName')
        for company in companies:
            overview = company.css('a.companyCardWrapper__companyName ::attr(href)').get()
            if overview is not None:
                yield response.follow(f"{self.base_url}{overview}", callback=self.parse_company_details)
            # name = ((company.css('h2.companyCardWrapper__companyName ::text').get()).lstrip()).rstrip()
            # print(name)
    
        
        next_page = response.css('a.page-nav-btn.router-link-active')
        
        if len(next_page)>1: 
            next_page = next_page[1]
            
        next_page = next_page.css('a.page-nav-btn.router-link-active ::attr(href)').get()
        
        if next_page is not None:
            page_no = next_page[next_page.find('page='):]
            p = int(page_no[page_no.find('=')+1:])
            if self.stop_req >= p:
                return
            else:
                self.stop_req = p
            next_page_url = f"{self.base_url}/list-of-companies?locations=kolkata&tags=startup&ratings=4.0&sortBy=popular&{page_no}"
            # print(next_page_url)
            yield response.follow(next_page_url, callback=self.parse)
