import os

print(os.getcwd())

manta125 = False
manta235 = True
css100 = True
PM100 = False
LPR59 = False


def dump_file_to_file(in_name, out_file):
    with open(in_name, 'r') as in_file:
        input = in_file.read()
        out_file.write(input)


with open('/tmp/st_gen.cmd', 'w') as f:
    dump_file_to_file('st_components/init.txt', f)
    if(manta125):
        dump_file_to_file('st_components/manta125.txt', f)
    if(manta235):
        dump_file_to_file('st_components/manta235.txt', f)
    if(css100):
        dump_file_to_file('st_components/ccs100.txt', f)
    if(PM100):
        dump_file_to_file('st_components/PM100.txt', f)
    if(LPR59):
        dump_file_to_file('st_components/LPR59.txt', f)
    dump_file_to_file('st_components/tail.txt', f)
