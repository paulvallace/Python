 oimport sys
import math
import string
import numpy as np

def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X={letter: 0 for letter in string.ascii_lowercase}
    with open(filename,encoding='utf-8') as f:
        for word in f:
            for letter in word:
                letter = letter.casefold()
                if letter in string.ascii_lowercase:
                    if letter in X:
                        X[letter] += 1
                    else:
                        X[letter] = 0
        #used chatgpt to help make each key uppercase and to strip the commas
        X = {key.upper(): value for key, value in X.items()}
        print("Q1")
        for i in X:
            print(i, X[i])
    return X
 
def predict_language(filename):
    e, s = get_parameter_vectors()
    counts = shred(filename)
    print("Q2")
    # Used chatgpt to help me with decimal count
    print("{:.4f}".format(counts["A"] * math.log(e[0])))
    print("{:.4f}".format(counts["A"] * math.log(s[0])))
    
    print("Q3")
    #English
    total = list()
    for i in counts:
        total.append(counts[i])
    e_log_list = [math.log(e[i]) for i in range(len(counts))]
    e_log_list_np = np.array(e_log_list)
    e_total_np = np.array(total)
    English = sum(e_log_list_np * e_total_np) + math.log(.6)
    
    #Spanish
    s_log_list = [math.log(s[i]) for i in range(len(counts))]
    s_log_list_np = np.array(s_log_list)
    s_total_np = np.array(total)
    Spanish = sum(s_log_list_np * s_total_np) + math.log(.4)
    print("{:.4f}".format(English))
    print("{:.4f}".format(Spanish))
    
    print("Q4")

    diff = Spanish - English
    if diff >= 100:
        P_Y_English_X = 0
    elif diff <= -100:
        P_Y_English_X = 1
    else:
        P_Y_English_X = 1 / (1 + math.exp(diff))
    print("{:.4f}".format(P_Y_English_X))
    
predict_language("letter.txt")
