import json


def sortbyKey(array, _key):
    return sorted(array, key=lambda x: x[_key])


def add_no(fpath):
    f = open(fpath, 'r')
    jo = sortbyKey(json.load(f), 'domain')
    f.close()
    i = 0;
    for item in jo:
        item['id'] = i
        i += 1
    f = open(fpath, 'w')
    f.write(json.dumps(jo))
    f.close()


add_no('nginx.json')
