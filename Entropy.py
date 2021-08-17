from math import log
import numpy as np

'''
Areen Abu Caf 212654719
Fadi Amon 212472542
Rasheed Abu Mdeagm 212555650
'''

def entropy(list):
    '''
    :param list: List of data
    :return: Entropy of the list
    '''
    temp = set(list)
    ent = 0
    for i in temp:
        ent += -((list.count(i) / len(list)) * log(list.count(i) / len(list),2))
    return ent




def InfoGain(data, attr):
    '''
    :param data: Dictionary of the data
    :param attr: Attribute of the wanted data
    :return: Information gain of the attribute according to the class
    '''
    total_entropy = entropy(data["class"].tolist())
    values, counts = np.unique(data[attr], return_counts=True)
    weightes = []
    for i in range(0, len(values)):
        weightes.append((counts[i] / sum(counts)) * entropy(data[data[attr] == values[i]]['class'].tolist()))
    return total_entropy - sum(weightes)



def Conditional_Entropy(list1, list2):
    '''

    :param list1: List of data.
    :param list2: List of data.
    :return: The conditional entropy of the lists.
    '''
    if len(list1) != len(list2):
        raise ValueError("the length of the lists must be equal")

    temp1 = []
    for i in range(len(list1)):
        temp1.append((list1[i], list2[i]))

    temp2 = set(temp1)
    ent = 0
    for i in temp2:
        ent += -((temp1.count(i) / len(temp1)) * log((temp1.count(i) / len(temp1)) / (list2.count(i[1]) / len(list1)),
                                                     2))
    return ent




def mutual_Information(X, Y):
    '''

    :param X: list of data.
    :param Y: list of data.
    :return: mutual information of the lists.
    '''
    HY = entropy(Y)
    HYX = Conditional_Entropy(Y, X)
    return HY - HYX




