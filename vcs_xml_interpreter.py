from xml.dom.minidom import parse

def get_line_report(file):
	dom = parse(file)
	data = dom.documentElement

	stus = data.getElementsByTagName('linebb')
	line_list = []

	for stu in stus:
		 st_id = stu.getAttribute('id')
		 st_file_id = stu.getAttribute('file_id')
		 st_line_num = stu.getAttribute('line_num')
		 st_line_ignore = stu.getAttribute('line_ignore')
		 line_list.append([st_id, st_file_id, st_line_num, st_line_ignore])
		 

	files = data.getElementsByTagName('linedef')
	file_list = []

	for file in files:
		file_id = file.getAttribute('id')
		file_list.append(file_id)

	return file_list, line_list


def Integrate_file_line(file_list, line_list):
	dic = {}

	lists = [[] for i in range(len(file_list))]

	file_list_index = -1

	for i in range(len(line_list)):
		if i == len(line_list) - 1:
			break
		elif line_list[i][0] == '0':
			file_list_index += 1

		lists[file_list_index].append(line_list[i])

	for i in zip(file_list, lists):
		dic[i[0]] = i[1]

	return dic		
		

def get_file_name(file):
	dom = parse(file)
	data = dom.documentElement

	stus = data.getElementsByTagName('srcdef')

	out = []
	for stu in stus:
		stu_id = stu.getAttribute('id')
		stu_name = stu.getAttribute('name')
		out.append([stu_id, stu_name])
	return out

def Integrate_file_name(report_dic, file_names):
	for name in file_names:
		report_dic[name[1]] = report_dic.pop(name[0])
	return report_dic



def get_inactive_code(file):
	dom = parse(file)
	data = dom.documentElement

	stus = data.getElementsByTagName('instance_data')

	out = []
	for stu in stus:
		stu_name = stu.getAttribute('name')
		stu_value = stu.getAttribute('value')
		out.append([stu_name, stu_value])
	return out


def Integrate_inactive_line(dic, inactive_line):
	for i in range(len(inactive_line)):
		name = inactive_line[i][0]
		cover_line = inactive_line[i][1]

		for key in dic.keys():
			if name not in dic.keys():
				for i in range(len(dic[key])):
					dic[key][i].append(cover_line[i])
			else:
				for i in range(len(dic[name])):
					dic[name][i].append(cover_line[i])
	return dic


def main():
	file_report, line_report = get_line_report('db/shape/line.verilog.shape.xml')
	report_dic = Integrate_file_line(file_report, line_report)

	file_names = get_file_name("db/design/verilog.design.xml")
	# {file: line}
	dic = Integrate_file_name(report_dic, file_names)
	inactive_line = get_inactive_code("db/testdata/test/line.verilog.data.xml")

	new_dic = Integrate_inactive_line(dic, inactive_line)


	print(new_dic)
	
	for	key in new_dic:
		print(key)
		for i in new_dic[key]:

			print(i[2], i[4])
		print("         ")


main()









