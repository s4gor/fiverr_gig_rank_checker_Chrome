#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.common.exceptions import NoSuchElementException
import time
import urllib.parse

service = service.Service('/home/imran/Desktop/selenium/chromedriver')


def search(keyword, page=1):
    keyword = urllib.parse.quote(keyword)
    return f'https://www.fiverr.com/search/gigs?query={keyword}&source=top-bar&search_in=everywhere&search-autocomplete-original-term={keyword}&page={page}&offset=-5'


def main():
    kywrd = input('\n[+] Enter keyword: ')

    username = input('[+] Enter username: ')

    start_page = input('[+] From which page you want to start looking [enter:Default = 1]: ')

    if start_page == '':
        start_page = 1

    start_page = int(start_page)
    first_loader = time.time()
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(search(kywrd))

    total_services = driver.find_element_by_xpath('//*[@id="perseus-app"]/div/div/div[4]/div[1]/div').text
    print(f'\n{total_services}\n')
    end_page = int((total_services.split(' ')[0]).replace(',', ''))
    end_page = round(end_page / 48)

    if end_page > 21:
        end_page = 21

    driver.quit()

    time.sleep(1)

    for j in range(start_page, end_page):
        driver = webdriver.Chrome(service=service)
        driver.minimize_window()
        start_time = time.time()
        driver.get(search(kywrd, j))
        print(f'Page loaded in {round(time.time() - start_time, 2)} seconds')

        for i in range(1, 49):
            try:
                usrnam = driver.find_element_by_xpath(
                    f'/html/body/div[1]/div[2]/div[2]/div/div/div/div[5]/div/div/div[{i}]/div/div/div[1]/div/span[2]/a').text
                if usrnam == username:
                    rank = ((j - 1) * 48) + i
                    if j > 1:
                        print('')
                    print(f'Found! Rank: {rank} | On page: {j}')
                    break
                elif i == 48 and j == (end_page - 1):
                    print(f'\nNot found with in {j} pages. Try to improve your gig impressions')
                    break
                elif i == 48:
                    print(f'Not found in page {j}')

            except NoSuchElementException:
                pass
        if i == 48 and j == (end_page - 1):
            break

        if usrnam == username:
            break
        else:
            driver.quit()
            time.sleep(1)

    last_loader = time.time()

    driver.close()

    hr = last_loader - first_loader

    scnd = round(hr % 60)

    mnte = round((hr - scnd) / 60)


    print(f'\nTime: {mnte} minutes {scnd} seconds')

    print('\nDevelopr: github.com/s4gor')

    input('\nPress any key to exit ')


if __name__ == '__main__':
    main()
