

def transfer_results(results: dict):
    passession_common = results['1']['передача✅'] + results['2']['передача✅']
    tmp = {}
    for teams in results:
        team = results[teams]
        shoots_all = sum([team[i] for i in team if i.startswith('удар')])
        try:
            percent_shoots = team['удар✅'] / shoots_all * 100
        except ZeroDivisionError:
            percent_shoots = 0
        pass_all = sum([team[i] for i in team if i.startswith('передача')])
        try:
            percent_pass = team['передача✅'] / pass_all * 100
        except ZeroDivisionError:
            percent_pass = 0
        obvodka_all = sum([team[i] for i in team if i.startswith('Обводка')])
        ball_posession = team['передача✅'] / passession_common * 100
        tmp[teams] = {"Удары всего": shoots_all,
                      "Удары точные": team['удар✅'],
                      "Процент точных ударов": percent_shoots,
                      "Передачи всего": pass_all,
                      "Передачи точные": team['передача✅'],
                      "Процент точных передач": percent_pass,
                      "Владение мячом": ball_posession,
                      "Обводка всего": obvodka_all,
                      "Обводка точные": team['Обводка✅'],
                      "Сейвы": team['Сейвы'],
                      "Фолы": team['Фолы'],
                      "ЖК": team['ЖК'],
                      "КК": team['КК'],
                      "Угловые": team['Угловые']
                      }

    return tmp