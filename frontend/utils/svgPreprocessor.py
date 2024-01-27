import xml.etree.ElementTree as ET
import re

SVG_FILE_NAME = "batE-RDC1.svg"

tree = ET.parse(SVG_FILE_NAME)
root_element = tree.getroot()

output = ""

print(r""" 
 ______     ______    ____                          _            
/ ___\ \   / / ___|  / ___|___  _ ____   _____ _ __| |_ ___ _ __ 
\___ \\ \ / / |  _  | |   / _ \| '_ \ \ / / _ \ '__| __/ _ \ '__|
 ___) |\ V /| |_| | | |__| (_) | | | \ V /  __/ |  | ||  __/ |   
|____/  \_/  \____|  \____\___/|_| |_|\_/ \___|_|   \__\___|_|   

The elements that are already a room will be automatically selected
You will be asked to enter a name for the other ones, to keep the
original one just press enter
""")

for child in root_element:
    # We only care about groups in the svg, so we ignore the items that aren’t groups
    if not child.tag.endswith("g"):
        continue

    original_group_id = child.attrib.get('id')

    # If the name correspond to a room we make it uppercase add use the id
    if bool(re.match(r'^[A-Ea-e]\d{3}$', original_group_id)):
        group_id = original_group_id
        print("\033[0;36m[INFO]", group_id, "automatically selected\033[0m")
    else:
        # If not we ask for the new id
        group_id = input("\033[0;33m[INPUT] " + original_group_id + ": \033[0m")
        if group_id == "":
            # If nothing is entered we keep the original one
            group_id = original_group_id

    # If there is a dash in the name we need to add single quotes around it so that it works in JS
    if "-" in group_id:
        group_id = "'" + group_id + "'"

    # We add all path in the group
    paths = []
    for inner in child:
        if not inner.tag.endswith("path"):
            continue
        path = inner.attrib.get('d')
        paths.append(path)

    # We make the dictionnary string for this group
    output = output + (
                group_id + ": { color: \"grey\", state: true, path: [\"" + "\", \"".join(paths) + "\"], data:{} },\n")

print("\n\033[0;32m[OUTPUT]JS Dictionary : \033[0m")
print(output)
