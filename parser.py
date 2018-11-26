import xml.etree.ElementTree as ET
from pprint import pprint as prettyprint
from config import ns0, xsi, file_path_nip, file_path_hsbb
from writer import *

def pprint(string):
    # prints out the node in an indented fashion
    prettyprint(string.decode('utf-8'))

def gen_tag(string, source=ns0):
    # helper for generating strings for searching tags
    return '%s%s' % (source, string)

nip = ET.parse(file_path_nip)
hsbb = ET.parse(file_path_hsbb)

cartridge = hsbb.find(gen_tag('cartridge'))

all_processes = {}
for process in cartridge.iter(gen_tag('process')):
    if process.get('name') is not None:
        all_processes[process.get('name')] = process

all_tasks = {}
for task in cartridge.iter(gen_tag('task')):
    if task.get('name') is not None:
        all_tasks[task.get('name')] = task

all_rules = {}
for rule in cartridge.iter(gen_tag('rule')):
    if rule.get('name') is not None:
        all_rules[rule.get('name')] = rule

def get_activities(process):
    activity_names = []
    for activity in process.iter(gen_tag('activity')):
        if activity.get('name') is not None:
            activity_names.append(activity.get('name'))
    return activity_names

output_processes = []
output_tasks = []
output_rules = []

# main
def prepare_output_for_process(process_name):
    starting_process = all_processes[process_name]

    output_processes.append(starting_process)
    activities = get_activities(starting_process)
    for task_name in filter(lambda task_name: task_name in activities, all_tasks):
        task = all_tasks[task_name]
        output_tasks.append(task)
        task_type = task.get(gen_tag('type', xsi))

        if task_type == 'ruleTaskType' and all_rules.get(task_name) is not None:
            output_rules.append(all_rules[task_name])
        
        elif task_type == 'subprocessTaskType':
            processes = []
            subprocess = task.find(gen_tag('subprocess'))
            processes.extend([elem for elem in subprocess.iter(gen_tag('condition')) if elem.text != 'null_rule'])
            processes.extend(subprocess.findall(gen_tag('process')))
            for process in processes:
                prepare_output_for_process(process.text)
                print(process.text)


prepare_output_for_process('A4.11_HOTES_New_Installation_Process')
writeXML(output_rules)

