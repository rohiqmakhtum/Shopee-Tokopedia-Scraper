from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
from time import sleep

# create object for chrome options
chrome_options = Options()
# base_url = 'https://shopee.sg/search?keyword=disinfectant'

# set chrome driver options to disable any popup's from the website
# to find local path for chrome profile, open chrome browser
# and in the address bar type, "chrome://version"
chrome_options.add_argument('disable-notifications')
chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('user-data-dir=C:\\Users\\username\\AppData\\Local\\Google\\Chrome\\User Data\\Default')
# To disable the message, "Chrome is being controlled by automated test software"
chrome_options.add_argument("disable-infobars")
# Pass the argument 1 to allow and 2 to block
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})

def get_url(search_term):
    """Generate an url from the search term"""
    template = "https://www.tokopedia.com/search?q={}"
    #?page=3&q=nutriflakes&st=product"
    search_term = search_term.replace(' ', '+')

    # add term query to url
    url = template.format(search_term)

    # add page query placeholder
    url += '&page={}' # -> url = url + '&page' 

    return url


def main(search_term):
    # invoke the webdriver
    driver = webdriver.Chrome(executable_path='C:\\Users\\LENOVO\\Downloads\\chromedriver\\chromedriver' , options=chrome_options)
    rows = []
    url = get_url(search_term)

    for page in range(0, 1):
        driver.get(url.format(page))
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "css-qa82pd")))
        driver.execute_script("""
        var scroll = document.body.scrollHeight / 5;
        var i = 0;
        function scrollit(i) {
           window.scrollBy({top: scroll, left: 0, behavior: 'smooth'});
           i++;
           if (i < 10) {
            setTimeout(scrollit, 500, i);
            }
        }
        scrollit(i);
        """)
        sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', {'class': 'pcv3__container css-gfx8z3'}):
            name = item.find('div', {'class': 'prd_link-product-name css-3um8ox'})
            if name is not None:
                name = name.text.strip()
            else:
                name = ''

            price = item.find('div', {'class': 'prd_link-product-price css-1ksb19c'})
            if price is not None:
                price = price.text.strip().replace(".", ",").replace("Rp", "")
            else:
                price = ''

            location = item.find('span', {'class': 'prd_link-shop-loc css-1kdc32b flip'})
            if location is not None:
              location = location.text.strip()
            else:
              location = ''
            
            link = item.find('a', {'class':'pcv3__info-content css-gwkf0u'})
            if link is not None:
              link = link.get('href')
            else:
              link = ''
              
            print([name, price])
            print([link])
            rows.append([name, location, price, link])
            # rows.append([name, price])

    with open('tokped_item_list.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # writer.writerow(['Deskripsi Produk', 'Lokasi Toko', 'Harga', 'Link'])
        writer.writerow(['Deskripsi Produk', 'Lokasi', 'Harga', 'Link'])
        writer.writerows(rows)

main("kaligrafi")
