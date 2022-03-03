from argparse import Namespace
import re
from unicodedata import name
from pypinyin import pinyin, lazy_pinyin, Style
from pypinyin.contrib.tone_convert import to_normal, to_tone, to_initials, to_finals
from Pinyin2Hanzi import DefaultHmmParams
from Pinyin2Hanzi import viterbi
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag
dagparams = DefaultDagParams()
import itertools as it


names=input("请输入队员名称(用空格分隔):\n")

names = names.split(" ")
pinyinarr = []
for name in names:
    tmp = [to_normal(pinyin(i)[0][0]) for i in name]
    pinyinarr.append(tmp)
    print(name,"->",pinyinarr[len(pinyinarr)-1])



totalResult = []
hmmparams = DefaultHmmParams()
dagparams = DefaultDagParams()
for e in it.product(*pinyinarr):
    result = viterbi(hmm_params=hmmparams, observations=e, path_num = 2)
    for item in result:
        totalResult.append(item) 
    result = dag(dagparams,e,path_num = 2)
    for item in result:
        totalResult.append(item) 
    result = viterbi(hmm_params=hmmparams, observations=e[::-1], path_num = 2)
    for item in result:
        totalResult.append(item) 
    result = dag(dagparams,e[::-1],path_num = 2)
    for item in result:
        totalResult.append(item) 


totalResult.sort(reverse=True)

already = set()

for item in totalResult:
    res = ""
    for i in item.path:
        res+=i
    if res in already:
        continue
    already.add(res) # deduplication
    print(format(item.score,'.2f'), res)

