from klein import  Klein
import json
from spyder_runner import  SpiderRunner
from utils import return_spider_output, save_json, save_b3_csv, get_finance
from financescrape.spiders import b3, financenews, ultimoinstate
import spacy

app = Klein()
nlp = spacy.load("pt_core_news_sm")

@app.route('/api/mine_save/<int:num>')
def mine_save(request, num):
    """
    Mine and save the news from financenews and ultimoinstante.
    Return the last <int:num> news downloaded.
    """
    runner = SpiderRunner()

    deferred = runner.crawl(financenews.FinanceNews)
    deferred.addCallback(save_json)


    deferred = runner.crawl(ultimoinstate.UltimoInstante)
    deferred.addCallback(save_json)

    output = get_finance(num)

    return json.dumps(output)


@app.route('/api/extract_entities/<int:num>')
def extract_entities(request, num):
    """
    Extract the entities of the last <int:num> news.
    """
    analyzed = []
    news = get_finance(num)
    for new in news:
        ent_list = []
        entities = nlp(dict(new)['title'])
        for ent in entities.ents:
            ent_list.append(ent.text)
        analyzed.append({'origin':new['origin'], 'title': new['title'], 'entities': ent_list})

    return json.dumps(analyzed)


@app.route('/api/get_b3')
def get_B3(request):
    """
    Get B3 info from https://br.advfn.com/bolsa-de-valores/bovespa and save into a csv file
    """
    runner = SpiderRunner()

    deferred = runner.crawl(b3.B3)
    deferred.addCallback(save_b3_csv)
    deferred.addCallback(return_spider_output)

    return deferred



if __name__ == "__main__":
    app.run("localhost", 8080)