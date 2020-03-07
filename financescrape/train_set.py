import spacy
import random
import os

TRAINING_DATA = [
        ("Uber blew through $1 million a week", {"entities": [(0, 4, "ORG")]}),
        ("Google rebrands its business apps", {"entities": [(0, 6, "ORG")]})]


nlp = spacy.blank("en")


if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe(ner, last=True)
else:
    ner = nlp.get_pipe('ner')

for _, annotations in TRAINING_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])


other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(200):
        random.shuffle(TRAINING_DATA)
        losses = {}
        for text, annotations in TRAINING_DATA:
            # Updating the weights
            nlp.update([text], [annotations], sgd=optimizer, 
                       drop=0.5, losses=losses)
            # print('Losses', losses)
nlp.to_disk('model')

# docx = nlp("Uber blew through $1 million a week")
# for token in docx.ents:
#     print(token.text, token.label_)