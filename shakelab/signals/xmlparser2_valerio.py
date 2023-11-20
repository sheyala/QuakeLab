import xml.etree.ElementTree as ET
import io

def convert (string):
    """
    """
    try:
        return float(string)
    except:
        return string

def xml_to_dict(xml):
    """
    """
    xml_string = io.StringIO(xml)
    
    it = ET.iterparse(xml_string)

    # Strip namespaces (ns)
    # Author: Nonagon
    for _, el in it:
        _, _, el.tag = el.tag.rpartition('}')

    # Stripping ns also from attributes
    # Author: DisappointedByUnaccountableMod
    #for _, el in it:
    #    if '}' in el.tag:
    #        el.tag = el.tag.split('}', 1)[1]  # strip all namespaces
    #    for at in list(el.attrib.keys()): # strip namespaces of attributes too
    #        if '}' in at:
    #            newat = at.split('}', 1)[1]
    #            el.attrib[newat] = el.attrib[at]
    #            del el.attrib[at]

    return it.root
    #return root_to_dict(it.root)

def root_to_dict(root):
    """
    Iterative function
    """
    """
    xml_dict = []

    if root.attrib:
        xml_dict.append({'attribute' : root.attrib})

    if root.text:
        xml_dict.append(convert(root.text))

    if len(root):
        for elem in root:
            xml_dict = xml_dict + [root_to_dict(elem)]
            if elem.tail:
                xml_dict = xml_dict + [convert(elem.tail)]

    xml_dict = xml_dict[0] if len(xml_dict)==1 else xml_dict

    return {root.tag : xml_dict}
    """
    xml_dict = {}

    xml_dict['attribute'] = root.attrib if root.attrib else {}

    xml_dict['value'] = []
    if root.text:
        xml_dict['value'] = [convert(root.text)]

    if len(root):
        for elem in root:
            xml_dict['value'] += [root_to_dict(elem)]
            if elem.tail:
                xml_dict['value'] += [convert(elem.tail)]

    #xml_dict = xml_dict[0] if len(xml_dict)==1 else xml_dict

    return {root.tag : xml_dict}

def xml_strip(xml):
    """
    Function to remove with spaces and new line from xml string.
    """
    lines = xml.split('\n')
    buffer = []
    for x in lines:
        y = x.strip()
        if y: buffer.append(y)
    buffer = ''.join(buffer)
    buffer = buffer.replace("  ","")
    buffer = buffer.replace("> <","><")
    return buffer

def xml2py(node):
    """
    convert xml to python object
    node: xml.etree.ElementTree object
    Author: Petr Dvořáček
    """

    name = node.tag

    pytype = type(name, (object, ), {})
    pyobj = pytype()

    for attr in node.attrib.keys():
        setattr(pyobj, attr, node.get(attr))

    if node.text and node.text not in ['', ' ', '\n']:
        setattr(pyobj, 'text', node.text)

    for cn in node:
        if not hasattr(pyobj, cn.tag):
            setattr(pyobj, cn.tag, [])
        getattr(pyobj, cn.tag).append(xml2py(cn))

    return pyobj
