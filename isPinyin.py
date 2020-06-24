#!/usr/bin/env python
# encoding: utf-8

## check if the string from stdin CAN BE parsed into a pinyin word.
## eg. Mila -> Mi La;  Lua -> Lu A. 
## notice multiple solutions can exist: lie -> Lie OR Li E

from sys import stdin
import argparse
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--showSolution', action = 'store_true', help='show solutions.')
args = parser.parse_args()
showSolution = args.showSolution

## downloaded pinyin database and curated uniq pinyins.
pinyins = ["a","ai","an","ang","ao","ba","bai","ban","bang","bao","bei","ben","beng","bi","bian","biao","bie","bin","bing","bo","bu","ca","cai","can","cang","cao","ce","cen","ceng","cha","chai","chan","chang","chao","che","chen","cheng","chi","chong","chou","chu","chuai","chuan","chuang","chui","chun","chuo","ci","cong","cou","cu","cuan","cui","cun","cuo","da","dai","dan","dang","dao","de","dei","deng","di","dia","dian","diao","die","ding","diu","dong","dou","du","duan","dui","dun","duo","e","en","er","fa","fan","fang","fei","fen","feng","fo","fou","fu","ga","gai","gan","gang","gao","ge","gei","gen","geng","gong","gou","gu","gua","guai","guan","guang","gui","gun","guo","ha","hai","han","hang","hao","he","hei","hen","heng","hong","hou","hu","hua","huai","huan","huang","hui","hun","huo","ji","jia","jian","jiang","jiao","jie","jin","jing","jiong","jiu","ju","juan","jue","jun","jv","ka","kai","kan","kang","kao","ke","ken","keng","kong","kou","ku","kua","kuai","kuan","kuang","kui","kun","kuo","la","lai","lan","lang","lao","le","lei","leng","li","lia","lian","liang","liao","lie","lin","ling","liu","lo","long","lou","lu","luan","lue","lun","luo","lv","ma","mai","man","mang","mao","me","mei","men","meng","mi","mian","miao","mie","min","ming","miu","mo","mou","mu","na","nai","nan","nang","nao","ne","nei","nen","neng","ni","nian","niang","niao","nie","nin","ning","niu","nong","nu","nuan","nue","nuo","nv","o","ou","pa","pai","pan","pang","pao","pei","pen","peng","pi","pian","piao","pie","pin","ping","po","pou","pu","qi","qia","qian","qiang","qiao","qie","qin","qing","qiong","qiu","qu","quan","que","qun","ran","rang","rao","re","ren","reng","ri","rong","rou","ru","ruan","rui","run","ruo","sa","sai","san","sang","sao","se","sen","seng","sha","shai","shan","shang","shao","she","shen","sheng","shi","shou","shu","shua","shuai","shuan","shuang","shui","shun","shuo","si","song","sou","su","suan","sui","sun","suo","ta","tai","tan","tang","tao","te","teng","ti","tian","tiao","tie","ting","tong","tou","tu","tuan","tui","tun","tuo","wa","wai","wan","wang","wei","wen","weng","wo","wu","xi","xia","xian","xiang","xiao","xie","xin","xing","xiong","xiu","xu","xuan","xue","xun","ya","yan","yang","yao","ye","yi","yin","ying","yo","yong","you","yu","yuan","yue","yun","za","zai","zan","zang","zao","ze","zei","zen","zeng","zha","zhai","zhan","zhang","zhao","zhe","zhen","zheng","zhi","zhong","zhou","zhu","zhua","zhuai","zhuan","zhuang","zhui","zhun","zhuo","zi","zong","zou","zu","zuan","zui","zun","zuo"]

## from leetcode word break ##
## https://leetcode.com/problems/word-break-ii/discuss/44311/Python-easy-to-understand-solution ####
class Solution(object):
	def wordBreak(self, s, wordDict):
		return self.helper(s, wordDict, {})
		
	def helper(self, s, wordDict, memo):
		if s in memo: return memo[s]
		if not s: return []
		
		res = []
		for word in wordDict:
			if not s.startswith(word):
				continue
			if len(word) == len(s):
				res.append(word)
			else:
				resultOfTheRest = self.helper(s[len(word):], wordDict, memo)
				for item in resultOfTheRest:
					item = word + '-' + item
					res.append(item)
		memo[s] = res
		return res

## main ##
solution = Solution()
ls = stdin.readlines()
for l in ls:
	inStr = l.strip().lower()
	res = solution.wordBreak(inStr, pinyins)
	hasRes = 1 if res else 0
	if showSolution:
		resString = ",".join(_ for _ in res)
		toPrint = "{}\t{}\t{}".format(inStr, hasRes, resString)
	else:
		toPrint = "{}\t{}".format(inStr, hasRes)
	print(toPrint)

