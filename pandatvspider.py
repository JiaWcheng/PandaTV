# coding:utf-8
import re
from urllib import request


class Spider():
    url = 'https://www.panda.tv/cate/lol'
    root_partten = '<div class="video-info">([\s\S]*?)</div>'
    name_partten = '</i>([\s\S]*?)</span>'
    number_partten = '<span class="video-number">([\s\S]*?)</span>'

    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        htmls = r.read()
        htmls = str(htmls, encoding='utf-8')
        return htmls

    def __analysis(self, htmls):
        root_html = re.findall(Spider.root_partten, htmls)
        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_partten, html)
            number = re.findall(Spider.number_partten, html)
            anchor = {'name': name, 'number': number}
            anchors.append(anchor)
        return anchors

    def __refine(self, anchors):
        l = lambda anchor: {
            'name': anchor['name'][0].strip(),
            'number': anchor['number'][0]
        }
        return map(l, anchors)

    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors

    def __sort_seed(self, anchor):
        r = re.findall('\d*', anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number

    def __show(self, anchors):
        for rank in range(0, len(anchors)):
            print('rank ' + str(rank + 1)
                  + ':' + anchors[rank]['name']
                  + ':' + anchors[rank]['number']
                  )

    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)


pandaspider = Spider()
pandaspider.go()
