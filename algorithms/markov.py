import numpy as np
import random as rm
import time

def markov():
    # The statespace
    states = ["start","hault","accident"]

    # Possible sequences of events
    transitionName = [["SS","SH","SA"],["HS","HH","HA"],["AS","AH","AA"]]

    # Probabilities matrix (transition matrix)
    transitionMatrix = [[0.2,0.6,0.2],[0.1,0.6,0.3],[0.2,0.7,0.1]]

    if sum(transitionMatrix[0])+sum(transitionMatrix[1])+sum(transitionMatrix[1]) != 3:
        print("Error : total probability is not 1")


    def activity_forecast(days):
        # Choose the starting state
        activityToday = "start"
        # store the sequence of states taken.
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
                elif change == "SH":
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
                elif change == "HS":
                    prob = prob * 0.2
                    activityToday = "start"
                    activityList.append("start")
                else:
                    prob = prob * 0.3
                    activityToday = "hault"
                    activityList.append("hault")
            elif activityToday == "hault":
                change = np.random.choice(transitionName[2],replace=True,p=transitionMatrix[2])
                if change == "AA":
                    prob = prob * 0.1
                    activityList.append("hault")
                    pass
                elif change == "AS":
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


    for _ in range(1,100000):
            start = time.perf_counter()
            list_activity.append(activity_forecast(2))
    stop = time.perf_counter()

    # Check out all the `activityList` we collected    
    # print(list_activity)

    # Iterate through the list to get a count of all activities ending in state:'accident'
    for smaller_list in list_activity:
        if(smaller_list[2] == "accident"):
            count += 1

    # Calculate the probability of starting from state:'start' and ending at state:'accident'
    percentage = (count/100000) * 100
    print("The probability of starting at state:'start' and ending at state:'accident'= " + str(percentage) + "%")

    print("Time elaspsed :",stop - start)