from data.data import list_of_errors

list_of_errors = list_of_errors()['raw_data']

dataset = list_of_errors

import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
import time

def apriori_algo():

    oht = TransactionEncoder()

    oht_ary = oht.fit(dataset).transform(dataset)

    df = pd.DataFrame(oht_ary, columns=oht.columns_)
    print(df)

    t0 = time.time()
    frequent_error = apriori(df, min_support=0.6, use_colnames=True)
    print()
    print(frequent_error)

    rules = association_rules(frequent_error, metric ="lift", min_threshold = 0.7)
    t1 = time.time()
    ttotal = t1 - t0
    print()
    print(rules)
    print()
    print("Total time taken :",ttotal)