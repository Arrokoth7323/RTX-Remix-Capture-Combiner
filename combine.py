"""
Project: RTX Remix Capture Combiner
File: combine.py
Author: Arrokoth7323
Date: 04-29-2024

Description: A simple Python script using regex to merge a child capture's lights/meshes/materials/instances/cameras into a base capture. Duplicates will be accounted for and ignored.
Instances with the same ID between the base and child but different parameters will have their ID incremented until it is unique to both the base and child.
Recommended you make a backup of your base capture when exeucting this script in event of unforseen issues.

Report any issues, comments, or concerns to arrokoth7323_53772 on Discord or leave a report on Github https://github.com/Arrokoth7323/RTX-Remix-Capture-Combiner

Requirements: Latest Python 3 https://www.python.org/downloads/
Usage: Replace corresponding base_capture_path & child_capture_path with the locations of your respective captures. Then from command line execute using "python combine.py".

License: RTX Remix Capture Combiner © 2024 by Arrokoth7323 is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""
import re


def insert_lines(insert_line, base_contents, base_items, child_items, item_type):
    base_item_ids = list(base_items)
    for i, item in enumerate(base_item_ids):
        base_item_ids[i] = item.split("\n")[0]

    child_item_ids = list(child_items)
    for i, item in enumerate(child_item_ids):
        child_item_ids[i] = item.split("\n")[0]

    indices_child = [[j, i] for i, x in enumerate(base_item_ids) for j, y in enumerate(child_item_ids) if x == y]

    if item_type == "instance":
        for index in indices_child:
            if child_items[index[0]] != base_items[index[1]]:
                increment = 1
                child_id = child_item_ids[index[0]]
                child_id_short = re.search(r'".+?"', child_id).group(0)
                child_id_short_split = child_id_short.replace('"', '').rsplit('_', 1)
                child_id_short_incremented = f'"{child_id_short_split[0]}_{(int(child_id_short_split[1])+increment)}"'
                child_id_incremented = child_id.replace(child_id_short, child_id_short_incremented)

                while (child_id_incremented in base_item_ids) or (child_id_incremented in child_item_ids):
                    increment = increment + 1
                    child_id_short_incremented = f'"{child_id_short_split[0]}_{(int(child_id_short_split[1])+increment)}"'
                    child_id_incremented = child_id.replace(child_id_short, child_id_short_incremented)
                else:
                    child_item_ids.append(child_id_incremented)
                    child_items[index[0]] = child_items[index[0]].replace(child_item_ids[index[0]], child_id_incremented)

        base_item_ids = list(base_items)
        for i, item in enumerate(base_item_ids):
            base_item_ids[i] = item.split("\n")[0]

        child_item_ids = list(child_items)
        for i, item in enumerate(child_item_ids):
            child_item_ids[i] = item.split("\n")[0]

        indices_child = [[j, i] for i, x in enumerate(base_item_ids) for j, y in enumerate(child_item_ids) if x == y]
        

    if not (len(indices_child) == len(child_items)):
        for index in sorted(indices_child, reverse=True):
            del child_items[index[0]]

        if base_contents[(insert_line-1)] != "    {":
            child_items[0] = "\n" + child_items[0]

        for i, item in enumerate(reversed(child_items)):
            if item not in base_items:
                item_lines = (item.split("\n"))

                if (i != 0):
                    item_lines.append("\n")

                for line in reversed(item_lines):
                    if not line.endswith("\n"):
                        line = line + "\n"
                        
                    base_contents.insert(insert_line, line)

                item = re.search(r'".+?"', item).group(0)
                print(f'Added {item_type} {item}')

        base_capture = open(base_capture_path, 'w')

        base_capture.seek(0)
        base_capture.truncate(0)
        base_capture.writelines(base_contents)

        base_capture.close()
    else:
        print(f"No new {item_type}s identified to be added!")


def identify_items(section_regex, item_type):
    def captures_items(capture_path):
        capture = open(capture_path, 'r')
        capture_contents = capture.readlines()
        capture.seek(0)
        capture_text = capture.read()
        capture.close()

        capture_match = re.search(r'    def %s.+?\n.+?\n    }' % section_regex, capture_text, re.DOTALL)

        if capture_match != None:
            insert_line = 0
            items = capture_match.group(0)
            items_match = re.findall(r'        def .+?\n.+?\n        }', items, re.DOTALL)

            for number, line in enumerate(capture_contents, 0):
                if line.strip() == items.split("\n")[0].strip():
                    insert_line = number + (len(items.split("\n")) - 1)
                    break

            return {"insert_line": insert_line, "items": items_match, "capture_contents": capture_contents}
        else:
            return {"insert_line": None, "items": None, "capture_contents": capture_contents}

    
    base_capture_dict = captures_items(base_capture_path)
    child_capture_dict = captures_items(child_capture_path)

    if child_capture_dict["items"] != None:
        insert_lines(base_capture_dict["insert_line"], base_capture_dict["capture_contents"], base_capture_dict["items"], child_capture_dict["items"], item_type)
    else:
        print(f"No new {item_type}s identified to be added!")


base_capture_path = "Z:\\SteamLibrary\\steamapps\\common\\Star Wars Battlefront II Classic\\GameData\\rtx-remix\\captures\\Coruscant.usda"
child_capture_path = "Z:\\SteamLibrary\\steamapps\\common\\Star Wars Battlefront II Classic\\GameData\\rtx-remix\\captures\\Coruscant-2.usda"

identify_items('Xform "lights"', 'light')
identify_items('"meshes"', 'mesh')
identify_items('"Looks"', 'material')
identify_items('Xform "instances"', 'instance')
identify_items('Xform "cameras"', 'camera')
