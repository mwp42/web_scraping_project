from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from bs4 import BeautifulSoup

driver = webdriver.Chrome(r'./chromedriver.exe') #local path
driver.get("https://twitter.com/search?f=news&vertical=default&q=quantum%20computing&src=typd&lang=en")

SCROLL_PAUSE_TIME = 3
last_height = driver.execute_script("return document.body.scrollHeight")
index = 1
while index < 400:
    index += 1
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        print('scrolling!')
    except:
        print('We are at the end of the page')
        break

csv_file = open('tweets.csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(['Content', 'Author', 'Time','Day','Month','Year','Reply', 'Retweet', 'Like', 'Hashtag', 'Location'])
soup = BeautifulSoup(driver.page_source, "html.parser")

tweets = driver.find_elements_by_xpath('//*[contains(@id,"stream-item-tweet-")]')
for tweet in tweets:
    tweet_dict = {}
    try:
        Content = tweet.find_element_by_xpath('.//div[2]/div[2]/p').text
    except:
        Content = "NA"
    try:
        Author = tweet.find_element_by_xpath('.//div[2]/div[1]/a/span[1]').text
    except:
        Author = "NA"
    try:
        Time = tweet.find_element_by_xpath('.//div[2]/div[1]/small/a').text
        Month = Time.split(' ')[1]
        Day = Time.split(' ')[0]
    except:
        Time = "NA"
        Month = "NA"
        Day = "NA"
    try:
        Time2 = tweet.find_element_by_xpath('.//div[2]/div[1]/small/a').text
        Year = Time2.split(' ')[2]
    except:
        Year = "NA"
    try:
        Reply = tweet.find_element_by_xpath('.//div[2]/div[4]/div[2]/div[1]/button/span/span').text
    except:
        Reply = "NA"
    try:
        Retweet = tweet.find_element_by_xpath('.//div[2]/div[4]/div[2]/div[2]/button[1]/span/span').text
    except:
        Retweet = "NA"
    try:
        Like = tweet.find_element_by_xpath('.//div[2]/div[4]/div[2]/div[3]/button[1]/span/span').text
    except:
        Like = "NA"
    try:
        Hashtag = review.find_element_by_xpath(".//div[1]/div[3]/ul/li[1]/ul").text
        Hashtag = Hashtag.replace('#', ',')
        Hashtag = Hashtag[1:]
    except:
        Hashtag = "NA"

    for tweet_loc in soup.find_all('div', {'class': 'content'}):
        try:
            Location = tweet_loc.find('span', {'class': 'Tweet-geo'})['title'].encode('UTF-8')
        except:
            Location = "NA"


    print('(*)> Tweet Tweet!  '*4)

    tweet_dict['Content'] = Content
    tweet_dict['Author'] = Author
    tweet_dict['Time'] = Time
    tweet_dict['Day'] = Day
    tweet_dict['Month'] = Month
    tweet_dict['Year'] = Year
    tweet_dict['Reply'] = Reply
    tweet_dict['Retweet'] = Retweet
    tweet_dict['Like'] = Like
    tweet_dict['Hashtag'] = Hashtag
    tweet_dict['Location'] = Location

    writer.writerow(tweet_dict.values())


csv_file.close()
driver.close()
print('CSV File Created')

