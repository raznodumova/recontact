from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

con_dict = []


def change_names():
    keys = contacts_list[0]
    values = contacts_list[1:]
    for k, v in enumerate(values):
        con_dict.append({})
        for key, val in zip(keys, v):
            con_dict[k].update({key: val})

    for names in con_dict:
        fullname = names['firstname'] + ' ' + names['lastname'] + ' ' + names['surname']
        name = fullname.split()
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


def change_phone():
    phone_pattern = re.compile(r'(\+7|8)?\s*\(?(\d{3})\)?\s*\D?(\d{3})[-\s+]?(\d{2})-?(\d{2})((\s)?\(?(доб.)?\s?(\d+)\)?)?')
    phone_substitution = r'+7(\2)\3-\4-\5\7\8\9'

    for names in con_dict:
        phone = names['phone']
        if phone:
            names['phone'] = re.sub(phone_pattern, phone_substitution, phone)
    return con_dict


def merge_duplicates(contacts):
    merged_contacts = {}

    for contact in contacts:
        key = frozenset({contact['firstname'], contact['lastname']})

        if key not in merged_contacts:
            merged_contacts[key] = contact.copy()
        else:
            existing_contact = merged_contacts[key]
            for field in existing_contact:
                if existing_contact[field] == '' and contact[field] != '':
                    existing_contact[field] = contact[field]

    return list(merged_contacts.values())


def write_to_csv(contacts, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['lastname', 'firstname', 'surname', 'phone', 'email', 'organization', 'position']

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for contact in contacts:
            writer.writerow(contact)


if __name__ == '__main__':
    change_names()
    change_phone()
    pprint(con_dict)
    merged_contacts = merge_duplicates(con_dict)
    write_to_csv(merged_contacts, 'phonebook.csv')
