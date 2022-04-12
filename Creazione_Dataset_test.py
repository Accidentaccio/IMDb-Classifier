from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from pandas import DataFrame
from os import chdir
from sys import path

chdir(path[0])

films = {
    'Iron Man': 'https://www.imdb.com/title/tt0371746/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'L\'incredibile Hulk': 'https://www.imdb.com/title/tt0800080/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Iron Man 2': 'https://www.imdb.com/title/tt1228705/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Thor': 'https://www.imdb.com/title/tt0800369/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Captain America - Il primo vendicatore': 'https://www.imdb.com/title/tt0458339/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'The Avengers': 'https://www.imdb.com/title/tt0848228/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Iron Man 3': 'https://www.imdb.com/title/tt1300854/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Thor - The Dark World': 'https://www.imdb.com/title/tt1981115/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Captain America - The Winter Soldier': 'https://www.imdb.com/title/tt1843866/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Guardiani della Galassia': 'https://www.imdb.com/title/tt2015381/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Avengers - Age of Ultron': 'https://www.imdb.com/title/tt2395427/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Ant-Man': 'https://www.imdb.com/title/tt0478970/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Captain America - Civil War': 'https://www.imdb.com/title/tt3498820/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Doctor Strange': 'https://www.imdb.com/title/tt1211837/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Guardiani della Galassia Vol. 2': 'https://www.imdb.com/title/tt3896198/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Spider-Man - Homecoming': 'https://www.imdb.com/title/tt2250912/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Thor - Ragnarok': 'https://www.imdb.com/title/tt3501632/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Black Panther': 'https://www.imdb.com/title/tt3501632/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Avengers - Infinity War': 'https://www.imdb.com/title/tt4154756/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Ant-Man and the Wasp': 'https://www.imdb.com/title/tt5095030/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Captain Marvel': 'https://www.imdb.com/title/tt4154664/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Avengers - Endgame': 'https://www.imdb.com/title/tt4154796/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Spider-Man - Far from Home': 'https://www.imdb.com/title/tt6320628/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Black Widow': 'https://www.imdb.com/title/tt3480822/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Shang-Chi e la leggenda dei Dieci Anelli': 'https://www.imdb.com/title/tt9376612/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Eternals': 'https://www.imdb.com/title/tt9032400/reviews?sort=submissionDate&dir=desc&ratingFilter=0',
    'Spider-Man - No Way Home': 'https://www.imdb.com/title/tt10872600/reviews?sort=submissionDate&dir=desc&ratingFilter=0'

}

PATH = 'chromedriver.exe'
s=Service(PATH)
options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
pilot = webdriver.Chrome(service=s, options=options)


for key, value in films.items():
    
    pilot.get(value)

    while True:
        try:
            pilot.find_element(By.XPATH, '//div[@class="load-more-data"]').click()
        except NoSuchElementException:
            break
        except (ElementClickInterceptedException, ElementNotInteractableException):
            break


    warning_buttons = pilot.find_elements(By.XPATH, './/div[@class="expander-icon-wrapper spoiler-warning__control"]')
    for button in warning_buttons:
        try:
            button.click()
        except (ElementClickInterceptedException, ElementNotInteractableException):
            pilot.execute_script("arguments[0].click();", button)


    reviews = pilot.find_elements(By.XPATH, './/div[@class="lister-item-content"]')

    ratings = []
    texts = []

    for review in reviews:

        try:
            rating = review.find_element(By.XPATH, './/div[@class="ipl-ratings-bar"]').text.replace('\n', '')
            ratings.append(rating.split('/')[0])
        except NoSuchElementException:
            continue

        title = review.find_element(By.XPATH, './/a[@class="title"]').text.replace('\n', '')

        body = review.find_element(By.XPATH, './/div[contains(@class, "text show-more__control")]').text.replace('\n', '')
        texts.append(f'{title} {body}')

    df = DataFrame({
        'Rating' : ratings,
        'Reviews' : texts
    })

    df.to_csv(f'.\Reviews\{key}.csv')