import SendRequest
from bs4 import BeautifulSoup
import pandas as pd
class Vidange : 
    def __init__(self,search="roulement",page="1"):
        self.search=f"{search}"
        self.url=lambda page: f"https://vidange.tn/recherche?controller=search&{page}=2&s={search}&spr_submit_search=Search"
        self.link=self.url(page)
        self.headers = {
            'User-Agent': 'Mozilla/5.0'}
        self.response=SendRequest.SendRequest(self.link,self.headers).send_request()
        self.soup=BeautifulSoup(self.response.text, 'html.parser')
        self.search_links=self.flattenPagination()
        self.search_result=self.search_product()
        self.min_price_product=None
    
    def flattenPagination(self):
    # Find the pagination div

        pagination = self.soup.find( class_='pagination')
        # Find the last page number
        last_page = int(pagination.find_all('a')[-2].text)
        pages_list=[]
        for i in range(1,last_page+1):
            pages_list.append (self.url(i))
        return pages_list
    def search_product(self):
        print("Searching for products in Vidange site Please wait...")
        df = pd.DataFrame(columns=['product_name', 'product_price', 'product_link'])
        for link in self.search_links:
            self.response=SendRequest.SendRequest(link,self.headers).send_request()
            self.soup=BeautifulSoup(self.response.text, 'html.parser')
            products=self.soup.find_all(class_='product-miniature')
            for product in products:
                product_name=product.find(class_='product-title').text
                product_price=product.find(class_='price').text
                product_link=product.find('a')['href']
                df = df._append({'product_name': product_name, 'product_price': product_price, 'product_link': product_link}, ignore_index=True)
        df['product_price'] = df['product_price'].str.replace('TND', '').str.replace(',', '.').astype(float)
# Convert price to float
        min_price_row = df.loc[df['product_price'].idxmin()]
        self.min_price_product = {
            'product_name': min_price_row['product_name'],
            'product_price': f"{min_price_row['product_price']} TND",
            'product_link': min_price_row['product_link']
        }
        
        # Print the minimum price product
        print(f"Product {self.search} with the minimum price in Vidange : ")
        print(self.min_price_product)
        return df
if __name__ == "__main__":
    Vidange()