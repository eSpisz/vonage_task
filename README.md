## Installation

1. Clone repo 
```
git clone https://github.com/eSpisz/vonage_task.git
cd vonage_task
```

2. MacOS/Linux
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Windows
```
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage example
```
python3 solution.py --yaml-file <yaml_file_path> --docker-file <docker_file_path>
```

## Additional information

Output will be in output_files directory

The Code was written following SOLID principles 

The code was developed in python virtual env and required modules need to be installed using requirements.txt file

The code was linted using a PEP 8-compliant black formatter

To perform functional test pytest module was used
