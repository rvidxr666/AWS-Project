import csv


# Function which finds indexes of specific attributes and stores them in a dictionary
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


# Function which searches for unique occupations or states in the provided file (depends on the provided key(
# "job_title" or "worksite_state")
def find_unique_names(csv_read_obj, indexes_of_attributes, key):
    fin_list = []
    for row in csv_read_obj[1:]:
        name = row[indexes_of_attributes[key]]
        if name not in fin_list:
            fin_list.append(name)

    return fin_list


# Function which iterates through unique occupations/states and checks for each appearance whether it is certified or
# not and therefore generates the overall number of certified appearances and number of certified appearances for each
# state/occupation. Finally returns a list for each of the unique occupation/states in such format:
# [Name, Number of Cert.Applications, Number of Cert.Applications/Overall Number of Cert Applications]
def find_number_of_certified(csv_read_obj, indexes_of_attributes, key):
    list_unique = find_unique_names(csv_read_obj, indexes_of_attributes, key)
    list_with_amount = []
    overall_amount = 0
    # Iteration through the list of unique occupations/states
    for name in list_unique:
        cert_amount = 0
        # Iteration through the entries
        for row in csv_read_obj[1:]:
            # Checking whether the entry is "Certified" and storing the count in overall_amount and in individual
            # cert_amount
            if row[indexes_of_attributes[key]] == name and row[
                indexes_of_attributes['case_status']] == 'certified':
                cert_amount += 1
                overall_amount += 1
        # If record is not certified we will not include it to the final output list
        if cert_amount == 0:
            pass
        else:
            list_with_amount.append([name, str(cert_amount)])

    # Finally we append the percentage of the certified state/occupation on overall amount of certified applications
    for lst in list_with_amount:
        lst.append(str(round(int(lst[1]) / overall_amount * 100)) + '%')

    return list_with_amount


# Function which performs final preparations of the data such as sorting. First of all, method will sort the output
# list from the method find_number_of_certified by the amount_of_applications, then after sorting by amount the function
# will use the "Two Pointers" technique for sorting alphabetically. So, it will find the specific entries in the
# provided sorted list with the same amount of certified applications, sort those entries and finally store in the final
# list
def final_prep(csv_read_obj, indexes_of_attributes, key):
    list_to_sort = find_number_of_certified(csv_read_obj, indexes_of_attributes, key)
    # Sorting the list of certified states/occupations by the amount of certified applications
    list_to_sort.sort(key=lambda l: int(l[1]), reverse=True)
    amount_of_elems = int(list_to_sort[0][1])
    start = 0
    list_of_sorted_lists = []
    # Iterating through sorted list
    for ind in range(len(list_to_sort)):
        if int(list_to_sort[ind][1]) != amount_of_elems:
            amount_of_elems = int(list_to_sort[ind][1])
            finish = ind
            # Isolating the parts with the same amount of certified applications, sorting them and storing in the final
            # list
            list_of_sorted_lists.append(sorted(list_to_sort[start:finish], key=lambda l: l[0]))
            start = finish
        if ind == len(list_to_sort) - 1:
            finish = ind + 1
            list_of_sorted_lists.append(sorted(list_to_sort[start:finish], key=lambda l: l[0]))

    list_of_sorted_lists = [job for t in list_of_sorted_lists for job in t]
    return list_of_sorted_lists


# Opening the input list
with open('input2.txt', 'r') as csv_file:
    csv_read = list(csv.reader(csv_file, delimiter=";"))
    # Making all the entries in the files lowercase in order to avoid problems with addressing
    for i in range(len(csv_read)):
        csv_read[i] = [word.lower() for word in csv_read[i]]
    indexes_of_attributes = find_index(csv_read)

    # Try/except block in order to avoid errors, in case if file will contain empty columns or will have a wrong
    # structure, the script will return the empty files with column names of the output file
    try:
        jobs_list = final_prep(csv_read, indexes_of_attributes, 'job_title')
        states_list = final_prep(csv_read, indexes_of_attributes, 'worksite_state')
    except:
        pass

    with open('input2_jobs.txt', 'w+') as wf:
        wf.write('TOP_OCCUPATIONS; NUMBER_CERTIFIED_APPLICATIONS; PERCENTAGE' + '\n')

        try:
            # Writing only first 10 unique jobs to the file
            for part in jobs_list[:11]:
                wf.write("; ".join(part).upper() + "\n")
        except:
            pass

    with open('input2_states.txt', 'w+') as wf:
        wf.write('TOP_STATES; NUMBER_CERTIFIED_APPLICATIONS; PERCENTAGE' + '\n')
        try:
            # Writing only first 10 unique states to the file
            for part in states_list[:11]:
                wf.write("; ".join(part).upper() + "\n")
        except:
            pass

