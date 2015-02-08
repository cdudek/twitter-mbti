from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import random

# Currently using mock data
mbti_types_list=['INFP','INFJ','INTJ','INTP','ISFJ','ISFP','ISTJ','ISTP','ENFJ','ENFP','ENTJ','ENTP','ESFJ','ESFP','ESTJ','ESTP']
type_counts = random.sample(range(101), 16)

# Plot histogram using matplotlib bar().
indexes = np.arange(len(mbti_types_list))
width = 0.8
plt.figure(figsize=(14, 7))
plt.bar(indexes, type_counts, width)
plt.xticks(indexes + width * 0.5, mbti_types_list)
plt.savefig('foo.png')
