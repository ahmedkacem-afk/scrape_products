import SendRequest
from bs4 import BeautifulSoup
import pandas as pd
class Vidange : 
    def __init__(self,search="roulement",page="1"):
        self.url=lambda page: f"https://www.piecesautos.tn/recherche/{search}?page={page}"
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
        last_page = int(pagination.find_all('a')[-1].text)
    
        pages_list=[]
        for i in range(1,last_page+1):
            pages_list.append (self.url(i))
           
        return pages_list
    def search_product(self):
    # Initialize an empty DataFrame
        df = pd.DataFrame(columns=['product_name', 'product_price', 'product_link'])
        
        # Iterate through all search links
        for link in self.search_links:
            print(f"Fetching data from: {link}")
            self.response = SendRequest.SendRequest(link, self.headers).send_request()
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            
            # Find all product cards
            products = self.soup.find_all(class_='product-card')
            for product in products:
                # Extract product name
                product_name_div = product.find("div", class_="product-card__name")
                product_link = product_name_div.find("a")['href']
                product_name = product_name_div.find("a").get_text(strip=True)
                
                # Extract product price
                product_footer_div = product.find("div", class_="product-card__footer")
                product_price = product_footer_div.find(class_='product-card__price').text.strip()
                
                # Append to DataFrame
                df = pd.concat([df, pd.DataFrame([{
                    'product_name': product_name,
                    'product_price': product_price,
                    'product_link': product_link
                }])], ignore_index=True)
        
        # Print the resulting DataFrame
        df['product_price'] = df['product_price'].str.replace(',', '').astype(float)  # Convert price to float
        min_price_row = df.loc[df['product_price'].idxmin()]
        self.min_price_product = {
            'product_name': min_price_row['product_name'],
            'product_price': min_price_row['product_price'],
            'product_link': min_price_row['product_link']
        }
        
        # Print the minimum price product
        print("Product with the minimum price:")
        print(self.min_price_product)
        return df

if __name__ == "__main__":
    Vidange()