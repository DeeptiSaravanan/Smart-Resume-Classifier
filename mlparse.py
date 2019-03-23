import json

import random

import logging

from sklearn.metrics import classification_report

from sklearn.metrics import precision_recall_fscore_support

from spacy.gold import GoldParse

from spacy.scorer import Scorer

from sklearn.metrics import accuracy_score

def convert_dataturks_to_spacy(dataturks_JSON_FilePath):

    try:

        resume = []

        #lines=[]

        #with open(dataturks_JSON_FilePath, 'r') as f:

         #   lines = f.readlines()



        #for line in lines:

         #   data = json.loads(line)

           text = resume['content']

            entities = []

            for annotation in resume['annotation']:

                #only a single point in text annotation.

                point = annotation['points'][0]

                labels = annotation['label']

                # handle both list of labels or a single label.

                if not isinstance(labels, list):

                    labels = [labels]



                for label in labels:

                    #dataturks indices are both inclusive [start, end] but spacy is not [start, end)

                    entities.append((point['start'], point['end'] + 1 ,label))

            resume.append((text, {"entities" : entities}))



        return resume

    #except Exception as e:

     #   logging.exception("Unable to process " + dataturks_JSON_FilePath + "\n" + "error = " + str(e))

      #  return None



import spacy

################### Train Spacy NER.###########

def train_spacy():



    TRAIN_DATA = convert_dataturks_to_spacy("/home/abhishekn/dataturks/entityrecognition/traindata.json")

    nlp = spacy.blank('en')  # create blank Language class

    # create the built-in pipeline components and add them to the pipeline

    # nlp.create_pipe works for built-ins that are registered with spaCy

    if 'ner' not in nlp.pipe_names:

        ner = nlp.create_pipe('ner')

        nlp.add_pipe(ner, last=True)

       



    # add labels

    for _, annotations in TRAIN_DATA:

         for ent in annotations.get('entities'):

            ner.add_label(ent[2])



    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']

    with nlp.disable_pipes(*other_pipes):  # only train NER

        optimizer = nlp.begin_training()

        for itn in range(10):

            print("Starting iteration " + str(itn))

            random.shuffle(TRAIN_DATA)

            losses = {}

            for text, annotations in TRAIN_DATA:

                nlp.update(

                    [text],  # batch of texts

                    [annotations],  # batch of annotations

                    drop=0.2,  # dropout - make it harder to memorise data

                    sgd=optimizer,  # callable to update weights

                    losses=losses)

            print(losses)

train_spacy()        