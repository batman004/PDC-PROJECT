from algorithms.apriori import apriori_algo
from algorithms.markov import markov
from algorithms.map_reduce import map_reduce
from algorithms.kmeans import kmeans

print("****************************** Phase 1 : Data Analysis  *********************************************\n")

print("Executing MAP REDUCE \n")
map_reduce()

print("****************************** Phase 2 : Data and Signal Processing Module  *************************\n")
print("Executing K-means \n")
kmeans()

print("****************************** Phase 3 : Activity Forecast Module  ***********************************\n")

print("Executing Markov model\n")

markov()


print("****************************** Phase 4 : Accident Factor Analysis  ************************************\n")

print("Executing Apriori\n")

apriori_algo()