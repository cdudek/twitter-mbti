__author__ = 'Zera'
import json
from nlp.TextFeatures import NLP

def process(data):
    n=[0,0,0,0,0]
    #n={'symbols':0,'user_mentions':0,'hashtags':0,'urls':0,'media':0};
    for tweet in data['tweets'].values():
        for entity in enumerate(tweet['entities']):
            n[entity[0]]=n[entity[0]]+len(tweet['entities'][entity[1]])
    #print n , " " , len(data['tweets'])
    usr_analysis = [round(float(len(data['tweets'])) / float(x),4) if x > 0 else 1 for x in n]

    nlp = NLP(data)

    usr_analysis.extend(nlp.getPosTweetDist())
    usr_analysis.extend(nlp.getPosDescriptionDist())
    #print len(usr_analysis)


    return usr_analysis

class Sample:
    def __init__(self, file):
        filename = file.split("/")[-1]
        splitpos = filename.find('_')
        self.type = filename[0:splitpos]
        self.twitName = filename[splitpos+1:-5]
        with open(file) as json_data:
            try:
                loaded = json.load(json_data)
                json_data.close()
                self.data = process(loaded)
            except Exception:
                self.data = {}
