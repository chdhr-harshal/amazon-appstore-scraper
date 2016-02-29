# !/home/grad3/harshal/py_env/my_env/bin/python2.7

from bs4 import BeautifulSoup as bs
from datetime import datetime
import re
import string

class parser:
    def __init__(self, html):
        self.html = filter(lambda x: x in string.printable, html)
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

    def get_developer_url(self):
        developer_url = self.soup.find('div', {'class':'buying'}).find('a')['href']
        return 'http://www.amazon.com' + developer_url

    def get_content_rating(self):
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

    def get_overall_rank(self):
        try:
            sales_rank = self.soup.find(text=re.compile('Free in Appstore for Android')).strip()
            sales_rank = sales_rank.split(' ')[0][1:].replace(',','')
            return dict({'Free':int(sales_rank)})
        except:
            sales_rank = self.soup.find(text=re.compile('Paid in Appstore for Android')).strip()
            sales_rank = sales_rank.split(' ')[0][1:].replace(',','')
            return dict({'Paid':int(sales_rank)})

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

    def get_avg_star_rating(self):
        star_rating = self.soup.find('span', {'class':'a-icon-alt'}).next.split(' ')[0]
        return star_rating
        
    def get_star_rating_histogram(self):
        histogram = self.soup.findAll('div', {'class':'a-meter'})
        histogram = [int(x['aria-label'][:-1]) for x in histogram]
        
        star_histogram = {
                        'percent_5_star' : histogram[0],
                        'percent_4_star' : histogram[1],
                        'percent_3_star' : histogram[2],
                        'percent_2_star' : histogram[3],
                        'percent_1_star' : histogram[4]
                        }
        return star_histogram
                   
    def get_category_rank(self):
        overall_rank = self.get_overall_rank()
        category_rank = {}
        categories = self.soup.findAll('li', {'class':'zg_hrsr_item'})
        for category in categories:
            rank = category.find('span').text[1:].replace(',','')
            category_name = category.text.strip().split('Appstore for Android > ')[1]
            category_rank[overall_rank.keys()[0] + ' > '+ category_name] = int(rank)

        category_rank.update(overall_rank)
        return category_rank

    def get_categories(self):
        names = []
        categories = self.soup.findAll('li', {'class':'zg_hrsr_item'})
        for category in categories:
            category_name = category.text.strip().split('Appstore for Android > ')[1]
            names.append(category_name)

        return names

    def get_icon_url(self):
        url = self.soup.find('img', {'class':'masrw-main-image'})['src']
        return url.strip()

    def get_permissions(self):
        perms_div = self.soup.find('div',{'id':'mas-app-permissions'}).find('ul')
        perms = perms_div.findAll('span')

        permissions = [perm.text.strip() for perm in perms]
        return permissions

    def get_developer_info(self):
        dev_info = {}
        dev_name = self.get_developer()
        dev_info['name'] = dev_name

        dev_div = self.soup.find('div', {'id':'mas-developer-info'}).findAll('span')
        dev_rows = [row.text.strip() for row in dev_div]

        for row in dev_rows:
            if '@' in row:
                dev_info['email'] = row
            if 'http://' in row:
                dev_info['website'] = row
            if 'email' in dev_info and 'website' in dev_info:
                break

        return dev_info

    def get_description(self):
        description = self.soup.find('div', {'id':'mas-product-description'})
        return description.find('div').text.strip()

    def get_similar_apps(self):
        apps = self.soup.findAll('div', {'class':'a-section a-spacing-none p13nimp p13n-asin'})
        asins = [app['data-asin'] for app in apps]
        return asins

    def get_app_info(self):
        return {'asin' : self.get_asin(),
                'title' : self.get_title(),
                'developer' : self.get_developer(),
                'developer_url' : self.get_developer_url(),
                'content_rating' : self.get_content_rating(),
                'price' : self.get_price(),
                'iap' : self.get_iap(),
                'release_date' : self.get_release_date(),
                'overall_rank' : self.get_overall_rank(),
                'version' : self.get_version(),
                'size' : self.get_size(),
                'min_os_version' : self.get_min_os_version(),
                'total_reviews' : self.get_total_reviews(),
                'avg_star_rating' : self.get_avg_star_rating(),
                'category_rank' : self.get_category_rank(),
                'categories' : self.get_categories(),
                'icon_url' : self.get_icon_url(),
                'permissions' : self.get_permissions(),
                'developer_info' : self.get_developer_info(),
                'description' : self.get_description(),
                'similar_apps' : self.get_similar_apps()}
