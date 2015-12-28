#coding=utf-8
import xlrd
import xlwt

def parse_account(path=""):

	if path == "":
		return

	data = xlrd.open_workbook(path, formatting_info=True)

	table = data.sheets()[0]

	detail = []

	for i in range(1, table.nrows):
		row = table.row_values(i)
		if row[0] == "":
			for crange in table.merged_cells:
				rlo, rhi, clo, chi = crange
				if rlo < i < rhi and clo == 0:
					row[0] = table.cell_value(rlo, clo)
					break
		if row[2] == "":
			for crange in table.merged_cells:
				rlo, rhi, clo, chi = crange
				if rlo < i < rhi and clo == 2:
					row[2] = table.cell_value(rlo, clo)
					break
		detail.append(row)

	return detail


def get_header_style():
	header_style = xlwt.XFStyle()
	font = xlwt.Font()
	font.name = 'SimSun'
	font.bold = True
	font.colour_index = 0
	header_style.font = font

	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER
	alignment.vert = xlwt.Alignment.VERT_CENTER
	header_style.alignment = alignment

	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = 23
	header_style.pattern = pattern

	borders = xlwt.Borders()
	borders.left = xlwt.Borders.THIN
	borders.right = xlwt.Borders.THIN
	borders.top = xlwt.Borders.THIN
	borders.bottom = xlwt.Borders.THIN
	header_style.borders = borders
	return header_style


def get_footer_style():
	footer_style = xlwt.XFStyle()
	font = xlwt.Font()
	font.bold = True
	font.colour_index = 2
	font.height = 0x00CF
	footer_style.font = font

	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = 11
	footer_style.pattern = pattern

	borders = xlwt.Borders()
	borders.left = xlwt.Borders.THIN
	borders.right = xlwt.Borders.THIN
	borders.top = xlwt.Borders.THIN
	borders.bottom = xlwt.Borders.THIN
	footer_style.borders = borders
	return footer_style



def get_form_style():
	n_style = xlwt.XFStyle()
	font = xlwt.Font()
	font.name = 'SimSun'
	font.colour_index = 0
	n_style.font = font

	borders = xlwt.Borders()
	borders.left = xlwt.Borders.THIN
	borders.right = xlwt.Borders.THIN
	borders.top = xlwt.Borders.THIN
	borders.bottom = xlwt.Borders.THIN
	n_style.borders = borders

	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER
	alignment.vert = xlwt.Alignment.VERT_CENTER
	n_style.alignment = alignment
	return n_style


def get_normal_style():
	n_style = xlwt.easyxf('font:height 280;')

	borders = xlwt.Borders()
	borders.left = xlwt.Borders.THIN
	borders.right = xlwt.Borders.THIN
	borders.top = xlwt.Borders.THIN
	borders.bottom = xlwt.Borders.THIN
	n_style.borders = borders

	alignment = xlwt.Alignment()
	alignment.horz = xlwt.Alignment.HORZ_CENTER
	alignment.vert = xlwt.Alignment.VERT_CENTER
	n_style.alignment = alignment
	return n_style



path = 'e:/dataD/test/test (2).xls'
account_file_path = "e:/dataD/account.xls"
save_dir = "e:/dataD/test/"

workbook = xlrd.open_workbook(path)
sheet = workbook.sheet_by_index(0)


i = 0
j = 0
t = 0
start = 1
company = ""
name = ""
date_list = []


day = 0
for t in range(3, sheet.ncols):
	if sheet.cell_value(0, t) == u"合计（数量）":
		break
	date_list.append(sheet.cell_value(0, t))
	day += 1


detail = parse_account(account_file_path)
for i in range(1, sheet.nrows):
	if sheet.cell_value(i, 0) == u"总计（费用）":
		break
	if sheet.cell_value(i, 0) != "" and sheet.cell_value(i, 0) != u"合计":
		account = sheet.cell_value(i, 0)
		for row in detail:
			catch = 0
			if account.lower() == row[1] or account.upper() == row[1]:
				company = row[0]
				name = row[2]
				catch = 1
				break
		if catch != 1:
			print account+" has no detail"

		if company == "" and name != "":
			title = name
		elif name == "" and company != "":
			title = company
		elif company == "" and name == "":
			title = account
		else:
			title = company+"-"+name
		company = ""
		name = ""
		print title, account
		wbk = xlwt.Workbook(encoding='utf-8', style_compression=0)
		isheet1 = wbk.add_sheet(title, cell_overwrite_ok=True)
		isheet2 = wbk.add_sheet(title+u"(日)", cell_overwrite_ok=True)

		isheet1.write(1, 1, u"采集账号", get_normal_style())
		isheet1.write(1, 2, u"补贴金额（单位：/元）", get_normal_style())
		isheet1.write(1, 3, u"合计（单位：/元）", get_normal_style())
		start = 1
	for j in range(0, sheet.ncols):
		if sheet.cell_value(i, 0) == u"合计":
			isheet2.write(start, j, sheet.cell_value(i, j), get_footer_style())
		else:
			isheet2.write(start, j, sheet.cell_value(i, j), get_form_style())
	start += 1
	if sheet.cell_value(i, 0) == u"合计":
		sum = sheet.cell_value(i, day+4)

		isheet1.write(2, 0, title, get_normal_style())
		isheet1.write(2, 1, account, get_normal_style())
		isheet1.write(2, 2, sum, get_normal_style())
		isheet1.write(2, 3, sum, get_normal_style())
		isheet1.write_merge(0, 0, 0, 3, u"2015年11月份<"+title+u">采集补贴(共"+str(sum)+u"元)", get_normal_style())
		isheet1.col(0).width = 6000
		isheet1.col(1).width = 6000
		isheet1.col(2).width = 8000
		isheet1.col(3).width = 6000

		num = 0
		for i, col in enumerate(sheet.row_values(0)):
			isheet2.write(0, i, col, get_header_style())
		isheet2.col(0).width = 3600
		isheet2.col(2).width = 3800
		isheet2.write_merge(1, start-2, 0, 0, account, get_normal_style())

		wbk.save(save_dir+u"2015年11月份采集费用补贴（"+title+u"）.xls")



















