from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

con_dict = []


def change_names(contacts_list):
    keys = contacts_list[0]
    values = contacts_list[1:]
    for k, v in enumerate(values):
        con_dict.append({})
        for key, val in zip(keys, v):
            con_dict[k].update({key: val})

    for names in con_dict:
        name = names['lastname'].split()
        if len(name) == 3:
            names['lastname'] = name[0]
            names['firstname'] = name[1]
            names['surname'] = name[2]
        elif len(name) == 2:
            names['lastname'] = name[0]
            names['firstname'] = name[1]
            names['surname'] = ''
        else:
            names['lastname'] = name[0]
            names['firstname'] = ''
            names['surname'] = ''
    return con_dict


def change_phone(con_dict):
    phone_pattern = re.compile(r'(\+7|8)?\s*\(?(\d{3})\)?\s*\D?(\d{3})[-\s+]?(\d{2})-?(\d{2})((\s)?\(?(доб.)?\s?(\d+)\)?)?')
    phone_substitution = r'+7(\2)\3-\4-\5\7\8\9'

    for names in con_dict:
        phone = names['phone']
        if phone:
            names['phone'] = re.sub(phone_pattern, phone_substitution, phone)
    return con_dict


def merge_duplicates(con_dict):
    merged_dict = {}
    for con in con_dict:
        key = (con['lastname'], con['firstname'], con['surname'])
        if key not in merged_dict:
            merged_dict[key] = con
        else:
            existing_contact = merged_dict[key]
            for k in con.keys():
                if con[k] and con[k] != existing_contact[k]:
                    existing_contact[k] += f'; {con[k]}'

    return list(merged_dict.values())


if __name__ == '__main__':
    con_dict = change_names(contacts_list)
    con_dict = change_phone(con_dict)
    con_dict = merge_duplicates(con_dict)

    with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        header = ["lastname", "firstname", "surname", "phone", "email", "organization", "position"]
        datawriter.writerow(header)
        for contact in con_dict:
            datawriter.writerow([contact['lastname'], contact['firstname'], contact['surname'],
                                 contact['phone'], contact['email'], contact['organization'], contact['position']])