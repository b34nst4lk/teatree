import xml.etree.ElementTree as ET

def writeXML(items):
    data = ET.Element('model')
    for item in items:
        data.append(item)

    mydata = ET.tostring(data)
    myfile = open("output.xml", "wb")
    myfile.write(mydata)


