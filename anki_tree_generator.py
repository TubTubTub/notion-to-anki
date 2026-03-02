res = []
TITLE_NAME = 'BRS'

with open('BRS 2a8f587eccc180619563c2ca6bcacfba.md', 'r') as file:
    lines = [x.strip() for x in file.readlines() if x.strip() != '']

    current_header = ''
    page_name = ''
    i = 0

    while i < len(lines):
        line = lines[i]

        if line[0:3] == '###':
            current_header = line[4:]
            print(current_header)
        elif line[0] == '[':
            page_name = line[1:line.index(']')]
            res.append(f'{TITLE_NAME}::{current_header}::{page_name}')
        
        i += 1

with open('anki_tree.txt', 'w') as file:
    file.write('\n'.join(res))