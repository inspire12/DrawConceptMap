#-*- coding: utf-8 -*-
import urlopen
from bs4 import BeautifulSoup
import html

class ExtractConcept:
    def __init__(self):
        self.result = []

    def Test(self, num):
        self.result.append(num)
        return self.result

    def cleaninput(input):
        import re
        import string
        input = re.sub('\n+', " ", input)
        input = re.sub('\[[0-9]*\]', "", input)
        input = re.sub(' +', " ", input)
        input = bytes(input, "UTF-8")
        input = input.decode("ascii", "ignore")
        cleanInput = []
        input = input.split(' ')
        for item in input:
            item = item.strip(string.punctuation)
            if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
                cleanInput.append(item)
        return cleanInput

    def Extract_subcript(self, video_id):

        url = "http://video.google.com/timedtext?lang=en&v=" + video_id
        html_page = urlopen(url)
        bs_obj = BeautifulSoup(html_page, "html.parser")
        lines = bs_obj.transcript.find_all("text")  # BeautifulSoup으로 자막 태그 전부 lines에 저장
        captions = [""]  # 한줄한줄씩 저장할 리스트
        caption = ""  # 자막 전부를 저장할 문자열
        for line in lines:
            one_line = html.unescape(line.get_text())
            # 필요한 경우 전부 소문자로 바꿈
            # one_line = html.unescape(line.get_text()).lower()
            one_line = one_line.replace("\n", " ")
            one_line = one_line.split(" ")
            print(one_line)
            captions += one_line
        return captions

    def Extract_Concept_1(self, captions):

        from sklearn.feature_extraction.text import CountVectorizer
        from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
        from sklearn.decomposition import LatentDirichletAllocation
        import numpy as np
        import nltk

        nltk.download("punkt")
        # 1~3-gram의 bow를 만드는 코드
        vect = CountVectorizer(ngram_range=(1, 3), stop_words="english",max_df=.15)
        vect.vocabulary_
        # vect = CountVectorizer(ngram_range=(1,3), max_features=10000, max_df=.15)
        X = vect.fit_transform(captions)
        feature_names = np.array(vect.get_feature_names())
        print(feature_names)  # 여기서 출력된 부분들 중에서 임의로 토픽인것 뽑아씀

        return feature_names
