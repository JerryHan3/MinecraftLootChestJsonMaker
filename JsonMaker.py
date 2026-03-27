import os, re, json, time, traceback
from colorama import Fore, Style

with open('JsonMakerMap.json', 'r') as mapfile:
    mapdata = json.load(mapfile)
    mapfile.close()

result = {}
doc=open('structureList.txt','w')
error_log_name = f'error_{time.strftime("%Y-%m-%d_%H-%M-%S")}.log'
error_log = open(error_log_name, 'w')
error_count = [0, 0]

for entry in mapdata:
    # Handle overrides if they exist
    has_override = False
    try:
        override = entry['overrides']
        has_override = True
        print(f'{Fore.CYAN}[i]{Style.RESET_ALL} Override found for \'{entry["path"]}\'')
    except KeyError:
        pass
    filedir = os.getcwd()+entry['path']
    if not os.path.exists(filedir):
        print(f'{Fore.RED}[X] Directory not found: {filedir}{Style.RESET_ALL}')
        error_log.write(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Directory not found: {filedir}\n')
        error_count[0] += 1
        continue
    filenames = os.listdir(filedir)
    for filename in filenames:
        if re.search('json', filename):
            filepath = filedir+'\\'+filename
            # Check for override and construct the string name accordingly
            if has_override and filename in override.keys():
                struname = re.sub(r'\..*$', "", filename) + override[filename]
                print(f'{Fore.CYAN}[i]{Style.RESET_ALL} Suffix overridden for \'{filename}\' as \'{override[filename]}\'')
            else:
                struname = re.sub(r'\..*$', "", filename) + entry['suffix']
            # Write name into structure list
            doc.writelines(struname+'\n')
            # Load JSON data and add to result
            with open(filepath, 'r') as loot_table:
                try:
                    jsondata = json.load(loot_table)
                    loot_table.close()
                except json.JSONDecodeError as e:
                    print(f'{Fore.RED}[X] Error decoding JSON from file: {filepath}. \nError: {e.msg}{Style.RESET_ALL}')
                    error_log.write(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] Error decoding JSON from file: {filepath}: \n{traceback.format_exc()}\n')
                    error_count[1] += 1
                    continue
            result[struname] = jsondata
            print(f'{Fore.GREEN}[√]{Style.RESET_ALL} Added \'{struname}\' data from path: .{entry["path"] + "\\" + filename}')
doc.close()
error_log.close()

print("\n")
if error_count[0] > 0 or error_count[1] > 0:
    print(f'{Fore.YELLOW}[!] {error_count[0]} directories not found, {error_count[1]} loot tables failed to merge. Check {error_log_name} for details.\n{Style.RESET_ALL}')
else:
    print(f'{Fore.GREEN}[√]{Style.RESET_ALL} All loot tables merged successfully without errors.')
    os.remove(error_log_name)

# Sort by keys alphabetically
final_result = {k: result[k] for k in sorted(result.keys())}
with open('result.json', 'w') as f:
    json.dump(final_result, f, indent=4)
    f.close()
