# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import spacy
from fuzzywuzzy import fuzz, process
from scrapy.exceptions import DropItem
nlp = spacy.load("pt_core_news_sm")

class FinancescrapePipeline(object):

    def process_item(self, item, spider):
        """
        Process items and discard the items that do not belong to the B3 set.
        """
        entities = nlp(item['title'])
        exist=False
        for ent in entities.ents:
            exist = self.match_entity(ent.text)
            if exist:
                break
        if exist:
            return item
        else:
            raise DropItem("Missing value")


    def match_entity(self, entity):
        """
        Verify if the B3 set contains an entity using fuzzy ratio match
        """
        s= ""
        max_score = 0
        path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'b3.csv'))
        items = self.load_b3(path)
        for item in items:
            if item.lower() in entity.lower():
                return True
            score = fuzz.partial_ratio(entity, item)
            if score > max_score:
                s=item
                max_score = score
        if max_score >= 80:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", s, entity, max_score)
            return True
        else:
            return False

    def load_b3(self, input_path):
        """
        Read a b3 csv file and return a set with it's items.
        """
        b3_set = {"B3", "Bovespa"}
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                b3_set |= set(line.rstrip('\n|\r').split(','))
        return b3_set