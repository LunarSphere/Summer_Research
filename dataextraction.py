from cProfile import label
from csv import *
import pandas as pd
import re
from sklearn.utils import shuffle
# from csv extract date, tweet, and language.
#dont forget about formatting so i can reread the data later
# remove @user, links, non english tweets
# the point of this program is to read the data from the csv created by hydrate 
# as something readeable to an algorithim this is done by stripping it down to only english tweets and their text
def main():
    alldata = []
    # filelist = ['5gcovid', "5gcoronavirus",'curecovid', '5gcovid', 'CoronavirusHoax',\
    #     'curecoronavirus', 'curecovid', 'faucicoronavirus', 'faucicovid', 'gatescoronavirus',\
    #         'gatescovid', 'microchip', 'gatesfoundation']
    filelist = ['sampledata1000.csv']
    for j in filelist:
        stripeddata = []
        dataset = []
        with open(j, newline='') as csvfile:
            readfile = DictReader(csvfile)
            for row in readfile:
                dataset.append([row['year'], row['content'], row['label']])
        for data in dataset:
            text = data[1]
            unstripedtext = data[1]
            label = data[2]
            year = data[0]
            text = text.lower()
            text = text.replace("\r", "\t")
            text = text.replace("\n", "\t")
            text = re.sub(r'http\S+', '', text) #removes hyper links
            text = re.sub(r'@([A-z])+', '', text) # removes @user
            text = re.sub(r"[^a-zA-Z0-9\s]+", '', text) #removes emojis symbols everything besides single and double quotes
            #writes english languge tweets to an outfile, however, could be improved so data collection creates less junk      
            stripeddata.append([text,label])
            # writes stripped data from txt file to a csv 
        Twitterstripped = pd.DataFrame(stripeddata, columns=['content','label'])
        # Twitterstripped.to_csv(f'Twitter{j}.csv')
        Twitterstripped.to_csv(j)
    #collect data for sampling
    # alldf = pd.DataFrame(alldata, columns=['content','label','year','id'])
    # alldf = shuffle(alldf)
    # alldf[:2000].to_csv("sampledata2000.csv")
if __name__ == '__main__':
    main()
    