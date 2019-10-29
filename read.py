import re

with open('fstekout.txt', 'r', encoding='utf-16') as file:
    for line in file:
        if re.match('## Overwrite', line):
            path=re.search('(## Overwrite existing file:)\s*(.*)', line).group(2).strip()
            with open(path, 'r') as xml:
                for line in xml:
                    print(line)
            print('\n')