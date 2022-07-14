import os
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

links = []
with open("sampledata1000.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        links.append(row[-1])

links = links[1:]
print(len(set(links)))


label = {}
count = 0
done = open("label_result.txt").read()
with open("label_result.txt", "a") as f:
    for link in links:
        count = count + 1
#        print('tweet: ' + str(count))
        if link in done:
            continue
        try:
            driver.get('https://twitter.com/palashv2/status/' + link)
        except:
            continue
        value = input()
        if value == "s" or value == "S":
            break
        label[link] = value
        x = f.write(link + '\t' + label[link] + '\n')


driver.close()