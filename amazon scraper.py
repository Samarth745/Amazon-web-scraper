from bs4 import BeautifulSoup
import csv
from selenium import webdriver
website = "https://www.amazon.in/s?k={}"
def  get_url(search):
    search = search.replace(" ", "+")
    url = website.format(search)
    url += '&page{}'   
    return url
def extract_record(item):
            atag = item.h2.a
            description = atag.text.strip()           
            try:
                price_parent = item.find('span', 'a-price')
                price = price_parent.find('span', 'a-price-whole').text
            except AttributeError:
                price_parent=-1
                price=-1       
            try:
                rating = item.i.text
                count_review = item.find('span', {'class': 'a-size-base'}).text
            except AttributeError:
                rating = " "
                count_review = " "
            result = (description, price, rating, count_review)
            return result
def main(search): 
    driver = webdriver.Chrome()
    records = []
    url = get_url(search)
    for page in range(1,2):   
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'class': 's-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16'})
        for item in results:
            records.append(extract_record(item))
        print(len(records))
    with open('results.csv', 'w', newline='', encoding=('utf-8')) as f:
        writer = csv.writer(f)
        writer.writerow(['description', 'price', 'ratings', 'count_review'])
        writer.writerows(records)
 
        
    

main('gopro')  
    
