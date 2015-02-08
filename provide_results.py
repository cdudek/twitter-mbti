__author__ = 'Zera'
import json
import os.path

def get_follower_types(name):
    filename = "evaluated/follower_types_{}.json".format(name)
    if os.path.isfile(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            return data
    else:
        return {}


def account_for_baseline(data):
    mbti_twitter_baseline={'INFP': 0.069, 'INFJ': 0.037, 'INTJ': 0.048, 'INTP': 0.059, 'ISFJ': 0.032, 'ISFP': 0.016, 'ISTJ': 0.101, 'ISTP': 0.048, 'ENFJ': 0.08, 'ENFP': 0.106, 'ENTJ': 0.085, 'ENTP': 0.117, 'ESFJ': 0.021, 'ESFP': 0.016, 'ESTJ': 0.112, 'ESTP': 0.053}
    count=data
    total=0
    for type in data:
        n=len(count[type])
        total=total+n
        count[type]=n
    distribution = count
    for x in distribution:
        distribution[x]=round(count[x] / float(total), 4)
    distribution_factor=[round(distribution[x] / float(mbti_twitter_baseline[x]), 4) for x in distribution]
    print distribution_factor


account_for_baseline(get_follower_types("bmw"))
