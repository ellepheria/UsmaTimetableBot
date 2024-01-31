import pandas as pd
import constants

file_name = './timetables/timetable.xlsx'


def get_data_from_excel(filename):
    df = pd.read_excel(filename)

    grouped_data = df.groupby(['group', 'data'])

    result_dict = {}
    for (group, date), group_data in grouped_data:
        if group not in result_dict:
            result_dict[group] = {
                date: group_data.to_dict('records')
            }
        else:
            result_dict[group] = {
                **result_dict[group],
                date: group_data.to_dict('records')
            }

    return result_dict


def get_timetable(group, date):
    timetables = get_data_from_excel(file_name)

    if date == 7:
        return None
    return timetables[group][date]


def generate_message(name, timetable: list):
    if not len(timetable):
        return 'В этот день занятий нет.'
    message = f"""
Привет, {name}!
Вот расписание для {timetable[0]['group']} на {constants.DATE_TO_DAY[timetable[0]['data']]}:
    """

    for subject in timetable:
        message += f"""
НП:  {subject['subject']}
ВР:  {subject['time']}
АДРЕС:  {subject['address']}
КАФ:  {subject['department']}
ССЫЛКА:  {subject['link']}
ПОДГРУППА:  {str(subject['subgroup']) + ('-я неделя' if subject['subgroup'] != '-' else '')}
        """

    return message
