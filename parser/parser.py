from bs4 import BeautifulSoup as bs
from datetime import datetime
import re
import string

class parser:
    def __init__(self, html):
        self.html = html.decode('ascii','ignore')
        self.soup = bs(self.html, "lxml")

    def get_asin(self):
        asin = self.soup.find(text=re.compile('ASIN:')).next
        return asin.strip()

    def get_title(self):
        title = self.soup.find('span', {'id':'btAsinTitle'}).next
        return title.strip()

    def get_developer(self):
        developer = self.soup.find('div', {'class':'buying'}).find('a').next
        return developer.strip()

    def get_mas_rating(self):
        mas_rating = self.soup.find('span', {'class':'mas-rating-value'}).find('a').next
        return mas_rating.strip()

    def get_price(self):
        price = self.soup.find('strong', {'class':'priceLarge'}).next.strip()
        return price

    def get_iap(self):
        iap = self.soup.find('span', {'id':'offer_inapp_popover'})
        if iap:
            return True
        else:
            return False

    def get_release_date(self):
        release_date = self.soup.find(text=re.compile('Release Date:')).next.strip()
        release_date = datetime.strptime(release_date, "%B %d, %Y")
        return release_date.strftime("%Y-%m-%d")

    def get_sales_rank(self):
        sales_rank = self.soup.find(text=re.compile('Paid in Appstore for Android')).strip()
        sales_rank = sales_rank.split(' ')[0][1:].replace(',','')
        return sales_rank

    def get_version(self):
        version = self.soup.find(text=re.compile('Version:')).next
        return version.strip()

    def get_size(self):
        try:
            size = self.soup.find(text=re.compile('MB'))
            size = re.findall('[\d.]+', size)[0] + ' MB'
        except:
            size = self.soup.find(text=re.compile('KB'))
            size = re.findall('[\d.]+', size)[0] + ' KB'
        return size
        
    def get_min_os_version(self):
        try:
            min_os_version = self.soup.find(text=re.compile('Minimum Operating System:')).next
            min_os_version = re.findall('[\d.]+', min_os_version)[0]
            return min_os_version
        except:
            return 'Varies'

    def get_total_reviews(self):
        total_reviews = self.soup.find(text=re.compile('customer review')).strip()
        total_reviews = total_reviews.split(' ')[0].replace(',','')
        return total_reviews

    def get_star_rating(self):
        star_rating = self.soup.find('span', {'class':'a-icon-alt'}).next.split(' ')[0]
        return star_rating
        
    def get_star_rating_histogram(self):
        histogram = self.soup.findAll('div', {'class':'a-meter'})
        histogram = [int(x['asia-label'][:-1]) for x in histogram]
        
        star_histogram = {
                        'percent_5_star' : histogram[0],
                        'percent_4_star' : histogram[1],
                        'percent_3_star' : histogram[2],
                        'percent_2_star' : histogram[3],
                        'percent_1_star' : histogram[4]
                        }
        return star_histogram
                    
