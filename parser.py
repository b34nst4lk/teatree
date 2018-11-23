import xml.etree.ElementTree as ET
from pprint import pprint as prettyprint
from config import ns0, file_path_nip, file_path_hsbb

def pprint(string):
    # prints out the node in an indented fashion
    prettyprint(string.decode('utf-8'))

def gen_tag(string):
    # helper for generating strings for searching tags
    return '%s%s' % (ns0, string)

nip = ET.parse(file_path_nip)
hsbb = ET.parse(file_path_hsbb)

output = []
activities = {}
for activity in nip.findall(gen_tag('activity')):
    activities[activity.get('name')] = activity
    output.append(activity)

cartridge = hsbb.find(gen_tag('cartridge'))
tasks = {}
for task in cartridge.iter(gen_tag('task')):
    if task.get('name') is not None:
        tasks[task.get('name')] = task

rules = {}
for rule in cartridge.iter(gen_tag('rule')):
    if rule.get('name') is not None:
        rules[rule.get('name')] = task

for activity_name in activities:
    if activity_name in tasks:
        output.append(tasks[activity_name])
    if activity_name in rules:
        output.append(rules[activity_name])

print(len(output))
print(output[-1])
pprint(ET.tostring(output[-1]))

# for activity in activity_names:
#     process = hsbb.find('.//%s//%s[@name="%s"]' % (gen_tag('cartridge'), gen_tag('process'), activity))
#     print(process)