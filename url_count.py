f = open('url_only_bookmark_201903_domain.txt', mode='r')
line2 = f.readlines()
url_domain = []

for line in line2:
    line = line.strip()
    url_domain.append(line)

url_domain_no_duplication = list(set(url_domain))


with open('url_domain_201903_count.txt', 'a')as count:
    # print('url_sum', ':', len(url_domain), file=count)
    for i in range(len(url_domain_no_duplication)):
        print(url_domain_no_duplication[i], ':', url_domain.count(url_domain_no_duplication[i]), file=count)
