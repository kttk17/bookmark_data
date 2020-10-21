from urllib.parse import urlparse

f = open('userid_url_only_bookmark_201903.txt', mode='r')
line2 = f.readlines()

for line in line2:
    line = line.strip()
    line = line.split(':', 1)[1]
    parsed_url = urlparse(line.strip())
    with open('url_only_bookmark_201903_domain.txt', 'a')as url_domain:
        print(parsed_url.netloc, file=url_domain)
