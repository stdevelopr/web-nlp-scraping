from scrapy.utils.serialize import ScrapyJSONEncoder
import json
import os

def return_spider_output(output):
    """
    Encode the output into json
    """
    _encoder = ScrapyJSONEncoder(ensure_ascii=False)
    return _encoder.encode(output)


def save_json(output):
    """
    Save a list of spyder's outputs into jsonlines
    """
    with open('finance.jsonl', 'w', encoding='utf-8') as outfile:
        for item in output:
            json.dump(dict(item), outfile, ensure_ascii=False)
            outfile.write('\n')
    return output


def save_b3_csv(output):
    """
    Save the B3 spyder's outputs into csv
    """
    import csv
    with open('b3.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for item in output:
            writer.writerow((item['name'], item['symbol']))

    return output



def get_finance(number):
    data = []
    json_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'finance.jsonl'))
    with open(json_path) as f:
        for index, line in enumerate(f):
            if index == number:
                break
            data.append(json.loads(line))

    return data