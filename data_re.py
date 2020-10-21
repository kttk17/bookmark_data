f = open('userid_url_bookmark_201903.txt', mode='r')
line = f.readlines()

for line2 in line:

    line2 = line2.rstrip()
    userid = line2.split(',', 1)[0]
    bookmark = line2.rsplit(',', 1)[1]

    line2 = line2.split(',', 1)
    line2.pop(0)
    url = "".join(line2)
    url = url.rsplit(',', 1)[0]

    with open('userid_url_201903.txt', 'a') as uu:
        print(userid.rstrip() + ':' + url.rstrip(), file=uu)

    if bookmark == 'bookmark':
        with open('userid_url_only_bookmark_201903.txt', 'a') as only:
            print(userid.rstrip() + ':' + url.rstrip(), file=only)
