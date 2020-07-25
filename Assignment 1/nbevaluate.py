# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 13:35:58 2020

@author: sarthak
"""

import sys

TP_SPAM, FP_SPAM, TN_SPAM, FN_SPAM = 0, 0, 0, 0
TP_HAM, FP_HAM, TN_HAM, FN_HAM = 0, 0, 0, 0
path = ""


def read_path():
    """
        Reading nbmodel.txt
    """
    global path
    if len(sys.argv) >= 2:
        path = sys.argv[1]


def read_output_file():
    """
        Read output.txt
        Calculate True Positive, True Negative, False Positive and 
                  False Negative for Spam and ham
        Call calculate_f1() for spam and ham
    """
    global TP_SPAM, FP_SPAM, TN_SPAM, FN_SPAM
    global TP_HAM, FP_HAM, TN_HAM, FN_HAM
    global path
    output_file = open(path+"nboutput.txt","r", encoding="latin-1")
    i = 0
    for line in output_file:
        i+=1
        arr =  line.split()
        path = arr[1]
        label = arr[0]
        
        #calculating for spam
        if "spam" in path:
            if label == "spam":
                TP_SPAM+= 1
            else:
                FN_SPAM+= 1
        else:
            if label == "ham":
                TN_SPAM+= 1
            else:
                FP_SPAM+= 1
                
        #calculating for ham
        if "ham" in path:
            if label == "ham":
                TP_HAM+= 1
            else:
                FN_HAM+= 1
        else:
            if label == "spam":
                TN_HAM+= 1
            else:
                FP_HAM+= 1
    calculate_f1(TP_SPAM, TN_SPAM, FP_SPAM, FN_SPAM, "SPAM")
    calculate_f1(TP_HAM, TN_HAM, FP_HAM, FN_HAM, "HAM")
        
def calculate_f1(true_positive, true_negative, false_positive, false_negative, label):
    """
    
    Parameters
    ----------
    true_positive : Integer
    true_negative : Integer
    false_positive : Integer
    false_negative : Integer
    label : String - Spam/Ham
    -------
    
        Calculate Precision, Recall and Accuracy.
        Print the performance.
        
    Formula Description
    -------------------
    precision = True Positive/(True Positive + False Positive)
    Recall = True Positive/(True Positive + False Negative)
    F1 = 2 * Precision * Recall / (Precision + Recall)
    Accuracy = True Positive + True Negative / Total
    -------------------
    
    """
    
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    total = true_positive + true_negative + false_positive + false_negative
    f1_score = 2 * precision * recall/ (precision + recall)
    accuracy = (true_positive+true_negative)/total
    print("\n\n###########################################")
    print("\t\t",label)
    print("###########################################")
    print("Precision: ",precision)
    print("Recall: ",recall)
    print("F1-Score:",f1_score)
    print("Accuracy: ",accuracy)
    
    

read_path()
read_output_file()
