# Install tqdm with https://pypi.org/project/tqdm/
# used as a progress bar
from tqdm import tqdm

## Install matplotlib with 
# https://pypi.org/project/matplotlib/
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def draw_figure(title, day, data):
    """Creates a graph of Given Data"""
    fig, ax = plt.subplots(1,1)
    plt.title('Daily ' + title)
    plt.xlabel('Days from 2020, 1, 1 to 2022, 1, 1')
    plt.ylabel(title)
    plt.plot(day, data)
    plt.savefig(f'results/{title}.png')

from datetime import *
import pandas as pd
from csv import * 
import tweepy

def retrievedata(file):
    """Extracts Data from the predicted data file"""
    RoFtotal = [0,0] #(Nonrumor, Rumor)
    otherdata = [] #[tweet,tweetid,date,RumorOrNot]
    start_date = date(2020, 1, 1) 
    end_date = date(2022, 1, 1)
    delta = timedelta(days=1)
    filename = f"Tweets_results/{file}predictions.txt" 
    with open(filename, newline='') as data:
        dailyrumors = {} #{"day":number of rumors for that day}
        for row in data:
            # extract data from line of text
            row = row.split(",")
            # Create date 
            day = row[3].split(" ") 
            month = day[1]
            datetime_object = datetime.strptime(month, "%b")
            month = datetime_object.month
            day = date(int(day[-1]),month,int(day[2])) 
            ToF = int(row[1]) #rumor or not. 0 = rumor 1 = Not rumor
            tweetid = row[2] #id of tweet
            tweet = row[0] #tweet text
            otherdata.append([tweet,tweetid,day,ToF])
            #get number of Rumor or non Rumor Tweets Total
            if ToF == 1: #non Rumor 
                RoFtotal[0]+=1
            elif ToF == 0: #Rumor
                RoFtotal[1] += 1 
            if day not in dailyrumors.keys(): 
                dailyrumors[day] = [0,0]
                if ToF == 1: #non Rumor 
                    dailyrumors[day][0]+=1
                elif ToF == 0: #rumor
                    dailyrumors[day][1]+=1
            else:   
                if ToF == 1: #non Rumor 
                    dailyrumors[day][0]+=1
                elif ToF == 0: #rumor
                    dailyrumors[day][1]+=1
    return dailyrumors, otherdata, RoFtotal

def rumor_lookup(file):
    """
    Creates dictionary of tweet ids for rumors and if true or false
    """
    rumorlookup = {}
    filename = f"Tweets_results/{file}predictions.txt"
    with open(filename, newline='') as data:
         for row in data:
            row = row.split(",")
            tweetid = row[2]
            ToF = int(row[1])
            rumorlookup[tweetid] = ToF
    return rumorlookup

def topicdatacollection(topic):
    """This funciton gathers numerical data about topics such as rumorpercentage daily tweets,
    and rumor tweets 
    """
    rumors = []
    rumorpercentage = []
    topictweets = []
    days = []
    day = 0
    #retrievedata for topic
    dailyrumors,otherdata,RoFtotal = retrievedata(topic) 
    #gets daily values
    for x in dailyrumors.values():
        day+=1
        days.append([day])
        rumors.append([x[1]]) #rumor tweets
        rumorpercentage.append([(x[1]/(x[1]+x[0]))*100]) # percentage
        topictweets.append([x[1]+x[0]]) #tweets about topic
    #figure out how to save everything to one figure and save the figure without it opening
    #plot and save rumor data
    draw_figure(f'{topic} Rumors',days,rumors) #graph of rumors per day 
    draw_figure(f'Percentage of Rumors About {topic}',days,rumorpercentage) #graph of rumor percentage per day
    draw_figure(f'Total Tweets About {topic}',days,topictweets) #graph of tweets about topic perday 


def totaldatacollection(days):
    """
    Same function as topicdatacollection(topic). 
    execpt it collects data on all tweets within the data set instead of by topic.
    """
    rumors = []
    rumorpercentage = []
    topictweets = []
    dayslist = []
    day = 0 
    topiclist = ['5gcovid', "5gcoronavirus",'curecovid', 'CoronavirusHoax',\
        'curecoronavirus', 'faucicoronavirus', 'faucicovid', 'gatescoronavirus',\
            'gatescovid', 'microchip', 'gatesfoundation']
    totaldailyrumors = {}
    for i in days: 
        totaldailyrumors[i] = [0,0]
    for j in topiclist:
        dailyrumors,otherdata,RoFtotal = retrievedata(j)
        for key in dailyrumors.keys():
            totaldailyrumors[key][0] += dailyrumors[key][0] 
            totaldailyrumors[key][1]+= dailyrumors[key][1]
    for x in totaldailyrumors.values():
        day+=1
        dayslist.append([day])
        rumors.append([x[1]])
        rumorpercentage.append([((x[1]+1)/((x[1]+x[0])+1))*100])#calculates percentage rumors/total number of tweets * 100
        topictweets.append([x[1]+x[0]])
        #figure out how to save everything to one figure and save the figure without it opening
        #plot and save rumor data
    draw_figure(f'All Rumors',dayslist,rumors)
    draw_figure(f'Percentage of allRumors',dayslist,rumorpercentage) 
    draw_figure(f'Total Tweets About Rumors',dayslist,topictweets)
    #Same task as topic data collection captures all of the data 

def statisticanalysis(topic):
    """
    return total number of retweets and likes about each topic. Outputs a file containing 
    userids and the number of tweets they have spread
    """
    favoritecount = 0
    retweet = 0 
    userdatadictionary = {}
    sorteduserdatadictionary = {}
    #dailyrumors,otherdata,RoFtotal  = retrievedata(topic)
    outfile = open(f"userdata/userdata{topic}.txt", 'w')
    with open(f"Raw_results/Twitter-ids-{topic}.csv") as f:
        readfile = DictReader(f)
        # gets retweeets and likes
        for row in readfile:
            if row['user_id'] in userdatadictionary.keys():
                userdatadictionary[row['user_id']] += 1
            else:
                userdatadictionary[row['user_id']] = 1
            favoritecount += int(row['favorite_count'])
            retweet += int(row['retweet_count'])
        # sort dictionary with users and the number of tweets they have about a topic
        sorted_keys = sorted(userdatadictionary, key=userdatadictionary.get)
        for key in sorted_keys:
            sorteduserdatadictionary[key] = userdatadictionary[key]
        for key in sorted_keys:
            outfile.write(f"{key},{sorteduserdatadictionary[key]}\n")
    outfile.close()
    return favoritecount,retweet

def user_analysis():
    #separate by if it is a rumor or not so rumor dictionary and non rumor dictionary
    #gets number of rumor tweets of a user for all of the files
    print("running")
    topiclist = ['5gcovid', "5gcoronavirus",'curecovid', 'CoronavirusHoax',\
        'curecoronavirus', 'faucicoronavirus', 'faucicovid', 'gatescoronavirus',\
            'gatescovid', 'microchip', 'gatesfoundation']
    userdatadictionary = {}
    userdatadictionary2 = {}
    sorteduserdatadictionary = {}
    sorteduserdatadictionary2 = {}
    outfile = open(f"userdata/userdataall.txt", 'w')
    #adds number of user rumor tweet ids to a set and the length of the set is the number of rumors they have spread
    for i in topiclist:
        rumorlookup = rumor_lookup(i)
        with open(f"Raw_results/Twitter-ids-{i}.csv") as f:
            readfile = DictReader(f)
            for row in readfile:
                if row['user_id'] in userdatadictionary2.keys():
                    userdatadictionary2[row['user_id']].add(row['id'])
                else:
                    userdatadictionary2[row['user_id']] = set()
                    userdatadictionary2[row['user_id']].add(row['id'])
                if row['user_id'] in userdatadictionary.keys() and rumorlookup[row['id']] == 0:
                    userdatadictionary[row['user_id']].add(row['id']) 
                elif rumorlookup[row['id']] == 0:
                    userdatadictionary[row['user_id']] = set()
                    userdatadictionary[row['user_id']].add(row['id'])
    #sorts users by who has the most rumor tweets
    for key in userdatadictionary.keys():
        userdatadictionary[key] = len(userdatadictionary[key])
        userdatadictionary2[key] = len(userdatadictionary2[key])
    sorted_keys = sorted(userdatadictionary, key=userdatadictionary.get)
    for key in sorted_keys:
        sorteduserdatadictionary[key] = userdatadictionary[key]
        sorteduserdatadictionary2[key] = userdatadictionary2[key]
    for key in sorted_keys:
        #output user id, number of tweets and percentage of rumors to non rumors
        outfile.write(f"{key},{sorteduserdatadictionary[key]},{(sorteduserdatadictionary[key]/sorteduserdatadictionary2[key])*100}\n")
    outfile.close()

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
def sentiment_analysis():
    """
    Save ROF,ID,SentimentScore to a file
    """
    topiclist = ['5gcovid', "5gcoronavirus",'curecovid', 'CoronavirusHoax',\
        'curecoronavirus', 'faucicoronavirus', 'faucicovid', 'gatescoronavirus',\
            'gatescovid', 'microchip', 'gatesfoundation']
    outfile = open(f"userdata/sentiment.txt", 'w')
    for i in topiclist:
        dailyrumors,otherdata,RoFtotal= retrievedata(i)
        for j in otherdata:
            text = j[0]
            RoF = j[3]
            tweetid = j[1]
            analyzer = SentimentIntensityAnalyzer()
            vs = analyzer.polarity_scores(text)
            outfile.write(f"{RoF},{tweetid},{vs['compound']}\n")
        print("soon")
    outfile.close()

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm

def linear_regressiontrend(days, rumorcount):
    # Overall fixation across all subreddits
    periods = 0
    period_counts = []
    period_count = 0
    counts = rumorcount
    for i in range(len(days)):
        period_counts.append(i)

    X = np.array(period_counts).reshape(-1,1)
    y = np.array(counts).reshape(-1,1)
    print(X,y)
    reg = LinearRegression()
    reg.fit(X, y)
    print("The linear model is: Y = {:.5} + {:.5}X".format(reg.intercept_[0], reg.coef_[0][0]))

    X = counts
    y = period_counts
    X2 = sm.add_constant(X)
    est = sm.OLS(y, X2)
    est2 = est.fit()
    print(est2.summary())
    return None
from scipy import stats
from scipy.stats import wilcoxon
def welchtest(rumor,nonrumor):
    print("Welchtest:")
    print(stats.shapiro(rumor))
    print(stats.shapiro(nonrumor))
    print(stats.ttest_ind(rumor, nonrumor, equal_var = False))
def wilcoxon_test(rumor,nonrumor):
    print("wilcoxontest")
    w, p = wilcoxon(rumor, nonrumor)
    print('Rumor,Nonrumor:', w, ',',p)
def alldatalinearregression(days):
    rumors = []
    rumorpercentage = []
    topictweets = []
    dayslist = []
    day = 0 
    topiclist = ['5gcovid', "5gcoronavirus",'curecovid', 'CoronavirusHoax',\
        'curecoronavirus', 'faucicoronavirus', 'faucicovid', 'gatescoronavirus',\
            'gatescovid', 'microchip', 'gatesfoundation']
    totaldailyrumors = {}
    values = [] #rumors per day
    nonrumorvalues = []
    for i in days: 
        totaldailyrumors[i] = [0,0]
    for j in topiclist:
        dailyrumors,otherdata,RoFtotal = retrievedata(j)
        for key in dailyrumors.keys():
            totaldailyrumors[key][0] += dailyrumors[key][0] 
            totaldailyrumors[key][1]+= dailyrumors[key][1]
    for key in totaldailyrumors.keys():
        values.append(totaldailyrumors[key][1])
        nonrumorvalues.append(totaldailyrumors[key][0])
        
    linear_regressiontrend(days,values)
    welchtest(values,nonrumorvalues)
    wilcoxon_test(values,nonrumorvalues)
#task get number of rumor and non rumor tweets for each topic and also for everytopic. 
#get percentage of rumors, daily tweets, rumor tweets

# get number of tweets about a topic per day
#later get number of rumor tweets perday
def averagesentiment():
    rumorsentiment = []
    nonrumorsentiment = []
    f = open("userdata/sentiment.txt", 'r')
    data = f.readlines()
    for line in data:
        line = line.split(",")
        if int(line[0]) == 0:
            rumorsentiment.append(float(line[2]))
        else:
            nonrumorsentiment.append(float(line[2]))
    averagerumorsentiment = sum(rumorsentiment)/len(rumorsentiment)
    averagenonrumorsentiment = sum(nonrumorsentiment)/len(nonrumorsentiment)
    difference = abs(averagenonrumorsentiment-averagerumorsentiment)
    print(f"average rumor sentiment: {averagerumorsentiment}")
    print(f"average non-rumor sentiment: {averagenonrumorsentiment}")
    print(f"average sentiment difference: {difference}")
    return None
def main():
    topiclist = ['5gcovid', "5gcoronavirus",'curecovid', 'CoronavirusHoax',\
        'curecoronavirus', 'faucicoronavirus', 'faucicovid', 'gatescoronavirus',\
            'gatescovid', 'microchip', 'gatesfoundation']
    dailyrumors,otherdata,RoFtotal= retrievedata('gatesfoundation')
    days = dailyrumors.keys()
    # for i in topiclist:
    #     topicdatacollection(i) 
    #     favorite, retweet = statisticanalysis(i)
    #     print(f"{i} Like Count = {favorite} Retweet Count = {retweet}")
    # totaldatacollection(days)
    # user_analysis()
    # print("running")
    # sentiment_analysis()
    # print("done")
    #prints data
    #alldatalinearregression(days) #printsdata
    averagesentiment() #printsdata
if __name__ == "__main__":
    main()

