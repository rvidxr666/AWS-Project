import csv
import pandas as pd


# needed_attributes = ['naics_code', 'case_status','job_title' ]

def find_index(csv_read_obj):
    indexes_of_attributes = {}
    for row in csv_read_obj:
        # row = [word.lower() for word in row]
        if "naics_code" in row:
            indexes_of_attributes['soc_code'] = row.index("soc_code")
            indexes_of_attributes['case_status'] = row.index('case_status')
            indexes_of_attributes['job_title'] = row.index('soc_name')
            indexes_of_attributes['worksite_state'] = row.index('worksite_state')
        break
    return indexes_of_attributes


def find_unique_names(csv_read_obj, indexes_of_attributes, key):
    fin_list = []
    for row in csv_read_obj[1:]:
        # row = [word.lower() for word in row]
        name = row[indexes_of_attributes[key]]
        if name not in fin_list:
            fin_list.append(name)

    return fin_list


def find_number_of_certified(csv_read_obj, indexes_of_attributes, key):
    list_unique = find_unique_names(csv_read_obj, indexes_of_attributes, key)
    list_with_amount = []
    overall_amount = 0
    for name in list_unique:
        cert_amount = 0
        for row in csv_read_obj[1:]:
            # row = [word.lower() for word in row]
            if row[indexes_of_attributes[key]] == name and row[
                indexes_of_attributes['case_status']] == 'certified':
                cert_amount += 1
                overall_amount += 1

        if cert_amount == 0:
            pass
        else:
            list_with_amount.append([name, str(cert_amount)])

    for lst in list_with_amount:
        lst.append(str(round(int(lst[1]) / overall_amount * 100)) + '%')
        # dict_with_amount[key].append(str(round(dict_with_amount[key][0] / overall_amount * 100)) + '%')

    return list_with_amount


def final_prep(csv_read_obj, indexes_of_attributes, key):
    list_to_sort = find_number_of_certified(csv_read_obj, indexes_of_attributes, key)
    list_to_sort.sort(key=lambda l: int(l[1]), reverse=True)
    amount_of_elems = int(list_to_sort[0][1])
    finish = 0
    start = 0
    list_of_sorted_lists = []
    for ind in range(len(list_to_sort)):
        if int(list_to_sort[ind][1]) != amount_of_elems:
            amount_of_elems = int(list_to_sort[ind][1])
            finish = ind
            list_of_sorted_lists.append(sorted(list_to_sort[start:finish], key=lambda l: l[0]))
            start = finish
        if ind == len(list_to_sort) - 1:
            finish = ind+1
            list_of_sorted_lists.append(sorted(list_to_sort[start:finish], key=lambda l: l[0]))

    list_of_sorted_lists = [job for t in list_of_sorted_lists for job in t]
    return list_of_sorted_lists


with open('input2.txt', 'r') as csv_file:
    csv_read = list(csv.reader(csv_file, delimiter=";"))
    for i in range(len(csv_read)):
        csv_read[i] = [word.lower() for word in csv_read[i]]
    indexes_of_attributes = find_index(csv_read)
    jobs_list = final_prep(csv_read, indexes_of_attributes, 'job_title')
    states_list = final_prep(csv_read, indexes_of_attributes, 'worksite_state')

    with open('input2_jobs.txt', 'w+') as wf:
        wf.write('TOP_OCCUPATIONS; NUMBER_CERTIFIED_APPLICATIONS; PERCENTAGE' + '\n')
        for part in jobs_list:
            wf.write("; ".join(part) + "\n")

    with open('input2_states.txt', 'w+') as wf:
        wf.write('TOP_STATES; NUMBER_CERTIFIED_APPLICATIONS; PERCENTAGE' + '\n')
        for part in states_list:
            wf.write("; ".join(part) + "\n")

    # print(find_number_of_certified(csv_read, indexes_of_attributes, 'job_title'))
    # print(final_prep(csv_read, indexes_of_attributes, 'worksite_state'))
    # print(final_prep(csv_read, indexes_of_attributes, 'job_title'))
    # print(almost_fin_dict)
    # unique_lst = find_unique_codes(csv_read, indexes_of_attributes)
    # print(unique_lst)

    # for row in csv_read:
    #     row = [word.lower() for word in row]
    #     print(row[indexes_of_attributes['naics_index']], row[indexes_of_attributes['case_status']],
    #           row[indexes_of_attributes['job_title']])
    # #     row = [word.lower() for word in row]
    #     if "naics_code" in row:
    #         naics_index = row.index("naics_code")
    #         case_satus = row.index('case_status')
    #         job_title = row.index('soc_name')
    # # elif:
    # #     ""
    # else:
    #     print(row[naics_index], row[case_satus], row[job_title])

df = pd.read_csv('input1.csv', delimiter=";")
print(df[['WORKSITE_POSTAL_CODE', 'WORKSITE_STATE']])
