import csv
import re
file1 = 'info_1.txt'
file2 = 'info_2.txt'
file3 = 'info_3.txt'


def get_data(*args):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    for name in args:
        file = open(name, encoding="UTF-8")
        for line in file.readlines():
            insert = ''.join(re.findall(r'Изготовитель ОС:(.*)', line))
            os_prod_list.append(insert.strip())
            insert = ''.join(re.findall(r'Название ОС:(.*)', line))
            os_name_list.append(insert.strip())
            insert = ''.join(re.findall(r'Код продукта:(.*)', line))
            os_code_list.append(insert.strip())
            insert = ''.join(re.findall(r'Тип системы:(.*)', line))
            os_type_list.append(insert.strip())
    os_prod_list = list(filter(None, os_prod_list))
    os_name_list = list(filter(None, os_name_list))
    os_code_list = list(filter(None, os_code_list))
    os_type_list = list(filter(None, os_type_list))
    main_data = [['Изготовитель ОС', 'Название ОС', 'Код продукта', 'Тип системы'], os_prod_list, os_name_list, os_code_list, os_type_list]

    return main_data


def write_to_csv(name):
    with open(name, "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerows(get_data(file1, file2, file3))


write_to_csv('test2.csv')



