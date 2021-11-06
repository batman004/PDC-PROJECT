import numpy as np
import random as rm

# The statespace
states = ["start","hault","accident"]

# Possible sequences of events
transitionName = [["SS","SH","SA"],["HH","HS","HA"],["AA","AS","AH"]]

# Probabilities matrix (transition matrix)
transitionMatrix = [[0.2,0.6,0.2],[0.1,0.6,0.3],[0.2,0.7,0.1]]

if sum(transitionMatrix[0])+sum(transitionMatrix[1])+sum(transitionMatrix[1]) != 3:
    print("total probability is not 1")


def activity_forecast(days):
    # Choose the starting state
    activityToday = "start"
    activityList = [activityToday]
    i = 0
    prob = 1
    while i != days:
        if activityToday == "start":
            change = np.random.choice(transitionName[0],replace=True,p=transitionMatrix[0])
            if change == "SS":
                prob = prob * 0.2
                activityList.append("start")
                pass
            elif change == "SR":
                prob = prob * 0.6
                activityToday = "accident"
                activityList.append("accident")
            else:
                prob = prob * 0.2
                activityToday = "hault"
                activityList.append("hault")
        elif activityToday == "accident":
            change = np.random.choice(transitionName[1],replace=True,p=transitionMatrix[1])
            if change == "RR":
                prob = prob * 0.5
                activityList.append("accident")
                pass
            elif change == "RS":
                prob = prob * 0.2
                activityToday = "start"
                activityList.append("start")
            else:
                prob = prob * 0.3
                activityToday = "hault"
                activityList.append("hault")
        elif activityToday == "hault":
            change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2])
            if change == "II":
                prob = prob * 0.1
                activityList.append("hault")
                pass
            elif change == "IS":
                prob = prob * 0.2
                activityToday = "start"
                activityList.append("start")
            else:
                prob = prob * 0.7
                activityToday = "accident"
                activityList.append("accident")
        i += 1    
    return activityList

# To save every activityList
list_activity = []
count = 0

# `Range` starts from the first count up until but excluding the last count
for iterations in range(1,10000):
        list_activity.append(activity_forecast(2))

# Check out all the `activityList` we collected    
#print(list_activity)

# Iterate through the list to get a count of all activities ending in state:'accident'
for smaller_list in list_activity:
    if(smaller_list[2] == "accident"):
        count += 1

# Calculate the probability of starting from state:'start' and ending at state:'accident'
percentage = (count/10000) * 100
print("The probability of starting at state:'start' and ending at state:'accident'= " + str(percentage) + "%")
