#from django.test import TestCase

# Create your tests here.
import jieba

word = '我觉得我这辈子就没有爱过一个人'


jieba_list = jieba.lcut(word,cut_all=True)

#print(jieba_list)

def jieba_analyse(jieba_list):
    result = []
    if len(jieba_list) == 1:
        result.append(jieba_list[0])
    else:
        for elment in jieba_list[1:]:
            if len(elment) >= 2:
                result.append(jieba_list[0]+elment)


        jieba_list.pop(0)
        jieba_analyse(jieba_list)

    return result

print(jieba_analyse(jieba_list))







