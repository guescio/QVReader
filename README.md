# QVReader
A Python module to handle the output measurements of the Mitutoyo QVPAK software.

## Usage
QVReader can be used as a standalone script or as a module to be imported in other scripts.

### Standalone
Use QVReader alone to inspect the measurements contained in a file:
```bash
pyhton3 qvreader.py -f file.txt
```

### As a module
Import QVReader as a module in a script, then use it to handle QVPAK result files and retrieve measurements therein:
```bash
import qvreader
qvr = qvreader.qvreader("file.txt")
items = qvr.list()
plane_flatness = float(qvr.get("Plane", "plane")["Flatness"])`
```

## Help
```bash
python3 qvreader.py --help
```
