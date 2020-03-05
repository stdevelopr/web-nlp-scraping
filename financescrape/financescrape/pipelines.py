# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import spacy
import json
from fuzzywuzzy import fuzz, process
from scrapy.exceptions import DropItem
nlp = spacy.load("pt_core_news_sm")

class FinancescrapePipeline(object):
    def process_item(self, item, spider):
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
        max_score = 0
        for item in ['arezzo', 'b3', 'vale', 'bovespa', 'alpar on']:
            score = fuzz.ratio(entity, item)
            if score > max_score:
                max_score = score
            print(item, entity, score)
        if max_score > 80:
            return True
        else:
            return False


class JsonWriterPipeline(object):
    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
