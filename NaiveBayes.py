from functools import reduce
from collections import Counter
import numpy
import pandas as pd
'''
Areen Abu Caf 212654719
Fadi Amon 212472542
Rasheed Abu Mdeagm 212555650
'''


def ReadCsv(FileName):
    '''
    return the data frame of the csv file
    :param FileName: the file name of the csv
    :return: the data frame of the csv file
    '''
    df = pd.read_csv(FileName)
    return df


def ReadStructure(FileName):
    '''
    reading the structure file and return a dict that contain the structure of the file
    :param FileName: the file name of the structure file
    :return: a dict that contain the structure of the file
    '''

    f = open(FileName, "r")
    struct = {}
    for line in f:
        x = line.split()
        if x[2] == 'NUMERIC':
            struct[x[1]] = x[2]
        else:
            struct[x[1]] = [i for i in (x[2])[1:len(x[2]) - 1].split(',')]
    f.close()
    return struct


def make_prod(x, y):
    '''
    :param x: a tuple
    :param y: a tuple
    :return: a prod of the 2 tuples
    '''
    make_pairs = lambda el, lst: tuple(map(lambda x: (el, x), lst))
    c_prod = lambda lst1, lst2: tuple(make_pairs(x, lst2) for x in lst1)
    flat_c_prod = lambda lst1, lst2: reduce(lambda x, y: x + y, c_prod(lst1, lst2), ())
    return list(flat_c_prod(x, y))


def Build_probability_For_One_Column(Atrr, Class, attrs_Atrr, attrs_Class):
    '''
    Build a probability for a one column
    '''
    couples = list(zip(Atrr, Class))
    Original_couples = make_prod(attrs_Atrr, attrs_Class)
    count = 0

    # Laplacian
    if len(Original_couples) != len(set(couples)):
        for coup in Original_couples:
            if coup not in couples:
                couples.append(coup)
                count += 1

    count_class = {}

    for indx in couples:
        if indx[1] in count_class:
            count_class[indx[1]] += 1
        else:
            count_class[indx[1]] = 1

    # Calculate probability
    counter_values = {}
    for x in Counter(couples):
        counter_values[x] = Counter(couples)[x] / (count_class[x[1]])

    return counter_values


def probability(table, attr):
    '''
    build a probability for a given attr
    '''
    sum = 0
    for i in table:
        if attr in i:
            sum += table[i]
    return sum


def conditional_probability(table, attr1, attr2):
    '''
    build a conditional probability for 2 attrs
    '''
    if type(attr1)  not in [numpy.int64,numpy.float64]:
        attr1=attr1.lower()
        return table[(attr1, attr2)]

    for i in table:
        if attr1 in i[0]:
            return table[(i[0], attr2)]


def Testing_model(Path,model,test):
    '''
    return the classifications of the rows of the given data frame
    :param Path: a path that contain the files
    :param model: the model
    :param test: the data frame that we want to test the model on it
    :return:classifications of the rows of the given data frame
    '''

    struct = ReadStructure(Path+'/Structure.txt')
    prediction=[]
    columns = test.columns.tolist()
    rows = []
    for i in range(0, test.shape[0]):
        rows.append(test.iloc[i].tolist())


    for row in rows:
        lst = row[:len(row) - 1]
        class_prob = {}
        for class_attr in struct['class']:
            sum = probability(model[columns[0]], class_attr)
            for index in range(0, len(lst)):
                sum = sum * conditional_probability(model[columns[index]], lst[index], class_attr)
            class_prob[class_attr] = sum

        # Getting the max probability from class atrrs in one row
        prediction.append(list(filter(lambda t: t[1] == max(class_prob.values()), class_prob.items()))[0][0])

    return prediction


def NaiveBayes(Path,train):
    '''
    return and build a model on the given data frame
    :param Path: the path of the files
    :param train: the train data frame
    :return: a model
    '''
    # load files
    struct = ReadStructure(Path+'/Structure.txt')

    # Build Model
    model = {}
    for key in struct:
        if key != 'class':
            if struct[key] == 'NUMERIC':
                model[key] = Build_probability_For_One_Column(train[key].tolist(), train['class'].tolist(),
                                                              set(train[key].tolist()), struct['class'])
            else:
                model[key] = Build_probability_For_One_Column(train[key].tolist(), train['class'].tolist(), struct[key],
                                                              struct['class'])

    return model
