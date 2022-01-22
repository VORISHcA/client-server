import yaml
main_dict = {
    '1': [1, 2, 3],
    '2': 4,
    '3': {'1': u'23€', '2': u'45€'}
}

with open('test_yaml', 'w', encoding='UTF-8') as ya_file:
    yaml.dump(main_dict, ya_file, default_flow_style=False, allow_unicode=True)

'Все нормально с евросами'
with open('test_yaml', 'r', encoding='UTF-8') as ya_file:
    data = yaml.safe_load(ya_file)
    print(data)

