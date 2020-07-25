# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 19:26:23 2020

@author: sarthak
"""
import pycrfsuite
import hw2_corpus_tool as tool
import sys
import time

FIRST_UTTERANCE = "First_Utterance"
SPEAKER_CHANGE = "Speaker_Change"
TRAIN_DIRECTORY = ""
TEST_DIRECTORY = ""
OUTPUT_FILE = ""
MODEL = "baseline.crfsuite"


def featurise(utterance, speaker, index):
    """
        Featurise current dialogue and returns the feature, label and current speaker
        Baseline features:
            Speaker_Change=True/False
            First_Utterance=True
            Tokens_ 
            POS_
            No_Words
    """
    current_feature = []
    current_speaker = getattr(utterance, "speaker")
    tokens = getattr(utterance, "pos")
    
    if index == 0:
        current_feature.append(SPEAKER_CHANGE+"=False")
        current_feature.append(FIRST_UTTERANCE+"=True")
    else:
        if current_speaker == speaker:
            current_feature.append(SPEAKER_CHANGE+"=False")
        else:
            current_feature.append(SPEAKER_CHANGE+"=True")
        # current_feature.append(FIRST_UTTERANCE+"=False")
    if tokens:
        for token in tokens:
            current_feature.append("TOKEN_"+getattr(token, "token"))
            current_feature.append("POS_"+getattr(token, "pos"))
    else:
        current_feature.append("No_Words")
                
    if getattr(utterance, "act_tag"):
        act_tag = getattr(utterance, "act_tag")
    else:
        act_tag.append("No_Tag")
    return current_feature, act_tag, current_speaker


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
        
        for utterance in conversation:
            current_feature, current_label, current_speaker = featurise(utterance, speaker, index)
                
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
        Trains the crfsuite and genereates baseline.crfsuite
    """
    print("Training...")
    trainer=pycrfsuite.Trainer(verbose=False)
    
    for x, y in zip(train_features, train_labels):
        trainer.append(x, y)
        
    trainer.set_params({
        'c1': 1.0,   # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 50,  # stop earlier
    
        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })
    trainer.train(MODEL)   
    print(MODEL," generated!")
    


def predict(test_features, test_labels):
    """
        Generate the file by predicting the test features
    """
    correct = 0
    wrong = 0
    
    crf_tagger = pycrfsuite.Tagger()
    crf_tagger.open(MODEL)
    
    output_file = open(OUTPUT_FILE, 'w+')
    for i in range(len(test_features)):
        predicted_labels = crf_tagger.tag(test_features[i])
        current_test_labels = test_labels[i]
        
        for j in range(len(predicted_labels)):
            output_file.write(predicted_labels[j]+"\n")
            if predicted_labels[j] == current_test_labels[j]:
                correct += 1
            else:
                wrong += 1
               
        output_file.write("\n")
        
    output_file.close()
    
    print(correct, wrong, (correct+wrong))
    accuracy = correct * 100 / (correct+wrong)
    print("Accuracy: "+str(accuracy))
    print(OUTPUT_FILE+" generated!")


    

if __name__ == '__main__':
    start =  time.time()
    # Check len of args for file names 
    if len(sys.argv) >=3:
        TRAIN_DIRECTORY = sys.argv[1]
        TEST_DIRECTORY = sys.argv[2]
        OUTPUT_FILE = sys.argv[3]
    else:
        TRAIN_DIRECTORY = "prof_dataset/train"
        TEST_DIRECTORY = "prof_dataset/test"
        OUTPUT_FILE = "sarthak_baseline.txt"    
    
    print("Loading Training Data from: "+TRAIN_DIRECTORY)
    train_conversation_list = list(tool.get_data(TRAIN_DIRECTORY))
    train_features, train_labels = generate_features(train_conversation_list)
    train_crf(train_features, train_labels)
    print("Loading Test Data from: "+TEST_DIRECTORY)
    test_conversation_list = list(tool.get_data(TEST_DIRECTORY))
    test_features, test_labels = generate_features(test_conversation_list)
    predict(test_features, test_labels)
    
    print("total_time = ",time.time() - start)
    