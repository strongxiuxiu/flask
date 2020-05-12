test_list = [{'name': 'tim', 'age': 10}, {'name': 'joy', 'age': '20'}, {'name': 'john', 'age': '18'}]

for id, value in enumerate(test_list):
    value['id'] = id
    print(id, value)
