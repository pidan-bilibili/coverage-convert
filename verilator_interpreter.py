import re


def Integrate_dic(dic):
	for key in dic.keys():
		for e in dic[key]:
			if "-" in e:
				dic[key].remove(e)
				new_e = e.split('-', 1)
				num_a = int(new_e[0])
				num_b = int(new_e[1])
				for i in range(num_a, num_b+1):
					dic[key].append(str(i))
	return dic


def get_cover_info(info):
	dic = {}
	for e in info:
		if (e[10] == 'S'):
			if e[1] not in dic.keys():
				dic[e[1]] = [e[11]]
			else:
				dic[e[1]].append(e[11])
	return dic


def get_info(file):
	lines = file.readlines()
	output = []
	for line in lines: 
		line = repr(line)
		line_list = get_line_info(line)
		output.append(line_list)
	return output[1:]


def get_line_info(line):
	text_1 = r"\x01"
	text_2 = r"\x02"

	string = ""
	output = []
	count = 0
	for i in range(len(line)):
		string += line[i]
		if (count % 2 == 0):
			if string[-4:] == text_1:
				string = ""
			if string[-4:] == text_2:
				output.append(string[:-4])
				string = ""
				count += 1
		else:
			if string[-4:] == text_2:
				string = ""
			if string[-4:] == text_1:
				output.append(string[:-4])
				string = ""
				count += 1
	return output




def main():
	file = open("vlt_coverage.dat")
	info = get_info(file)
	dic = get_cover_info(info)
	dic = Integrate_dic(dic)
	print(dic)

main()









