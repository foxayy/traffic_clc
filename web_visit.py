import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def random_sleep():
    time.sleep(random.uniform(0, 2))

def random_click_links(driver):
    #links = driver.find_elements(By.TAG_NAME, 'a')
    #links = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'a')))
    #links = driver.find_element(By.XPATH, "//a")
    #buttons = driver.find_elements(By.TAG_NAME, 'button')
    #buttons = driver.find_elements(By.XPATH, "//button[@type='button']")
    links = driver.find_elements(By.CSS_SELECTOR, 'a[href]')
    '''
    test = "//*[@id=\"i_cecream\"]/div[2]/div[1]/div[1]/ul[1]/li[1]/a"
    element = driver.find_elements(By.XPATH, test)
    element[0].click()
    '''
    #links.pop(0)
    if links:
        link = random.choice(links)
        href = link.get_attribute("href")
        if href.startswith("http"):
            #driver.execute_script("arguments[0].click();", link)
            #link.click()
            return href
    
    return None

def visit_website(driver, url, depth=10):
    if depth == 0:
        return
    driver.get(url)
    random_sleep()
    next_url = random_click_links(driver)
    if next_url:
        visit_website(driver, next_url, depth - 1)

def read_website_list(filename):
    with open(filename, 'r') as file:
        website_list = file.readlines()
    return [url.strip() for url in website_list if url.strip()]

def get_chrome_driver():
    return webdriver.Chrome()

def get_firefox_driver():
    return webdriver.Firefox()

def get_edge_driver():
    return webdriver.Edge()

def main():

    drv_mapping = {
        "1": get_chrome_driver,
        "2": get_firefox_driver,
        "3": get_edge_driver
    }

    print("please choose browse driver: ")
    print("1. chrome")
    print("2. firefox")
    print("3. edge")

    drv_choice = input()
    if drv_choice not in drv_mapping:
        print("Invalid choice!")
        return

    websites = read_website_list("websites.txt")
    websites_len = len(websites)

    total_loop = 100
    cur_loop = 0
    idx = 0

    while True:

        for _ in range(websites_len):
            driver = drv_mapping[drv_choice]()
            driver.set_window_size(1920, 1080)
            visit_website(driver, websites[idx])
            driver.quit()
            idx = (idx + 1) % websites_len

        cur_loop += 1
        if cur_loop == total_loop:
            break
        print(f"have visit all the website, start round {cur_loop + 1}...")

    print("process done!")

    
main()