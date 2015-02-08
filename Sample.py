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
    usr_analysis = [round(x / float(len(data['tweets'])),4) if len(data['tweets']) > 0 else 0 for x in n]

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
        print "x"
        with open(file) as json_data:
            #try:
                print "a"
                loaded = json.load(json_data)
                print "b"
                json_data.close()
                print "c"
                self.data = process(loaded)
                print "processed {}".format(self.data)
            #except Exception:
            #    self.data = {}
