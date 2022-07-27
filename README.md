# Vulnage

Vulnage is a tool used to calculate the age of vulnerabilities from the [Pyne](https://www.github.com/Hoplite-Consulting/Pyne) output. 

Written by [Oliver Scotten](https://www.github.com/oliv10).

### Requirements
- Python 3.10.4 or greater

### Usage
- Install requirements
```
pip3 install -r requirements.txt
```

```
usage: vulnage.py [-h] [-v] [-f] [-c] csvFile writeFile

 _    _      _                         
| |  | |    | |                        
| |  | |   _| |____   ____  ____  ____ 
 \ \/ / | | | |  _ \ / _  |/ _  |/ _  )
  \  /| |_| | | | | ( ( | ( ( | ( (/ / 
   \/  \____|_|_| |_|\_||_|\_|| |\____)
                          (_____|      

Vulnage 1.0.0

positional arguments:
  csvFile         pyne csv output file
  writeFile       path to write file

options:
  -h, --help      show this help message and exit
  -v, --verbose   verbose output
  -f, --force     force overwrite of write file
  -c, --compress  write the most recent version of each unique vulnerability
```
