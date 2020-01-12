def get_news(search_term):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    driver.get(f'https://news.google.com/search?q={search_term}&hl=en-US&gl=US&ceid=US%3Aen')
    text = driver.page_source
    driver.quit()
    return text

if __name__ == '__main__':
    print(get_news('trifacta'))
