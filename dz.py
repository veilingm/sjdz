import re
import urllib
import urllib.request
import operator

from bs4 import BeautifulSoup
from xpinyin import Pinyin


class MyDict:
    def __init__(self, word, pinyin, pinyinWithoutYB, explain):
        self.word = word
        self.pinyin = pinyin
        self.pinyinWithoutYB = pinyinWithoutYB
        self.explain = explain

    pass


url = "https://hanyu.baidu.com/s"


def searchDict(char):
    word = urllib.parse.urlencode({"wd": char})
    newUrl = url + "?" + word + "&ptype=zici&tn=sug_click"
    request = urllib.request.urlopen(newUrl).read()
    response = request.decode('UTF-8')
    soup = BeautifulSoup(response, 'lxml')
    res = ""
    try:
        res = soup.find('div', id='basicmean-wrapper').find('dd').get_text().strip().replace("\n", "<br/>")
    except:
        res = "未能查找到"
    finally:
        return res


def handle():
    p = Pinyin()
    resArray = []
    tmpArray = []
    with open("诗经.txt", "r", encoding='utf8') as f:
        i = 0
        allLine = f.readlines()
        countLine = len(allLine)
        for line in allLine:
            line = line.strip('\n')
            if len(line) > 0:
                prefixChar = ''
                for curChar in list(line):
                    if re.match("[\u4E00-\u9FA5]", curChar):
                        if prefixChar == curChar:
                            if curChar not in tmpArray:
                                tmpArray.append(curChar)
                                resArray.append(MyDict(prefixChar + curChar,
                                                       p.get_pinyin(prefixChar, tone_marks='marks'),
                                                       p.get_pinyin(prefixChar),
                                                       searchDict(curChar)))
                        prefixChar = curChar
            i = i + 1
            print(str(round(i / countLine * 100, 2)) + "%")
    sortKey = operator.attrgetter("pinyinWithoutYB")
    resArray.sort(key=sortKey)

    with open("诗经叠字提取结果.md", "w", encoding='utf8') as f:
        f.write("| 序号 | 字 | 拼音 | 解释 |" + "\n")
        f.write("| ---- | ---- | ---- | ---- |" + "\n")
        i = 1
        for res in resArray:
            f.write("| " + str(i) + " | " + res.word + " | " + res.pinyin + " | " + res.explain + " |\n")
            i = i + 1


handle()
