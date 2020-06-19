import random
import datetime

random.seed(datetime.datetime.now())

def roll(dieCount,dieSize):
    result = random.randint(dieCount, dieSize)
    return result
