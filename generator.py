import json

with open('data/corner_mapping.json', 'r', encoding='utf-8') as file:
    mp = json.load(file)
    omp = mp["Orientation"]
    pmp = mp["Position"]
    for ky, vl in pmp.items():
        lst=[]
        for it in ky:
            lst.append(omp[it])
        print(vl, ":", lst)

with open('data/edge_mapping.json', 'r', encoding='utf-8') as file:
    mp = json.load(file)
    omp = mp["Orientation"]
    pmp = mp["Position"]
    for ky, vl in pmp.items():
        lst=[]
        for it in ky:
            lst.append(omp[it])
        print(vl, ":", lst)