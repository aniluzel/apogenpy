from html_similarity import style_similarity, structural_similarity, similarity
from csv import reader
import requests
import csv
import advertools as adv
import jellyfish

# 0.48
def sim_check(web_page_similarity_percentage=0.60, web_path_similarity_percentage=0.88, param="struct"):
    links = []
    base = []
    urls = []
    html_text = []

    with open('output.csv', 'r') as read_obj:
        csv_reader = reader(read_obj, delimiter=',')
        header = next(csv_reader)

        if header is not None:
            for row in csv_reader:
                links.append(row)

        print(len(links))
    for i in links:
        html_text.append((i[0], requests.get(i[0]).text))

    for down in html_text:
        for up in reversed(html_text):
            # Link 1
            req1 = down[1]
            # Link 2
            req2 = up[1]
            # print("structural sim", structural_similarity(req1, req2))
            if param == "struct":
                base.append((structural_similarity(req1, req2), down[0], up[0]))
            # print("styles =", style_similarity(req1, req2))
            elif param == "style":
                base.append((style_similarity(req1, req2), down[0], up[0]))
            # print("sim", similarity(req1, req2))
            else:
                base.append((similarity(req1, req2), down[0], up[0]))
    print(len(base))
    for n in base:
        if n[0] < web_page_similarity_percentage:
            # print(n[0])
            urls.append(n[2])
    print(urls)
    urls = set(urls)
    urls = list(set(urls))
    print(len(urls), "urls")
    seen = set()
    result = []
    for item in urls:
        if item not in seen:
            seen.add(item)
            result.append(item)
    # print("list of urls", len(urls))
    print(len(result))
    #url_data = adv.url_to_df(result)
    url_data = adv.url_to_df(urls)

    result_final = []
    domain = url_data["scheme"] + "://" + url_data["netloc"]

    tmp_2 = []
    for i in url_data["path"]:
        tmp_2.append(i)

    empty_arr = []
    for path in tmp_2:
        for rev in reversed(tmp_2):
            #print(path, "  ", rev, " =", jellyfish.jaro_distance(path, rev))
            if web_path_similarity_percentage < jellyfish.jaro_distance(path, rev) < 0.99:
                #print(path, "  ", rev, " =", jellyfish.jaro_distance(path, rev))
                empty_arr.append(path)
                tmp_2.remove(rev)

    print(tmp_2)

    result_final.append(domain[0])
    for i in tmp_2:
        result_final.append(domain[0] + i)

    result_final = list(set(result_final))

    with open('filtered_output.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        # old
        # writer.writerow(result)

        # new
        writer.writerow(result_final)
        f.close()


sim_check()
