import os
import re
import json

with open('JsonMakerMap.json', 'r') as mapfile:
    mapdata = json.load(mapfile)
    mapfile.close()

result = {}
doc=open('structureList.txt','w')

for entry in mapdata:
    # Handle overrides if they exist
    has_override = False
    try:
        override = entry['overrides']
        has_override = True
        print(f'Override found for \'{entry["path"]}\'')
    except KeyError:
        pass
    filedir =os.getcwd()+entry['path']
    filenames=os.listdir(filedir)
    for filename in filenames:
        if re.search('json', filename):
            filepath = filedir+'\\'+filename
            # Check for override and construct the string name accordingly
            if has_override and filename in override.keys():
                struname = re.sub(r'\..*$', "", filename) + override[filename]
                print(f'Suffix overrided for \'{filename}\' as \'{override[filename]}\'')
            else:
                struname = re.sub(r'\..*$', "", filename) + entry['suffix']
            # Write name into structure list
            doc.writelines(struname+'\n')
            # Load JSON data and add to result
            with open(filepath, 'r') as loot_table:
                jsondata = json.load(loot_table)
                loot_table.close()
            result[struname] = jsondata
            print(f'Added \'{struname}\' data from path: .{entry["path"] + "\\" + filename}')
doc.close()

# Sort by keys alphabetically
final_result = {k: result[k] for k in sorted(result.keys())}
with open('result.json', 'w') as f:
    json.dump(final_result, f, indent=4)
    f.close()
