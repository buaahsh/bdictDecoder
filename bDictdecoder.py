# -*- coding:utf-8 -*-


import binascii


class BaiduPinyinBDict():
    def __init__(self):
        self.fenmu = ["c", "d", "b", "f", "g", "h", "ch", "j", "k", "l", "m", "n", "", "p", "q", "r", "s", "t", "sh",
                      "zh", "w", "x", "y", "z"]
        self.yunmu = [ "uang", "iang", "ong", "ang", "eng", "ian", "iao", "ing", "ong", "uai", "uan", "ai", "an", "ao",
                       "ei","en", "er", "ua", "ie", "in", "iu", "ou", "ia", "ue", "ui", "un", "uo", "a", "e", "i", "a", "u", "v"]
        pass

    def hexToWord(self, hexStr):
        wordList = []
        for i in range(0, len(hexStr), 4):
            word = (chr(int(hexStr[i:i+2], 16)) + chr(int(hexStr[i+2:i+4], 16))).decode('utf-16')
            if u'\u4e00' <= word <= u'\u9fa5':
                word = word.encode("utf-8")
                wordList.append(word)
            else:
                wordList = []
                break
        return wordList

    def hexToPinyin(self, hexString):
        pinyinList = []
        for i in range(0, len(hexString), 4):
            fenmu = self.fenmu[int(hexString[i:i+2], 16)]
            yunmu = self.yunmu[int(hexString[i+2:i+4], 16)]
            pinyinList.append(fenmu+yunmu)
        return pinyinList

    def convert2txtByContent(self, content):
        resultList = []
        hexData = binascii.hexlify(content)
        hexData = hexData[1696:]
        word = ""
        #过滤前面信息
        while True:
            wordCount = hexData[0:2]
            wordCount = int(wordCount, 16)
            word = hexData[8+wordCount*4:8+wordCount*8]
            word = self.hexToWord(word)
            if len(word) < 1:
                break
            pinyin = hexData[8:8+wordCount*4]
            pinyin = self.hexToPinyin(pinyin)
            word = "".join(word)
            pinyin = " ".join(pinyin)
            resultList.append(word+"\t"+pinyin)
            hexData = hexData[8+wordCount*8:]
            if len(hexData) < 1:
                break
        return resultList

    def convert2txt(self, fileName):
        wordList = []
        fileText = open(fileName, "rb")
        with fileText as f:
            content = f.read()
        wordList = self.convert2txtByContent(content)
        return wordList

if __name__ == "__main__":
    baiduPinyinBDict = BaiduPinyinBDict()
    words = baiduPinyinBDict.convert2txt("87.bdict")
    for item in words:
        print item

