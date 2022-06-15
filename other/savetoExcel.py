import openpyxl
from list_of_actions import times, teams
import datas
test_data = {'1 half': {'1': {'ЖК': 1,
                  'КК': 1,
                  'Обводка✅': 2,
                  'Обводка❌': 3,
                  'Угловые': 0,
                  'Фолы': 0,
                  'передача✅': 0,
                  'передача❌': 0,
                  'удар✅': 0,
                  'удар❌': 0},
            '2': {'ЖК': 0,
                  'КК': 0,
                  'Обводка✅': 0,
                  'Обводка❌': 0,
                  'Угловые': 0,
                  'Фолы': 0,
                  'передача✅': 0,
                  'передача❌': 1,
                  'удар✅': 0,
                  'удар❌': 0}},
 '2 half': {'1': {'ЖК': 0,
                  'КК': 0,
                  'Обводка✅': 0,
                  'Обводка❌': 0,
                  'Угловые': 0,
                  'Фолы': 0,
                  'передача✅': 1,
                  'передача❌': 0,
                  'удар✅': 0,
                  'удар❌': 1},
            '2': {'ЖК': 0,
                  'КК': 0,
                  'Обводка✅': 0,
                  'Обводка❌': 0,
                  'Угловые': 1,
                  'Фолы': 0,
                  'передача✅': 0,
                  'передача❌': 0,
                  'удар✅': 0,
                  'удар❌': 0}}}


def transfer_to_approriate_type(ws: openpyxl.Workbook.active,final_data: dict):
    row = 3
    col = 2
    for half in final_data:
        for team in final_data[half]:
            row = 3

            for action in final_data[half][team]:
                ws.cell(row=row, column=col, value=final_data[half][team][action])
                row+=1
            col += 1


# def finalResults(results: dict[str]):
#     final_result = {}
#
#     for half in results:
#         final_result[half] = {}
#         for team in results[half]:
#             final_result[half][team] = {}
#             for action in results[half][team]:
#                 if not action.endswith("❌"):
#                     final_result[half][team][action] = results[half][team][action]
#                 elif action.endswith("❌"):
#                     tmpvalue = action.replace("❌", '✅')
#                     final_result[half][team][action.replace("❌","_всего")] = results[half][team][action] + results[half][team][tmpvalue]
#
#     return final_result








def create_template_of_excel():
    wb = openpyxl.Workbook()
    ws = wb.active
    _fill_halfs(ws,times)
    _fill_teams(ws,teams)
    _fill_actions(ws, datas.ACTIONS_FOR_EXCEL)
    transfer_to_approriate_type(ws, test_data)
    wb.save('test1.xls')
    wb.close()


def _fill_halfs(ws: openpyxl.Workbook.active ,halfs):
    col = 1
    for i in times:
        ws.cell(row=1, column=col, value=i)
        col +=3

def _fill_teams(ws: openpyxl.Workbook.active, teams):
    col = 2
    for team in teams:
        ws.cell(row=2, column=col, value=team)
        ws.cell(row=2, column=col + 2, value=team)
        col+=1

def _fill_actions(ws: openpyxl.Workbook.active, actions):
    row = 3
    for action in actions:
        ws.cell(row=row, column=1, value=action)
        row +=1

x = create_template_of_excel()