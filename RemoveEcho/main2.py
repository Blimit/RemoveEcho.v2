
import re
import jieba
import jieba.analyse
import sys

fr1 = "D:\orig.txt"
fr2 = "D:\orig_0.8_del.txt"
class simhash:
    def __init__(self,fl1,fl2):
        self.haiming = self.haiming(fl1,fl2)
        self.siminarity = self.siminarity(fl1,fl2)

    def getfile(self,file):
        txt1 = ''
        dictXL = {}
        linehub = 0
        with open(file, 'r', encoding="utf-8") as origin_file:
            for line in origin_file.readlines():
                linehub = linehub + 1
                if linehub % 2 != 0:
                    punctuation = '、，。!;:?"\''
                    text = re.sub(r'[{}]+'.format(punctuation), '', line)
                    txt1 = txt1 + text.strip()
                else:
                    continue

        jieba.analyse.set_stop_words('./stopwords.txt')
        size = 20
        for feature, weight in jieba.analyse.extract_tags(txt1, topK=size, withWeight=True):
            dictXL[feature] = weight
            # print (dictXL[feature])
        return dictXL,size

    def string_hash(self,source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            #print(source,x)
            return str(x)

    def simhashalgo(self,file):
        dictXL = {}
        dictXL,size = self.getfile(file)
        database = []
        length = 0
        for key,weight in dictXL.items():
            data = []
            weight = int(weight*100)
            #print(key)
            keyhash = self.string_hash(key)
            for i in keyhash:
                length +=1
                if i =='1':
                    data.append(weight)
                else :
                    data.append(-weight)
            database.append((data))

        list1 = [x*0 for x in range(64) ]
        for i in range(64):
            for j in range(size):
                list1[i] += database[j][i]
        hashlist = []
        for i in list1:
            if i>=0:
                hashlist.append('1')
            else:
                hashlist.append('0')
        #print(list1)
        #print(hashlist)
        return hashlist

    def haiming(self,file1,file2):
        F1 = self.simhashalgo(file1)
        F2 = self.simhashalgo(file2)
        haimingdistance = 0
        for i in range(64):
            if F1[i] ==F2[i]:
                continue
            else :
                haimingdistance +=1
        return haimingdistance

    def siminarity(self,file1,file2):
        a = ''
        b = ''
        F1 = self.simhashalgo(file1)
        F2 = self.simhashalgo(file2)
        a = int(a.join(F1),2)
        b = int(b.join(F2),2)
        print(a)
        print(b)
        if(a > b):
            return float(b/a)
        else:
            return float(a/b)
def main():
    '''
    try:
        fr1,fr2,savepath = sys.argv[1:4]
    except Exception as e:
        print("文件列表获取失败")
    with open(savepath,'w',encoding='utf-8') as save:
        save.write("两文件的海明距离为：%d \n" %project.haiming)
        save.write("两文件的相似度为：%f" %project.siminarity)
    '''


    project = simhash(fr1,fr2)
    print(project.siminarity)

if __name__ == "__main__":
    main()

