from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import random
import provide_results as pr

# Currently using mock data
mbti_types_list=['INFP','INFJ','INTJ','INTP','ISFJ','ISFP','ISTJ','ISTP','ENFJ','ENFP','ENTJ','ENTP','ESFJ','ESFP','ESTJ','ESTP']
type_counts = random.sample(range(101), 16)

def getPLotFromTypeCounts(name):
    print "starting to generate image"
    results = pr.account_for_baseline(pr.get_follower_types(name))
    # Plot histogram using matplotlib bar().
    mbti_types_list=results.keys()
    type_counts=results.values()
    print "here: ",
    print results
    indexes = np.arange(len(mbti_types_list))
    width = 0.8
    plt.figure(figsize=(14, 7))
    plt.bar(indexes, type_counts, width)
    plt.xticks(indexes + width * 0.5, mbti_types_list)
    print "almost there"
    plt.savefig('./static/foo.png')
    print "image saved :D"
    return mbti_types_list

getPLotFromTypeCounts("bmw")