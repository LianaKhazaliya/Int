import csv

brand=str(input())
mark=str(input())
year=str(input())

with open('DATA.csv', mode = 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    data = []
    cur = 0
    cnt = 0
    c=1
    for row in reader:
        while c:
            if (row['Mark'] == mark):
                if (row['Brand'] == brand):
                    if (row['Year'] == year):
                        cur += int(row['Cost'])
                        cnr += 1

    a = cur/cnt
    print(a*0.8, a*1.2)