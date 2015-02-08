__author__ = 'Zera'
from sample_analysis import process
import json

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
