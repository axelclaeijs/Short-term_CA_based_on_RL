

# Source: https://www.geeksforgeeks.org/python-merge-two-lists-into-list-of-tuples/
def merge(list1, list2):

    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list
