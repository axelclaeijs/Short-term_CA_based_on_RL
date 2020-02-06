
# Merge two lists into list of tuples
# Source: https://www.geeksforgeeks.org/python-merge-two-lists-into-list-of-tuples/
def merge(list1, list2):

    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]

    return merged_list

# Unpack list of tuples into two lists
def unpack(tupleList):

    list1, list2 = zip(*tupleList)
    list1 = list(list1)
    list2 = list(list2)

    return list1, list2

# Set range of array values
def scale(X, x_min, x_max):

    nom = (X - X.min(axis=0))*(x_max - x_min)
    denom = X.max(axis=0) - X.min(axis=0)
    denom[denom == 0] = 1

    return x_min + nom/denom
