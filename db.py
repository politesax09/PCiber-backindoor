import json
from operator import truediv



def read_modules():
    return json.load(open('db_module.json'))


def read_backdoors():
    return json.load(open('db_backdoor.json'))


def add_backdoor(new_data):
    with open('db_backdoor.json', 'r+') as f:
        data = json.load(f)
        
        is_backdoor = False
        for backdoor in data['backdoors']:
            # Si ya existe una con mismo nombre, la edita
            if backdoor['name'] == new_data['name']:
                is_backdoor = True
                data['backdoors'].insert(data['backdoors'].index(backdoor), new_data)
                data['backdoors'].pop(data['backdoors'].index(backdoor))
                break
        if not is_backdoor:
            data['backdoors'].append(new_data)
    
        f.seek(0)
        json.dump(data, f, indent=4)


def remove_backdoor(name):
    with open('db_backdoor.json', 'r+') as f:
        data = json.load(f)

        # Busca por nombre, no puede haber dos con mismo nombre
        for backdoor in data['backdoors']:
            if backdoor['name'] == name:
                print('ENCONTRADA ', data['backdoors'].index(backdoor))
                data['backdoors'].pop(data['backdoors'].index(backdoor))
                break
        
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
