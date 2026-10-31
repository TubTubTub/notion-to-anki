# 1. Export main page as .md file
# 2. Run python file
# 3. Install Mass Deck Creation Anki addon
# 4. Copy and paste anki_tree.txt output to create new deck

res = []
TITLE_NAME = 'BRS Yr 2'

with open('ANKI DECK GENERATOR/BRS 7b5798c9ff2b83baafcb019d5bd31d47.md', 'r') as file:
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

with open('ANKI DECK GENERATOR/anki_tree.txt', 'w') as file:
    file.write('\n'.join(res))