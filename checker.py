from pprint import pprint

with open('brands.csv', mode = 'r') as Infile1:
    with open('DATA_F.csv', mode = 'r') as Infile2:
# with open('DATA_FINAL.csv', mode = 'w') as Outfile:
        cars = {'Brand Mark' : 0}
        for line in Infile1:
            cars[line[8:-10]] = 0
        for line in Infile2:
            cars[' '.join(line.split(',')[:2])] += 1

        for i in cars.keys():
            if cars[i] == 0:
                print(i)