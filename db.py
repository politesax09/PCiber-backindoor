import json



def read_modules():
    return json.load(open('db_module.json'))


def search_module(id):
    with open('db_module.json', 'r+') as f:
        data = json.load(f)
        for module in data['modules']:
            if module['id'] == id:
                return module
        return None


def read_backdoors():
    return json.load(open('db_backdoor.json'))


def search_backdoor(name):
    f = open('db_backdoor.json', 'r')
    data = json.load(f)
    for backdoor in data['backdoors']:
        if backdoor['name'] == name:
            return backdoor
    return None


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
                break
        
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)

