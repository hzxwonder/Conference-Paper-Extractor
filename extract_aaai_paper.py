import requests
import json
from tqdm import tqdm
from lxml import etree
from lxml.etree import HTMLParser
from bs4 import BeautifulSoup
from lxml.etree import tostring
import os

def getHTMLText(url):
    kv = {'user_agent':'Mozilla/5.0'}
    # proxies_myself = {'http':'44.226.167.102:3128'}
    try:
        # r = requests.get(url,headers = kv,proxies = proxies_myself,timeout=120)
        error_try = 5
        for i in range(error_try):
            try:
                r = requests.get(url,headers = kv, timeout=120)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                return r.text
            except:
                print('Failed! Retrying... {}/{}'.format(i+1, error_try))
                continue
        return ''
    except:
        print('Failed! Please check the conference name, conference year and the keyword!')
        return ''
    
if __name__ == '__main__':
    name = 'aaai'
    conf_time_lst = [2023]
    for conf_time in conf_time_lst:
        keyword = None
        print("Looking for papers from conferences {} {}, keyword: {}".format(name, conf_time, keyword))
        if name == "neurips" or name == "nips":
            url = "https://dblp.org/db/conf/nips/neurips{}.html".format(conf_time)
        else:
            url = "https://dblp.org/db/conf/{}/{}{}.html".format(name,name,conf_time)
        print("Parsing URL: {}".format(url))
        htmltext = getHTMLText(url)

        try:
            parse_html = etree.HTML(htmltext,HTMLParser())
            parse_xpaths = parse_html.xpath('//li[@class="entry inproceedings"]')
        except:
            print('Failed! Please check the conference name ,conference year and the keyword!')
            exit(1)

        dics = []
        print("Number of papers(all fields): {}".format(len(parse_xpaths)))

        batch_size = 50
        for i in range(0, len(parse_xpaths), batch_size):
            parse_xpaths_batch = parse_xpaths[i:i+batch_size]
            for parse_xpath in tqdm(parse_xpaths_batch):
                # 获取文章链接
                html_txt = tostring(parse_xpath, pretty_print=True, encoding='utf-8', method='html').decode('utf-8')
                soup = BeautifulSoup(html_txt, 'html.parser')
                div_head = soup.find('div', {'class': 'head'})
                paper_url = div_head.find('a')['href']
                
                span_head = soup.find('span', {'class': 'title', 'itemprop': 'name'})
                title = span_head.text

                # 获取作者
                parse_html_str = etree.tostring(parse_xpath)
                parse_html1 = etree.HTML(parse_html_str,HTMLParser())
                parse_content = parse_html1.xpath('//cite//span[@itemprop="name"]')
                parse_content = [parse_content[idx].text for idx in range(len(parse_content))]
                try:
                    #获取摘要
                    abstract_html = getHTMLText(paper_url)
                    soup = BeautifulSoup(abstract_html, 'html.parser')
                    abstract_tag = soup.find('div', {'class': 'main_entry'})
                    abstract_text = abstract_tag.find('section', {'class': 'item abstract'}).text.strip().split('\t')[-1]
                    
                    paper_abstract = abstract_text

                    dic = {
                            "Title": title, 
                            "Authors": parse_content[:-1], 
                            'Conference': name, 
                            'Time': conf_time, 
                            "URL": paper_url,
                            'Abstract': paper_abstract
                            }
                    dics.append(dic)
                except:
                    dic = {
                            "Title": title, 
                            "Authors": parse_content[:-1], 
                            'Conference': name, 
                            'Time': conf_time, 
                            "URL": paper_url,
                            'Abstract': None
                            }
                    dics.append(dic)


            
            output_path = f'Paper_set/{name}-{conf_time}.json'
            # if os.path.exists(output_path):
            #     with open(output_path, "r") as f:
            #         data_list = json.load(f)
            #     titles = [dic['Title'] for dic in data_list]
            #     for i,data in enumerate(dics):
            #         if data["Title"] in titles:
            #             title_idx = titles.index(data["Title"])
            #             data_list[i].update(dics[title_idx])
            #             break
            #         else:
            #             data_list.append(data)
            # else:
            #     data_list = dics
            data_list = dics
            with open(output_path, "w") as f:
                json.dump(data_list, f, indent=4,)
            print("The number of Papers extracted: {}".format(len(data_list)))