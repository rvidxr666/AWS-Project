import boto3
import csv
import sys

s3 = boto3.client('s3')


def lambda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = str(event['Records'][0]['s3']['object']['key'])
    fileObj = s3.get_object(Bucket=source_bucket, Key=object_key)
    content_of_the_file = fileObj["Body"].read().decode("utf-8")
    lst = content_of_the_file.split("\n")

    csv_read = list(csv.reader(lst, delimiter=";"))
    for i in range(len(csv_read)):
        csv_read[i] = [word.lower() for word in csv_read[i]]
    indexes_of_attributes = find_index(csv_read)
    print(csv_read)

    try:
        jobs_list = final_prep(csv_read, indexes_of_attributes, 'job_title')
        states_list = final_prep(csv_read, indexes_of_attributes, 'worksite_state')
    except:
        sys.exit()

    jobs_string = 'TOP_OCCUPATIONS; NUMBER_CERTIFIED_APPLICATIONS; PERCENTAGE' + '\n'
    for job in jobs_list[:11]:
        jobs_string += '; '.join(job).upper() + '\n'
    s3.put_object(Bucket=source_bucket, Key=object_key.split('.')[0] + '_jobs.txt', Body=jobs_string)

    states_string = 'TOP_STATES; NUMBER_CERTIFIED_APPLICATIONS; PERCENTAGE' + '\n'
    for state in states_list[:11]:
        states_string += '; '.join(state).upper() + '\n'
    s3.put_object(Bucket=source_bucket, Key=object_key.split('.')[0] + '_states.txt', Body=states_string)


def find_index(csv_read_obj):
    indexes_of_attributes = {}
    for row in csv_read_obj:
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

    return list_with_amount


def final_prep(csv_read_obj, indexes_of_attributes, key):
    list_to_sort = find_number_of_certified(csv_read_obj, indexes_of_attributes, key)
    list_to_sort.sort(key=lambda l: int(l[1]), reverse=True)
    amount_of_elems = int(list_to_sort[0][1])
    start = 0
    list_of_sorted_lists = []
    for ind in range(len(list_to_sort)):
        if int(list_to_sort[ind][1]) != amount_of_elems:
            amount_of_elems = int(list_to_sort[ind][1])
            finish = ind
            list_of_sorted_lists.append(sorted(list_to_sort[start:finish], key=lambda l: l[0]))
            start = finish
        if ind == len(list_to_sort) - 1:
            finish = ind + 1
            list_of_sorted_lists.append(sorted(list_to_sort[start:finish], key=lambda l: l[0]))

    list_of_sorted_lists = [job for t in list_of_sorted_lists for job in t]
    return list_of_sorted_lists
