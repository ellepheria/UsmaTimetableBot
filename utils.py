import pandas as pd
import constants

file_name = './timetables/timetable.xlsx'


def get_data_from_excel(filename):
    df = pd.read_excel(filename)

    grouped_data = df.groupby(['group', 'data'])

    result_dict = {}
    for (group, date), group_data in grouped_data:
        if group not in result_dict:
            result_dict[group] = [
                {
                    date: group_data.to_dict('records')
                }
            ]
        else:
            result_dict[group].append({
                date: group_data.to_dict('records')
            })

    return result_dict


def get_timetable(group, date):
    pass
