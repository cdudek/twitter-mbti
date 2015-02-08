from os import listdir
from os.path import isfile, join
import Sample
import sample_analysis
import evaluate
import json

def main():
    path = "data"
    files = [ f for f in listdir(path) if isfile(join(path,f)) ]
    eval = []
    ml = evaluate.loadML()
    for file in files:
        sample = Sample.Sample("data/{}".format(file))
        print "{}: {}".format(sample.type, sample.twitName)
        if not sample.data:
            continue
        #features.append(twitName)
        real_type = sample_analysis.encode_type(sample.type)
        predicted_type = ml.predict(sample.data)
        result = {"type": evaluate.decodeType(real_type),
                  "prediction": evaluate.decodeType(predicted_type)}
        eval.append(result)

    with open("accuracy_results.json", "w") as f:
        json.dump(eval, f, indent=2)

main()