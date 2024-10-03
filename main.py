from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time

count = 1


# clean rating
def clean_rating(value):
    global count
    new_rating = []
    for n in value:
        if count % 2 != 0 and count <= 7:
            new_rating.append(n)


        elif count > 7 and count % 2 == 0:
            new_rating.append(n)

        count += 1

    return new_rating


# _________________________________________________ Beautiful Soup __________________________________


response = requests.get('https://www.audible.com/search?keywords=book&node=18573211011')

content = response.text

soup = BeautifulSoup(content, 'html.parser')

# scrap data
authors_name_list = [author for author in soup.select(selector='.authorLabel span.bc-text')]
narrated_by = [narator.getText() for narator in soup.select(selector='.narratorLabel span a')]
audio_length = [audio_len.getText() for audio_len in soup.select(selector='.runtimeLabel span')]
rating = [rating_label.getText() for rating_label in soup.select(selector='li.ratingsLabel span.bc-text')]

#  clean  Data
audio_length = [item.split('Length:')[1] for item in audio_length]
authors_name_list = [item.find('a').getText() for item in authors_name_list]
rating = clean_rating(rating)

#______________________________________________Selenium driver __________________________

# prevent browser from closing by itself

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

# chrome driver instance
driver = webdriver.Chrome(options=chrome_options)

for n in range(len(authors_name_list)):
    driver.get(
        'https://docs.google.com/forms/d/e/1FAIpQLSdj2tpqxvcM8ln2urBVYJgVrV2AsfIgJrSvINpVTbeWo-KowQ/viewform?usp'
        '=sf_link')

    time.sleep(2)

    # connect driver to input form

    author_input = driver.find_element(by=By.XPATH,
                                       value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    narrator_input = driver.find_element(by=By.XPATH,
                                         value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    audio_input = driver.find_element(by=By.XPATH,
                                      value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    rating_input = driver.find_element(by=By.XPATH,
                                       value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
    button = driver.find_element(by=By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    # data entry
    author_input.send_keys(authors_name_list[n])
    narrator_input.send_keys(narrated_by[n])
    audio_input.send_keys(audio_length[n])
    rating_input.send_keys(rating[n])

    time.sleep(2)

    button.click()

# close browser
driver.quit()
