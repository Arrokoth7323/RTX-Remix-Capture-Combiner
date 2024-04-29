# RTX-Remix-Capture-Combiner

A simple Python script using regex to merge a child capture's lights/meshes/materials/instances/cameras into a base capture. Duplicates will be accounted for and ignored.
Instances with the same ID between the base and child but different parameters will have their ID incremented until it is unique to both the base and child.

Recommended you make a backup of your base capture when exeucting this script in event of unforseen issues.

## Installation

Install the latest version of Python 3

```bash
 https://www.python.org/downloads/
```
    
## Run Locally

Clone the project

```bash
 git clone https://github.com/Arrokoth7323/RTX-Remix-Capture-Combiner
```

Go to the project directory

```bash
 cd RTX-Remix-Capture-Combiner
```

Replace paths for base_capture and child_capture in ```combine.py```

```bash
 base_capture_path = "Z:\\SteamLibrary\\steamapps\\common\\Star Wars Battlefront II Classic\\GameData\\rtx-remix\\captures\\Coruscant.usda"
 child_capture_path = "Z:\\SteamLibrary\\steamapps\\common\\Star Wars Battlefront II Classic\\GameData\\rtx-remix\\captures\\Coruscant-2.usda"
```

Execute the script

```bash
 python combine.py
```

You may now open RTX-Remix and choose the base capture to observe the child captures's merged items

## Feedback

Report any issues, comments, or concerns to arrokoth7323_53772 on Discord or leave a report on Github ```https://github.com/Arrokoth7323/RTX-Remix-Capture-Combiner/issues```


## License

RTX Remix Capture Combiner © 2024 by Arrokoth7323 is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International

