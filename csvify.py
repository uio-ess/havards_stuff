# Take a nastran output file, find node displacement data, put in CSV file
input_file = '/Users/haavagj//Downloads/adnw41d05.OUT'
output_file = '/tmp/outfile.csv'
node_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

with open(output_file, 'w') as outfile:
    with open(input_file, 'r') as infile:
        look_for_data = False
        for line in infile:
            # Kun se etter data etter man ser som inneholder D I S P...
            if( line.find('D I S P L A C E M E N T   V E C T O R') > 0):
                look_for_data = True
            # Avbryt soeket etter man ser en linje som inneholder MAXIMU...
            if( line.find('MAXIMUM DISPLACEMENT MAGNITUDE') > 0):
                break
            # Splitt linjen med whitespace, ta bort linjeskift
            numbers = line.replace('\r\n', '').split()
            if( look_for_data and 
                len(numbers) == 8 and
                numbers[0].isdigit() and
                int(numbers[0]) in node_list):
                print(numbers)
                outfile.write(';'.join(numbers) + '\r\n')
