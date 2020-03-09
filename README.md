App que expõe endpoints para minerar notícias sobre ações da B3.

---

Instruções de instalação:

- Crie um ambiente virtual em python 3
  `virtualenv -p python3 _vv`

- Ative o ambiente:
  `source _vv/bin/activate`

- Entre na pasta do financescrape:
  `cd financescrape`

- Instale os requerimentos:
  `pip install -r requirements.txt`

- Instale o modelo para o Spacy:
  `python -m spacy download pt_core_news_sm`

- Rode o app:
  `python app.py`

O app vai rodar em localhost:8080.

Existem três endpoints disṕoníveis:

- /api/mine_save \
  Comando via terminal: `curl -X GET localhost:8080/api/mine_save`\
  Ao acessar esse endpoint o feed de notícias dos sites ultimoinstante e financenews é minerado tendo em vista ações da B3 e gera um arquivo que é salvo com o nome finance.jsonl na pasta files.

- /api/extract_entities/<int:num> \
  Comando via terminal: `curl -X GET localhost:8080/api/extract_entities/5` \
  Esse endpoint retorna as últimas <int:num> notícias minerada,s juntamente entidades reconhecidas no título da notícia pelo Spacy.

- /get_b3 \
  Comando via terminal: `curl -X GET localhost:8080/get_b3`
  Esse endpoint faz o download das ações da B3 e salva em no arquivo b3.csv, que é usado para fazer os filtros das notícias dos endpoints anteriores.

---

Observações:

- Ao minerar e salvar as notícias elas são incluídas no topo do arquivo finance.jsonl, sem apagar as anteriores.
- Ao extrair as notícias as mesmas são lidas a partir do topo do arquivo.

- Para rodar os testes, deve-se executar fora da pasta testes:
  `python -m unittest tests/test_spider.py`
