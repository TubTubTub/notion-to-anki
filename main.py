# HOW TO USE

# (Make sure no notes before first heading in Notion page)
# (Tables are not supported, take a screenshot and paste it in as an image instead)
# (Delete any unwanted toggle headings afterwards)

# 1. Create new deck in Anki
# 2. Export Notion pages into individual .md files and image folders (Export each Notion page individually)
# 3. Move exported folder into input folder
# 4. Check for notes before first heading, tables, and toggles
# 4. Import output.txt and drag new files in output/asset into %AppData%\Anki2\User 1\collection.media

from pprint import pprint
from pathlib import Path
from urllib.parse import unquote
import shutil

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

def replace_images(images_folder, lines, file_name):
    new_lines = []
    image_index = 0
    
    images = [f for f in images_folder.rglob('*') if f.is_file() and f.suffix != '.md']
    assets = { f.name:str(f.resolve()) for f in images }
    print(images)
    print(assets)

    for line in lines:
        if '![' in line:
            image_path = line[line.find('(') + 1 : line.find(')')]
            image_path = unquote(image_path) # Processes %20 characters
            print(image_path)
            image_name = image_path.split('/')[1]
            extension = image_name.rpartition('.')[-1]
            
            if extension not in ['png', 'jpg', 'jpeg']:
                raise Exception('Unaccounted extension:', image_path)
            
            new_image_path = file_name + '_' + str(image_index) + '.' + extension
            
            line = line.replace('!', '')
            line = empty_brackets(line)
            line = line.replace('[]', f"<img src='{new_image_path}'>")

            src_path = assets[image_name]
            dest_path = Path('output/assets') / new_image_path
            shutil.copy2(src_path, dest_path)
            
            image_index += 1

            # print(line)

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

input_folder = Path("input")
output_folder = Path("output")

for folder_path in input_folder.iterdir():
    if not folder_path.is_dir():
        continue

    res = {}
    image_folder = None
    md_path = None

    for item in folder_path.iterdir():
        print(item)
        if item.is_dir():
            image_folder = item
        elif item.is_file() and item.suffix == '.md':
            md_path = item

    with open(md_path, 'r', encoding='utf-8') as file:
        content = file.read()
        lines = content.split('\n')
        
        lines = [x.replace('|', '/') for x in lines]
        lines = replace_images(image_folder, lines, folder_path.name)
        res = parse(lines)

    with open(f"output/{folder_path.name}.txt", 'w', encoding='utf-8') as file:
        for key, value in res.items():
            file.write(key)
            file.write('|')
            file.write(value)
            file.write('\n')