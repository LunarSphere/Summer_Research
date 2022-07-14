from csv import *
import pandas as pd
import re
# from csv extract date, tweet, and language.
#dont forget about formatting so i can reread the data later
# remove @user, links, non english tweets
# the point of this program is to read the data from the csv created by hydrate 
# as something readeable to an algorithim this is done by stripping it down to only english tweets and their text
def main():
    dataset = []
    #keywordlist = ['5gcovid', 'curecoronavirus', 'faucicoronavirus', 'faucicovid', 'gatescoronavirus', 'gatescovid']
    # filelist = ['5gcovid', "5gcoronavirus",'curecovid', '5gcovid', 'CoronavirusHoax',\
    #     'curecoronavirus', 'curecovid', 'faucicoronavirus', 'faucicovid', 'gatescoronavirus',\
    #         'gatescovid', 'microchip']\
    filelist = ["gatesfoundation"]
    for j in filelist:
        with open(f'twitter-ids-{j}.csv', newline='') as csvfile:
            readfile = DictReader(csvfile)
            for row in readfile:
                dataset.append([row['created_at'], row['text'],row['lang']])
        for data in dataset:
            alldata = []
            text = data[1]
            year = data[0]
            lang = data[2]
            text = text.lower()
            text = text.replace("\r", "\t")
            text = text.replace("\n", "\t")
            text = re.sub(r'http\S+', '', text) #removes hyper links
            text = re.sub(r'@([A-z])+', '', text) # removes @user
            text = re.sub(r"[^a-zA-Z0-9\s]+", '', text) #removes emojis symbols everything besides single and double quotes
            with open(f"data{j}.txt", "a") as outfile:        
                if lang == 'en':
                    outfile.write(f"{text},{year},{lang},  \n")
        readdata = open(f'data{j}.txt','r')
        for i in readdata:
            alldata.append(i.split(","))
        Twitter = pd.DataFrame(alldata, columns=['content', 'year', 'lang', 'label'])
        Twitter.to_csv(f'Twitter{j}.csv')
if __name__ == '__main__':
    main()
    