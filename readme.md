# Computer Science Conference Paper Extractor Script

This is a python script to extract conference paper from dblp : https://dblp.org/db/conf/index.html

## Requirements

```text
lxml==4.9.2
requests==2.25.1
tqdm==4.62.3
```

## Steps

### First Step : Install Dependency

```shell
pip install -r requirements.txt
```

### Second Step : Run main.py

```python
python main.py --name cvpr --time 2019 --keyword reinforcement,RL,DRL
```

* "-n" or "--name" Name of Conference you want to search, it is required. You must check whether the name is right or it will throw a exception after 2 minutes.
* "-t" or --time" Year of Conference you want to search. If not specified, it will fill the year of "2022".
* "-k" or "--keyword" means the keyword you want to filter the results founded. If not specified, it will output all the paper accepted. You don't need to pay attention to the case of keywords, because the code already has uniform case. It can support multi-keyword search and take the union of results. Use "," to split the keywords.
* "--save_dir" means the file directory which you want to save to.

And if all the processes are correct, it will output a .csv file containing the titles and authors of all (keyword) papers.

If you have any questions, you can submit your issue. I will tackle it as soon as possible!