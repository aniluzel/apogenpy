from collections import OrderedDict

from html_similarity import style_similarity, structural_similarity, similarity
from csv import reader
import requests
import csv


def sim_check():
    array = []
    struct = []
    style = []
    sim = []
    sorted = []
    new_array = []
    with open('output.csv', 'r') as read_obj:
        csv_reader = reader(read_obj, delimiter=',')
        header = next(csv_reader)

        if header is not None:
            for row in csv_reader:
                array.append(row)

    for i in array:
        new_array.append(i[0])

    for down in new_array:
        for up in reversed(new_array):
            # Link 1
            req1 = requests.get(down).text
            # Link 2
            req2 = requests.get(up).text
            # print("structural sim", structural_similarity(req1, req2))
            struct.append((structural_similarity(req1, req2), down, up))
            # print("styles =", style_similarity(req1, req2))
            style.append((style_similarity(req1, req2), down, up))
            # print("sim", similarity(req1, req2))
            sim.append((similarity(req1, req2), down, up))

    for n in struct:
        if n[0] < 0.48:
            #print(n[0])
            sorted.append(n[2])

    sorted = set(sorted)
    sorted = list(set(sorted))

    seen = set()
    result = []
    for item in sorted:
        if item not in seen:
            seen.add(item)
            result.append(item)
    # print("list of thinks", len(sorted))
    # for i in result:
    #     print(i)

    with open('filtered_output.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(result)



sim_check()
