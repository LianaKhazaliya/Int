from pprint import pprint

with open('DATA_F.csv', mode = 'r') as Infile:
    with open('DATA_FINAL.csv', mode = 'w') as Outfile:
        cnt1, cnt2, cnt3 = 0, 0, 0
        lines = Infile.read().splitlines()
        
        for line in lines:
            sep_line = line.split(',')
            
            if len(sep_line) == 14:
                if sep_line[3][:5] == 'https':
                    print(line, file=Outfile)
                else:
                    fragment = ' '.join(sep_line[2:4])
                    new_line = ','.join(sep_line[:2]+[fragment]+sep_line[4:-1]+['NoData', sep_line[-1]])
                    print(new_line, file=Outfile)

            elif len(sep_line) < 14:
                print(','.join(sep_line[:-1]+['NoData', sep_line[-1]]), file=Outfile)
   
            else:
                i = 0
                while sep_line[i][:5] != 'https':
                    i += 1
                fragment = ' '.join(sep_line[2:i])
                new_line = ','.join(sep_line[:2]+[fragment]+sep_line[i:])
                new_sep_line = new_line.split(',')
                if len(new_sep_line) == 14:
                    if new_sep_line[3][:5] == 'https':
                        print(new_line, file=Outfile)
                    else:
                        print(new_line)
                elif len(new_sep_line) < 14:
                    print(','.join(sep_line[:-1]+['NoData', sep_line[-1]]), file=Outfile)
                    
                    

                    