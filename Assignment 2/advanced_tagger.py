# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 14:17:55 2020

@author: sarthak
"""

import pycrfsuite
import hw2_corpus_tool as tool
import sys
import time
from collections import deque

FIRST_UTTERANCE = "First_Utterance"
SPEAKER_CHANGE = "Speaker_Change"
LAST_UTTERANCE = "Last_Utterance"
TRAIN_DIRECTORY = ""
TEST_DIRECTORY = ""
OUTPUT_FILE = ""
MODEL = "advanced.crfsuite"


def featurise(utterance, speaker, index, prev_utterances, count):
    """
        Featurise current dialogue and returns the feature, label and current speaker 
        Advanced Feature Set: 
        -   POS tag Counts in the current Utterances.
        -   Appended 'Text' of utterance instead of "No_Words" if token is blank.
        -   Sub_Utterance_Count: The Count of Utterance by Same Speaker.
        -   Included last 3 characters from text:   "/"     = end of complete unit				
                                                    "-/"    = end of cut-off unit				
                                                    Neither = unit continues to next turn by same speaker 			
                                                    Refernece - Annontation Manual - http://web.stanford.edu/~jurafsky/ws97/manual.august1.html
        -   cut_off=True/False:  Based on above Description.
        -   end_unit=True/False: Based on above Description.
        -   contains_question_mark=True/False: If there is Question Mark in 'Text'
        -   Data from Previous 2 Utterance: Backward Looking Function   
                                            Reference - https://www.cs.rochester.edu/research/cisd/resources/damsl/RevisedManual/
                                            Included POS Tags, Last 3 Characters, contains_question_mark, cut_off, end_unit
    """
    current_feature = []
    current_speaker = getattr(utterance, "speaker")
    tokens = getattr(utterance, "pos")
    text = getattr(utterance, "text")
    sub_feature = []
    
    if index == 0:
        current_feature.append(FIRST_UTTERANCE+"=True")
        current_feature.append(SPEAKER_CHANGE+"=False")
        count = 1
    else:
        current_feature.append(FIRST_UTTERANCE+"=False")
        if current_speaker == speaker:
            current_feature.append(SPEAKER_CHANGE+"=False")
            count += 1
        else:
            count = 1
            current_feature.append(SPEAKER_CHANGE+"=True")
    
    current_feature.append("Subsequence_Number="+str(count))
            
    
    ## Appending previous utterance data - Backward Looking Function
    
    for i,prev_utterance in enumerate(prev_utterances):
        # prev_utterance = prev_utterances[prev_len-i-1]
        for prev_feature in prev_utterance:
            current_feature.append(str(i)+"_Prev_"+prev_feature)
    
        
        
    pos_dict = {}
    if tokens:
        for token in tokens:
            pos = getattr(token, "pos")
            if pos not in pos_dict:
                pos_dict[pos] = 1
            else:
                pos_dict[pos] += 1
            current_feature.append("TOKEN_"+getattr(token, "token"))
            current_feature.append("POS_"+pos)
            sub_feature.append("POS_"+pos)
    else:
        sub_feature.append("NO_WORDS")
        current_feature.append("TEXT_"+text)
        current_feature.append("TEXT_"+text)
        current_feature.append("COUNT_POS_None")
    
    ## Appending pos tag count
    for pos_key in pos_dict:
        current_feature.append("COUNT_"+pos_key+"="+str(pos_dict[pos_key]))
    
    
    
    
    last, second_last, third_last = "", "", ""
    if len(text) > 0:
        last = text[-1]
    if len(text) > 1:
        second_last = text[-2:]
    if len(text) > 2:
        third_last = text[-3:]
    
    # current_feature.append("LEN="+str(len(text)))
    
    current_feature.append(last)
    current_feature.append(second_last)
    current_feature.append(third_last)
    
    sub_feature.append(last)
    sub_feature.append(second_last)
    sub_feature.append(third_last)
            
    
    #   "/"         = end of complete unit				
    #   "-/"        = end of cut-off unit				
    #   Neither     = unit continues to next turn by same speaker  
        
    if second_last == '-/' or third_last == '- /':
        current_feature.append("cut_off=True")
        sub_feature.append("cut_off=True")
    else:
        current_feature.append("cut_off=False")
        sub_feature.append("cut_off=False")
        
    if second_last == ' /':
        current_feature.append("end_unit=True")
        sub_feature.append("end_unit=True")
    else:
        current_feature.append("end_unit=False")
        sub_feature.append("end_unit=False")
    

    if '?' in text:
        current_feature.append("contains_ques_mark=True")
        sub_feature.append("contains_ques_mark=True")
    else:
        current_feature.append("contains_ques_mark=False")
        sub_feature.append("contains_ques_mark=False")
    
    if getattr(utterance, "act_tag"):
        act_tag = getattr(utterance, "act_tag")
    else:
        act_tag.append("No_Tag")
    
    prev_utterances.appendleft(sub_feature)
    
    return current_feature, act_tag, current_speaker, count, prev_utterances
    

def generate_features(conversation_list):
    """
        Returns feature vector and labels 
    """
    global FIRST_UTTERANCE, SPEAKER_CHANGE
    feature_list=[]
    label_list=[]
    print("Generating Features")
    for conversation in conversation_list:
        speaker = ""
        index = 0
        features = []
        labels = []
        count = 0
        prev_utterances = deque(maxlen=3)
        for utterance in conversation:
            current_feature, current_label, current_speaker, count, prev_utterance = featurise(utterance, speaker, index, prev_utterances, count)
            
            labels.append(current_label)
            features.append(current_feature)
            index += 1
            speaker = current_speaker
        feature_list.append(features)
        label_list.append(labels)
    print("Features Length: ", str(len(feature_list)))
    
    return feature_list, label_list


def train_crf(train_features, train_labels):
    """
        Trains the crfsuite and genereates advanced.crfsuite
    """
    print("Training...")
    trainer=pycrfsuite.Trainer(verbose=False)
    
    for x, y in zip(train_features, train_labels):
        trainer.append(x, y)
        
    trainer.set_params({
        'c1': 1.0,   # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 50,  # stop earlier
        'feature.possible_transitions': True
    })
    trainer.train(MODEL)   
    print(MODEL," generated!")
    


def predict(test_features, test_labels):
    # correct = 0
    # wrong = 0
    
    crf_tagger = pycrfsuite.Tagger()
    crf_tagger.open(MODEL)
    
    output_file = open(OUTPUT_FILE, 'w+')
    for i in range(len(test_features)):
        predicted_labels = crf_tagger.tag(test_features[i])
        # current_test_labels = test_labels[i]
        for j in range(len(predicted_labels)):
            output_file.write(predicted_labels[j]+"\n")
            
            # if predicted_labels[j] == current_test_labels[j]:
            #     correct += 1
            # else:
            #     wrong += 1
               
        output_file.write("\n")
        
    output_file.close()
    
    # print(correct, wrong)
    # accuracy = correct * 100 / (correct+wrong)
    # print("Accuracy = ", str(accuracy))
    
    print(OUTPUT_FILE+" generated!",)


    

if __name__ == '__main__':
    
    start =  time.time()
    
     # Check len of args for file names 
    if len(sys.argv) >=3:
        TRAIN_DIRECTORY = sys.argv[1]
        TEST_DIRECTORY = sys.argv[2]
        OUTPUT_FILE = sys.argv[3]
    else:
        TRAIN_DIRECTORY = "prof_dataset/train"
        TEST_DIRECTORY = "swda_new/test"
        OUTPUT_FILE = "advanced_output.txt"    
    
    print("Loading Training Data from: "+TRAIN_DIRECTORY)
    train_conversation_list = list(tool.get_data(TRAIN_DIRECTORY))
    train_features, train_labels = generate_features(train_conversation_list)
    train_crf(train_features, train_labels)
    print("Loading Test Data from: "+TEST_DIRECTORY)
    test_conversation_list = list(tool.get_data(TEST_DIRECTORY))
    test_features, test_labels = generate_features(test_conversation_list)
    predict(test_features, test_labels)
    
    print("total_time = ",time.time() - start)