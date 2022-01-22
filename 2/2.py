import json


def write_order_to_json(item, quantity, price, buyer, data):
    d = {'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'data': data}
    with open('orders.json', 'w') as json_file:
        json.dump(d, json_file, indent=4)

        
write_order_to_json(1,2,3,4,5)
