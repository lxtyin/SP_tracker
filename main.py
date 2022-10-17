
from lib2to3.pgen2.literals import simple_escapes
import re
from bs4 import BeautifulSoup
from numpy import single
import difflib


def string_similar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

page = ""
with open('info.html', encoding='utf-8', mode = 'r') as f:
	page = f.read()

# 解析题库
bank = []
with open('题库.txt', encoding='utf-8', mode = 'r') as f:
	for info in re.split('\d+\.', f.read()):
		tmp = re.split("正确答案[：:]+", info)
		if len(tmp) < 2: continue
		res = {
			'tag': '',
			'info': tmp[0],
			'ans': []
		}

		if re.search('填空题', info):
			res['tag'] = '填空'
			res['ans'].append(tmp[1])
		else:
			res['tag'] = '选择'
			opt = re.split('[A-Z]\.|我的答案', res['info'])
			res['info'] = opt[0]
			

			for c in re.findall('[A-Z]', tmp[1]):
				idx = ord(c) - ord('A') + 1
				if idx < len(opt): res['ans'].append(opt[idx])
				
		std_res = []
		for i in res['ans']:
			std_res.append(i.strip('\n& '))
		res['ans'] = std_res
		bank.append(res)

# for i in bank:
# 	print(i['tag'])
# 	print(i['info'])
# 	print(i['ans'])
# exit()

soup = BeautifulSoup(page, 'html.parser')

single_ls = soup.find_all(id = re.compile('sigleQuestionDiv_.'))

res_f = open('res.txt', 'w')

for div in single_ls:
	info = div.h3.div.string # 题目内容
	ques = {} #找到最匹配的题目
	mx_match = 0
	for q in bank:
		rate = string_similar(info, q['info'])
		if rate > mx_match:
			mx_match = rate
			ques = q

	res_f.write(info + "\nAnswer: \n")

	if ques['tag'] == '填空':
		res_f.write(ques['ans'][0])
	else:
		option = div.form.div.find_all('div')
		for idx in option: # 枚举选项
			if not idx.div: continue
			content = idx.div.text # 选项内容
			for i in ques['ans']:
				if string_similar(i, content) > 0.8: # 相似度
					res_f.write(idx.span.text + ' ' + content + ' ')
					res_f.write(str(string_similar(i, content))) #答案
					res_f.write('\n')
					break
	res_f.write("\n--------\n")
res_f.close()
