# !/home/grad3/harshal/py_env/my_env/bin/python2.7

from bs4 import BeautifulSoup as bs
from datetime import datetime
import re
import string

class parser:
    def __init__(self, html):
        self.html = filter(lambda x: x in string.printable, html)
        self.soup = bs(self.html, "lxml")

    def pagination_next_review_page(self):
        pagination = self.soup.find('ul', {'class':'a-pagination'})
        if pagination is None:
            return False
        next_page = self.soup.find('li', {'class':'a-disabled a-last'})
        if next_page is None:
            return True
        else:
            return False

    def get_reviews(self):
        reviews_data = []
        container = self.soup.find('div', {'id':'cm_cr-review_list'})
        reviews = container.findAll('div', {'class':'a-section review'})

        for review in reviews:
            review_id = review['id']

            asin = review.find('a', {'class':'a-link-normal'})['href'].split('=')[-1]

            star_rating = review.find('span', {'class':'a-icon-alt'}).next.split(' ')[0]

            title = review.find('a', {'class':'a-size-base a-link-normal review-title a-color-base a-text-bold'}).next.replace('"','').replace("'","")

            reviewer = review.find('a', {'class':'a-size-base a-link-normal author'})['href'].split('/')[4]

            reviewer_url = review.find('a', {'class':'a-size-base a-link-normal author'})['href']
            reviewer_url = "http://www.amazon.com" + reviewer_url

            date = review.find('span', {'class':'a-size-base a-color-secondary review-date'}).next.strip('on ')
            date = datetime.strptime(date, "%B %d, %Y").strftime("%Y-%m-%d")

            review_text = review.find('span', {'class':'a-size-base review-text'}).next.replace("'","").replace('"','')


            comments = review.find('span', {'class':'review-comment-total'}).next
            try:
                comments = int(comments)
            except:
                comments = 0

            total_votes = review.find('span',{'class':'a-size-small a-color-secondary review-votes'}).next.split(' ')[2].replace(',','')
            try:
                total_votes = int(total_votes)
            except:
                total_votes = 0

            upvotes = review.find('span', {'class':'a-size-small a-color-secondary review-votes'}).next.split(' ')[0].replace(',','')
            try:
                upvotes = int(upvotes)
            except:
                upvotes = 0

            downvotes = total_votes - upvotes

            try:
                review_type = review.find('span',{'class':'a-size-mini a-color-state a-text-bold'}).next
            except:
                review_type = None


        
            reviews_data.append({
                'review_id' : review_id,
                'asin' : asin,
                'star_rating' : star_rating,
                'title' : title,
                'reviewer' : reviewer,
                'reviewer_url' : reviewer_url,
                'date' : date,
                'text' : review_text,
                'comments' : comments,
                'total_votes' : total_votes,
                'upvotes' : upvotes,
                'downvotes' : downvotes,
                'type' : review_type
                })


        next_page_exists = self.pagination_next_review_page()

        return (reviews_data, next_page_exists)
