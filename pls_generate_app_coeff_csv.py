import os
import csv

start = 'PLS_COEFS_'
end = '_10_REG_RGB_FULL'
tag = 'LAST'

with open(start + tag + end + '.csv', "w", newline='') as f:
    writer = csv.writer(f, delimiter=',')

    directory = '../PAD_Coefficients/PAD Coefficients_2021_06_16'
    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".csv") and tag in filename:
            print(os.path.join(directory, filename))
            s = os.path.basename(filename)
            print(s[s.find(start)+len(start):s.rfind(end)])

            with open(directory + '/' + filename, "r", newline='') as f:
                coeffs = []
                coeffs.append(s[s.find(start)+len(start):s.rfind(end)].lower())
                reader = csv.reader(f, delimiter=',')
                for l in reader:
                    if 'x' not in l[1]:
                        coeffs.append(l[1])
                print(coeffs) # l will be a Python list
                writer.writerow(coeffs) # write the header
            # writer = csv.writer(f, delimiter=',')
            # writer.writerow(header) # write the header
            # # write the actual content line by line
            # for l in lines:
            #     writer.writerow(l)
            # # or we can write in a whole
            # # writer.writerows(lines)
        else:
            continue
