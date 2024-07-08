import pandas as pd


# source: https://github.com/godlytalias/Bible-Database/tree/master
class BibleParser:
    # {"chapter": Int, "verse":Int?, "text":String?}
    def __init__(self, version, book):
        self.__data = None
        if version == "kjv":
            self.__kjv(book)
        elif version == "hindi":
            self.__hindi(book)

    def get_data(self):
        return self.__data

    def __kjv(self, book):
        self.__data = self.__parse(pd.read_json("data/en_kjv.json"), book)

    def __hindi(self, book):
        self.__data = self.__parse(pd.read_json("data/hi.json"), book)

    @staticmethod
    def __parse(data, book):
        # 추가할 성경 인덱스 추가하기
        if book == "Matthew":
            key = 39
        elif book == "Mark":
            key = 40
        elif book == "Luke":
            key = 41
        elif book == "John":
            key = 42
        else:
            key = 0

        result = []
        book = data.iloc[key]['Book']['Chapter']
        for i in range(len(book)):
            chapter = book[i]['Verse']
            for j in range(len(chapter)):
                verse = chapter[j]['Verse']
                result.append({'chapter': i + 1, 'verse': j + 1, 'text': verse})

        return pd.DataFrame(result)
