import xml.etree.ElementTree as ET
from pprint import pprint as prettyprint
from config import ns0

def pprint(string):
    # prints out the node in an indented fashion
    prettyprint(string.decode('utf-8'))

def gen_tag(string):
    # helper for generating strings for searching tags
    return '%s%s' % (ns0, string)

file_path = '../TM Uplift/process/A4.11_HOTES_New_Installation_Process.xml'

new_installation = ET.parse(file_path)

root = new_installation.getroot()
activities = root.findall(gen_tag('activity'))
activity_names = [activity.attrib['name'] for activity in activities]
print(len(activities))
pprint(ET.tostring(activities[0]))