from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from config import datas

wb = load_workbook("Персональная статистика 2.0 - 4.xlsx")
r = wb.sheetnames
print(r[:2])
ws4 = wb.active
col_title = 4
row_title = 11
ws4.cell(row= row_title, column=col_title, value=12)
# wb = Workbook()
# ws = wb.active
# ws.title = "Hello"
#
# for row in range(1, 40):
#     ws.append(range(600))
#
# ws4 = wb.create_sheet(title="test")
#
# col_title = 1
# row_title = 1
#
# for halfs in datas:
#     ws4.cell(row_title, col_title, value=halfs)
#     for zones in datas[halfs]:
#         row_title += 1
#         ws4.cell(row= row_title, column=col_title, value= zones)
#         for action in datas[halfs][zones]:
#             row_title += 1
#             ws4.cell(row= row_title, column=col_title + 1, value=action)
#             ws4.cell(row= row_title, column=col_title + 2, value=datas[halfs][zones][action])
#     row_title = 1
#     col_title = 4
#
#
#
#
# # d = ws.cell(5,3,7)
wb.save('testing12.xls')
wb.close()

