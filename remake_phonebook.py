import csv
import re


def remake_name(name_list: list):
    lenght = len(name_list)
    name_list[:3] = ' '.join(name_list[:3]).strip().split()
    if len(name_list) != lenght:
        name_list.insert(2, '')
    return name_list[:7]


def remake_phone(phone_list: list):
    phone = phone_list[5]
    pattern = r"(\+7|8)?\s*\(?(\d{3})\)?(-|\s)*(\d{3})(-|\s)*(\d{2})(-|\s)*(\d{2})\s*(\D*(\d{4})\)?)?"
    if phone.find('доб') == -1:
        phone_list[5] = re.sub(pattern, r"+7(\2)\4-\6-\8", phone)
    else:
        phone_list[5] = re.sub(pattern, r"+7(\2)\4-\6-\8 доб.\10", phone)
    return phone_list


def merging_of_identical_names(lst: list):
    dict_name = {}
    for data in lst:
        key = ' '.join(data[:2])
        if key not in dict_name:
            dict_name[key] = data[2:]
        else:
            dict_name[key] = list(map(lambda x: x[1] if x[1] else x[0], zip(dict_name[key], data[2:])))
    lst = [k.split() + v for k, v in dict_name.items()]
    return lst


def repair_address_book(address_book: str):
    file_name, file_extension = address_book.split('.')

    with open(address_book) as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    for name in contacts_list[1:]:
        remake_name(name)
        remake_phone(name)

    contacts_list = merging_of_identical_names(contacts_list)

    with open(f"{file_name}_corrected.{file_extension}", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)
