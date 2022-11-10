from xml.dom.minidom import parse

def get_line_report(file):
	dom = parse(file)
	data = dom.documentElement

	stus = data.getElementsByTagName('linestmt')
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

	stus = data.getElementsByTagName('inactiveCodes')

	out = []
	for stu in stus:
		stu_fid = stu.getAttribute('fid')
		stu_lineno = stu.getAttribute('lineno')
		out.append([stu_fid, stu_lineno])
	return out


def main():
	file_report, line_report = get_line_report('db/shape/line.verilog.shape.xml')
	report_dic = Integrate_file_line(file_report, line_report)

	file_names = get_file_name("db/design/verilog.design.xml")
	# {file: line}
	dic = Integrate_file_name(report_dic, file_names)
	inactive_line = get_inactive_code("db/auxiliary/dve_debug.xml")
	for	key in dic:
		print(key)
		for i in dic[key]:
			print(i[2])
		print("         ")
	print("         ")
	print("inactive_line: ", inactive_line)





main()









