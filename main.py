# HOW TO USE

# 1. Change NOTE_NAME to desired name (for renaming assets)
# 2. Replace input.md and files in input/asset folder
# 3. Create new deck in Anki
# 4. Import output.txt and drag new files in output/asset into %AppData%\Anki2\User 1\collection.media

from pprint import pprint
from pathlib import Path
from urllib.parse import unquote
import shutil

NOTE_NAME = 'plasma'

def count_bold_level(line):
    i = 0

    while i < len(line) and line[i] == '#':
        i += 1
        
    return i

def empty_brackets(s):
    i = s.find('(')
    j = s.find(')', i + 1)
    out = s[i:j+1]

    s = ''.join(s.split(out))
    
    i = s.find('[')
    j = s.find(']', i + 1)
    out = s[i+1:j]

    s = ''.join(s.split(out))

    return s

def replace_images(lines):
    new_lines = []
    p = Path("input/assets")
    image_index = 0
    
    files = [f for f in p.rglob('*') if f.is_file()]
    assets = { f.name:str(f.resolve()) for f in files }

    for line in lines:
        if '![' in line:
            file_name = line[line.find('(') + 1 : line.find(')')]
            file_name = unquote(file_name) # Processes %20 characters

            extension = file_name.rpartition('.')[-1]
            new_file_name = NOTE_NAME + '_' + str(image_index) + '.' + extension

            if extension not in ['png', 'jpg', 'jpeg']:
                raise Exception('Unaccounted extension:', file_name)

            line = line.replace('!', '')
            line = empty_brackets(line)
            line = line.replace('[]', f'<img src={new_file_name}>')

            src_path = assets[file_name]
            dest_path = Path('output/assets') / new_file_name
            shutil.copy2(src_path, dest_path)
            
            image_index += 1

            print(line)

        new_lines.append(line)
    return new_lines

def parse(lines):
    res = {}
    current_level = []
    current_description = '"'

    for line in lines:
        level = count_bold_level(line)
        if level > 0:
            if current_level == []:
                current_level.append(line)
            else:
                if current_description.strip() != '"' and 'Learning Objectives' not in current_description:
                    print(current_level)
                    new_title = '"<h4>' + ' → '.join(current_level[:-1]).replace('#', '').strip() + ' →' + '</h4>' + '<h2>' + current_level[-1].replace('#', '').strip() + '</h2>"'
                    res[new_title] = current_description + '"'
                    
                current_description = '"'

                if level > count_bold_level(current_level[-1]):
                    current_level.append(line)
                else:
                    current_level = current_level[:level - 1]
                    current_level.append(line)
        else:
            current_description += line
            current_description += '\n'
    
    new_title = '"<h4>' + ' → '.join(current_level[:-1]).replace('#', '') + ' →' + '</h4>' + '<h2>' + current_level[-1].replace('#', '') + '</h2>"'
    res[new_title] = current_description + '"'

    return res

res = {}

with open("input/input.md", 'r', encoding='utf-8') as file:
    content = file.read()
    lines = content.split('\n')
    
    lines = [x.replace('|', '/') for x in lines]
    lines = replace_images(lines)
    res = parse(lines)

with open("output/output.txt", 'w', encoding='utf-8') as file:
    for key, value in res.items():
        file.write(key)
        file.write('|')
        file.write(value)
        file.write('\n')