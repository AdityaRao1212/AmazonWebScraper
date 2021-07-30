from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

context = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Host': 'www.amazon.in',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
}


class Scrapper:
    """A class to scrap amazon data"""

    def __init__(self):
        self.df = pd.DataFrame(
            columns=[
                'names',
                'categories',
                'selling_price',
                'cost_price',
                'rating',
                'total_rating',
                'discount',
                'discount_per',
                'links'
            ],
        )
        self.df = self.df.rename_axis('ID')

    def url_linker(self, total_pages=5, *args):
        urls = list()
        for page in range(1, total_pages+1):
            urls.append(self.url_builder(page, *args))
        return urls

    def url_builder(self, page=1, *args):
        parms = '+'.join(args)
        url = f'https://www.amazon.in/s?k={parms}&page={page}&ref=nb_sb_noss'
        return url

    def scrapper(self, urls, category):
        names = list()
        SP = list()
        CP = list()
        rating = list()
        people = list()
        discount = list()
        discount_per = list()
        brand_name = list()
        links = list()
        categories = list()
        data = dict()

        for url in urls:
            print(url)
            response = requests.get(url, headers=context).content
            soup = BeautifulSoup(response, 'html.parser')
            all_blocks = soup.findAll('div', class_='s-asin')
            for product in all_blocks:
                try:
                    name = product.find('h2').get_text()
                    selling_price = product.find(
                        'span', class_='a-price-whole').get_text()
                    cost_price = product.findAll(
                        'span', class_='a-offscreen')[-1].get_text().split('₹')[1]
                    rat = product.find(
                        'span', class_='a-icon-alt').get_text().split()[0]
                    peps = product.find(
                        'span', class_='a-size-base').get_text()
                    # Inside Link
                    link = 'https://www.amazon.in' + \
                        product.find('a', class_='a-link-normal').get('href')
                    new_res = requests.get(link, headers=context).content
                    new_soup = BeautifulSoup(new_res, 'html.parser')
                    disc, disc_per = new_soup.find(
                        'td', 'a-span12 a-color-price a-size-base priceBlockSavingsString').get_text().split()
                    disc = disc.split('₹')[1].replace(',', "")
                    disc_per = disc_per.lstrip('(').rstrip(')')[:2]

                    brand = dict()
                    lst = []
                    for i in new_soup.findAll('tr', 'a-spacing-small'):
                        lst.append([i.get_text().strip()])
                    for i in lst:
                        i = i[0].split('\n')
                        brand[i[0]] = i[-1]

                    brand_ = brand.get('Brand')
                    if not brand_:
                        continue
                    else:
                        brand_name.append(brand_)
                    print(name)
                    names.append(name)
                    SP.append(selling_price)
                    CP.append(cost_price)
                    rating.append(rat)
                    people.append(peps)
                    discount.append(disc)
                    discount_per.append(disc_per)
                    links.append(link)
                    categories.append(category)
                except Exception as e:
                    continue

        data['names'] = names
        data['selling_price'] = SP
        data['cost_price'] = CP
        data['rating'] = rating
        data['total_rating'] = people
        data['discount'] = discount
        data['discount_per'] = discount_per
        data['brands'] = brand_name
        data['categories'] = categories
        data['links'] = links
        return data

    def amazon_scraper(self, category, sex, pages=10):
        urls = self.url_linker(pages, category, sex)
        return self.scrapper(urls, category)

    def save_df_to_csv(self, name):
        self.df.to_csv(name + '.csv')


if __name__ == '__main__':
    scrapper = Scrapper()
    categories = [
        ('skin_cream', 'women'),
    ]
    all_data = []
    for category, sex in categories:
        data = scrapper.amazon_scraper(category, sex, 1)
        all_data.append(data)
        print(category)
    print(len(all_data[0]['names']), len(all_data[0]['selling_price']), len(all_data[0]['cost_price']), len(
        all_data[0]['total_rating']), len(all_data[0]['links']), len(all_data[0]['categories']), len(all_data[0]['brands']))

    df = pd.DataFrame(
        columns=[
            'names',
            'categories',
            'selling_price',
            'cost_price',
            'rating',
            'total_rating',
            'discount',
            'discount_per',
            'links'
        ],
    )
    df = df.rename_axis('ID')

    for data in all_data:
        df1 = pd.DataFrame(data)
        df = pd.concat([df, df1], ignore_index=True)

    df.to_csv('csv/1.csv')
    
    