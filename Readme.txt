###USEAGE GUIDE FOR RECREATING THIS PROJECT###
STEP1: Install all libraries and Create a twitter developer account Also read documentation about libraries
Step2: install snscrape app https://github.com/JustAnotherArchivist/snscrape
Step3: run data_collection.py the keywords list can be altered to find new topics
step4: data_collection should return files named "twitterids{topic}.txt"
step5: run these files through Hydrate to collect their data as a csv file dowload link: https://github.com/DocNow/hydrator
step6: run data_extraction.py on the previous files to generate a sample dataset named "sampledata1000.csv"
step7: run data_extractionnonsample.py on the previous files to generate "Twitter{topic}.csv"
step8: run "sampledata1000.csv" through CT_BERT.ipynb to train the model
step9: use the model to label the The datasets named "Twitter{topic}.csv"
step10: run label_data.py on the outputfile named "{topic}predictions.txt" to generate the results. 