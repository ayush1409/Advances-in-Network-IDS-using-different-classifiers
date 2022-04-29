# Advances-in-Network-IDS-using-different-classifiers
Network based Intrusion Detection System using Machine Learning.

### Install CICflowmeter

```sh
git clone https://github.com/ayush1409/cicflowmeter-edited.git
cd cicflowmeter
python setup.py install
```

### Install Network IDS Django application

```sh
pip install -r requirements.txt
```
### Usage

#### First capture the network flow data

```sh
usage: cicflowmeter [-h] (-i INPUT_INTERFACE | -f INPUT_FILE) [-c] [-u URL_MODEL] output

positional arguments:
  output                output file name (in flow mode) or directory (in sequence mode)

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_INTERFACE    capture online data from INPUT_INTERFACE
  -f INPUT_FILE         capture offline data from INPUT_FILE
  -c, --csv, --flow     output flows as csv
```

Convert pcap file to flow csv:

```
cicflowmeter -f example.pcap -c flows.csv
```

Sniff packets real-time from interface to flow csv: (**need root permission**)

```
cicflowmeter -i eth0 -c flows.csv
```

#### First capture the network flow data

```
python manage.py runserver
```
Now in the main page, upload $flows.csv$ file. The result screen will look like



