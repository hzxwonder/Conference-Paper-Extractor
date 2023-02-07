import requests

import csv
from tqdm import tqdm
from lxml import etree
from lxml.etree import HTMLParser
import argparse
import os


def getHTMLText(url):
    kv = {'user_agent':'Mozilla/5.0'}
    proxies_myself = {'http':'105.27.238.167:80'}
    try:
        r = requests.get(url,headers = kv,proxies = proxies_myself,timeout=120)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('Failed! Please check the conference name, conference year and the keyword!')
        return ''

def writeToCsv(args,dicts):
    if not args.save_dir:
        args.save_dir = '.'
    else:
        if not os.path.exists(args.save_dir):
            os.mkdir(args.save_dir)

    if args.keyword:
        file_path = os.path.join(args.save_dir,"{}_{}_{}.csv".format(args.name,args.time,args.keyword))
    else:
        file_path = os.path.join(args.save_dir,"{}_{}.csv".format(args.name,args.time))

    with open(file_path,'w',encoding='utf-8',newline='') as f:
        csv_write = csv.writer(f)
        csv_head = ["Title","Authors"]
        csv_write.writerow(csv_head)
        for ele in dicts:
            csv_write.writerow([ele['title'],"\n".join(ele['authors'])])

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Conference Information")
    parser.add_argument('-n',"--name", type=str, required=True,help="Name of Conference you want to search.")
    parser.add_argument('-t',"--time", type=int, default=2022, help="Year of Conference you want to search.")
    parser.add_argument("--save_dir", type=str, default=None, help="the file directory which you want to save to.")
    parser.add_argument('-k',"--keyword", type=str, default=None, help="the keyword filter, if None, save all the paper found.")
    args = parser.parse_args()

    args.name = args.name.lower()
    print("Looking for papers from conferences {} {}, keyword: {}".format(args.name,args.time,args.keyword))
    if args.name == "neurips" or args.name == "nips":
        url = "https://dblp.org/db/conf/nips/neurips{}.html".format(args.time)
    else:
        url = "https://dblp.org/db/conf/{}/{}{}.html".format(args.name,args.name,args.time)
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
    for parse_xpath in tqdm(parse_xpaths):
        parse_html_str = etree.tostring(parse_xpath)
        parse_html1 = etree.HTML(parse_html_str,HTMLParser())
        parse_content = parse_html1.xpath('//cite//span[@itemprop="name"]')
        parse_content = [parse_content[idx].text for idx in range(len(parse_content))]
        try:
            if args.keyword:
                paper_title = parse_content[-1].upper()
                keyword = args.keyword.upper()
                if paper_title.find(keyword) == -1:
                    # print(parse_content[-1])
                    continue
                else:
                    dic = {"title": parse_content[-1], "authors": parse_content[:-1]}
                    dics.append(dic)
            else:
                dic = {"title": parse_content[-1], "authors": parse_content[:-1]}
                dics.append(dic)
        except:
            continue

    writeToCsv(args,dics)
    print("The number of Papers extracted: {}".format(len(dics)))


