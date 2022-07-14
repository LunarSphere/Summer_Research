import os
from datetime import *
# this file uses the snscrape tool to collect data ranging between two dates about a topic and saves the data to a file. 
# adjustments add more variables so there is less hard coding
def dateiterator():
    """
    This function returns a list of all the dates between two end points.
    """
    # initilze startdate enddate and list of dates
    dateslist = []
    start_date = date(2020, 1, 1) 
    end_date = date(2022, 1, 1)
    delta = timedelta(days=1)
    # iterates through dates until all date are added.
    while start_date <= end_date:
        start_date += delta
        dateslist.append(start_date.strftime("%Y-%m-%d"))
    return dateslist

def collectdata():
    """This function interacts with the terminal and gets data for every keyword over a period of time"""
    start_date = date(2020, 1, 1) 
    end_date = date(2022, 1, 1)
    delta = timedelta(days=1)
    keywordlist = ['5gcovid', "5gcoronavirus",'curecovid', '5gcovid', 'CoronavirusHoax',\
        'curecoronavirus', 'curecovid', 'faucicoronavirus', 'faucicovid', 'gatescoronavirus',\
            'gatescovid', 'microchip', 'gatesfoundation']
    for i in keywordlist: 
        os.system("snscrape twitter-search '{2} since:{0} - until:{1} lang:en' >>twitter-datalinksgatesfoundation.txt".format(start_date, end_date,i)) 
def collectids():
    """the purpose of this function is to collect the api keys from the twitter links"""
    twitterids = []
    keywordlist = ['5gcovid', "5gcoronavirus",'curecovid', '5gcovid', 'CoronavirusHoax',\
        'curecoronavirus', 'curecovid', 'faucicoronavirus', 'faucicovid', 'gatescoronavirus',\
            'gatescovid', 'microchip', 'gatesfoundation']
    for i in keywordlist: 
        file = open(f"twitter-datalinks{i.strip()}.txt",'r')
        tweets = file.readlines()
        for tweet in tweets:
        #extract api key
            temptweet = tweet.split("/")
            twitterids.append(temptweet[-1])
        outfile = open(f"twitterids{i.strip()}.txt",'w')
        outfile.write(''.join(twitterids))
        outfile.close()
        file.close()


def main():
    #after using this file run twitterids[keyword].txt in hydrate to get the csv form of the tweets
    # name the csv files twitterids{keyword}.csv
    collectdata()
    collectids()
    print("done")
if __name__ == "__main__":
    main()




