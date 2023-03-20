from bs4 import BeautifulSoup
import pandas as pd
import requests
from .debug_utils import debug

context = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Host': 'www.amazon.in',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
}


class FastScrapper:
    """A class to scrap amazon data"""

    def __init__(self, user_name, category, pages):
        self.df = pd.DataFrame(
            columns=[
                'user_name',
                'categories',
                'names',
                'rating',
                'total_rating',
                'cost_price',
                'selling_price',
                'links'
            ],
        )
        self.df = self.df.rename_axis('ID')
        self.category = category
        self.pages = int(pages)
        self.user_name = user_name
        self.data = dict()
        self.urls = list()

    def url_linker(self, *args):
        for page in range(0, self.pages):
            page_link = f'https://www.amazon.in/s?k={self.category}&page={page+1}&ref=nb_sb_noss'
            self.urls.append(page_link)

    def scrapper(self, urls):
        names = list()
        SP = list()
        CP = list()
        rating = list()
        people = list()
        links = list()
        categories = list()
        user_names = list()
        
        for url in urls:
            response = requests.get(url, headers=context).content
            soup = BeautifulSoup(response, 'html.parser')
            # OPTIONS TRIED:
            #  a-section
            #  sg-col-inner
            all_blocks = soup.findAll('div', class_="sg-col-inner")
            #if len(all_blocks) == 0: 
            #    debug(type='w', message="[WARNING] NO elements under this class found.")
            #    #pass
            for product in all_blocks:
                try:
                    name_obj = product.find('h2')
                    if name_obj is None:
                        #debug(type='e', message=f"OBJECT IS NONE!")
                        #debug(type='e', message="[PRODUCT IS SKIPPED]\n")
                        continue
                    else:
                        name = name_obj.get_text()
                    selling_price = product.find(
                                                 'span', 
                                                 class_='a-price-whole'
                                                ).get_text()
                    cost_price = product.findAll(
                                                    'span', 
                                                    class_='a-offscreen'
                                                )[-1].get_text().split('₹')[1]
                    
                    try:
                        rat = product.find(
                                            'span', 
                                            class_='a-icon-alt'
                                            ).get_text().split()[0] 
                        peps = product.find(
                                            'span', 
                                            class_='a-size-base'
                                            ).get_text()
                    except Exception as e:
                        debug(type='w', message=e)
                        continue
                        
                    # Inside Link
                    extracted_href = product.find('a', class_='a-link-normal').get('href')
                    link = str()
                    if extracted_href.startswith('https:'):
                        continue
                    else:
                        link = 'https://www.amazon.in' + extracted_href
                    names.append(name)
                    SP.append(selling_price)
                    CP.append(cost_price)
                    rating.append(rat)
                    people.append(peps)
                    links.append(link)
                    categories.append(self.category)
                    user_names.append(self.user_name)

                except Exception as e:
                    debug(type='w', message=e)

        self.data['user_name'] = user_names
        self.data['categories'] = categories
        self.data['names'] = names
        self.data['rating'] = rating
        self.data['total_rating'] = people
        self.data['cost_price'] = CP
        self.data['selling_price'] = SP
        self.data['links'] = links
        

    def convert_to_df(self):
        df1 = pd.DataFrame(self.data)
        self.df = pd.concat((self.df, df1))

    def scrap(self):
        self.url_linker(self.category)
        self.scrapper(self.urls)
        self.convert_to_df()
        self.df['cost_price'] = self.df['cost_price'].map(lambda x: x.replace(',', ''))
        self.df['selling_price'] = self.df['selling_price'].map(lambda x: x.replace(',', ''))
        self.df['total_rating'] = self.df['total_rating'].map(lambda x: x.replace(',', ''))
        my_df = self.df
        return my_df

    def save_to_csv(self):
        self.df.to_csv('csv/' + self.user_name + '.csv')
   