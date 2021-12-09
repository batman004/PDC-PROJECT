from  functools import *
from multiprocessing import Pool
import time

def map_reduce():
    from data.data import list_of_errors
    list_of_errors = list_of_errors()['raw_data']

    # print(list_of_errors)

    label ={"Error1":"High", "Error2":"High", "Error3":"Low", "Error4":"Low", "Error5":"Medium", "Error6":"Medium"}
    label1 ={"type1":"High", "type2":"High", "type3":"Low", "type4":"Low", "type5":"Medium", "type6":"Medium"}

    # label = list_of_errors()['labelled_data']

    severity = {"High":3, "Medium":2, "Low":1}

    error_type = {"Error1":"type1","Error2":"type2","Error3":"type3","Error4":"type4","Error5":"type5","Error6":"type6"}
    # list out keys and values separately
    key_list = list(error_type.keys())
    val_list = list(error_type.values())


    # mapper function which assings label to each error in the provided chunk
    def mapp(errors,error_type):
        mapped=[]
        for error in errors:
            mapped.append(error_type[error])
        return mapped

    def create_chunks(strings,number_of_chunks):
        x = [strings[i:i + number_of_chunks] for i in range(0, len(strings), number_of_chunks)] 
        return x

    # initialising Pool object which creates 8 threads to run parallel tasks
    pool = Pool(8)

    start = time.time()
    # splitting up large dataset into chunks for parallel computation on each chunk
    data_chunks = create_chunks(list_of_errors, number_of_chunks=8)
    

    # function to return the most frequent element in a list
    def most_frequent(chunk):
        counter = 0
        num = chunk[0]
        for i in chunk:
            curr_frequency = chunk.count(i)
            if(curr_frequency> counter):
                counter = curr_frequency
                num = i
            
        return num

    def frequency(error, errors):
        cnt=0
        for chunk in errors:
            if error in chunk:
                cnt+=1
        return cnt



    # returns the most frequent error while comparing two different chunks 
    def reducer(errors1, errors2):
        cnt1=0
        cnt2=0

        error1_mostf  = most_frequent(errors1)
        error2_mostf  = most_frequent(errors2)

        for error in errors1:
            if(error == error1_mostf):
                cnt1+=1
        for error in errors2:
            if(error == error2_mostf):
                cnt2+=1

        if(cnt2 > cnt1):
            return errors2
        else:

            return errors1

    reduced_all_most_freq = []

    for chunk in data_chunks:

        # print(chunk)
        mapped_chunk = mapp(chunk,error_type)
        # print(mapped_chunk)
        reduced_chunk = reduce(reducer,mapped_chunk)
        # print(reduced_chunk)
        reduced_all_most_freq.append(reduced_chunk)


    pos = val_list.index(most_frequent(reduced_all_most_freq))
    print(f"The error which occurs most frequently is : {most_frequent(reduced_all_most_freq)} \n")
    print(f"Severity of error is : {label1[most_frequent(reduced_all_most_freq)]}\n")
    print(f"The frequency of this error is : {frequency(key_list[pos],list_of_errors)}\n")
    print("amount of time taken : ",time.time() - start )


