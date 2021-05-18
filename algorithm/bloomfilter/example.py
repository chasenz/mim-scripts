from bloomfilter import BloomFilter
import random

n = 200
p = 0.01

bloomf = BloomFilter(n, p)
print("Size of bit array:{}".format(bloomf.size))
print("False positive Probability:{}".format(bloomf.fp_prob))
print("Number of hash functions:{}".format(bloomf.k))

# words to be added
word_present = ['abound', 'abounds', 'abundance', 'abundant', 'accessable',
                'bloom', 'blossom', 'bolster', 'bonny', 'bonus', 'bonuses',
                'coherent', 'cohesive', 'colorful', 'comely', 'comfort',
                'gems', 'generosity', 'generous', 'generously', 'genial']

# word not added
word_absent = ['bluff', 'cheater', 'hate', 'war', 'humanity',
               'racism', 'hurt', 'nuke', 'gloomy', 'facebook',
               'google', 'twitter']

for word in word_present:
    bloomf.insert(word)

random.shuffle(word_present)
random.shuffle(word_absent)
word_test = word_present[10:] + word_absent

random.shuffle(word_test)

for test in word_test:
    result = bloomf.check(test)

    if result:
        if test in word_absent:
            print("Word {} is a false positive".format(test))
        else:
            print("Word {} is probably present".format(test))
    else:
        print("Word {} is definitely not present".format(test))