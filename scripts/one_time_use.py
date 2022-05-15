import json

all_data = []
all_links = set()
with open('database/department_old.jl', 'r') as f:
    data = list(f)
    for i in data:
        i = json.loads(i)
        if i['link'] not in all_links:
            all_links.add(i['link'])
            all_data.append(i)

with open('database/department.jl', 'w') as write_file:
    for i in all_data:
        line = json.dumps(i) + "\n"
        write_file.write(line)
