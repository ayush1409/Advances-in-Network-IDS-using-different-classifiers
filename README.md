# Advances-in-Network-IDS-using-different-classifiers
Our proposed model is to implement the architecture of multimodel based Anomaly IDS with Neural Network (NN), Long short-term memory (LSTM) and Random Forest. We have integrated NN with Hidden Markov Model to improve our model. We have also tested our model by performing realtime attack on our model.

### Dataset
We have used <a href="https://www.unb.ca/cic/datasets/ids-2017.html">CIC-IDS 2017</a> dataset. It contains benign and the most up-to-date common attacks, which resembles the true real-world data (PCAPs). It also includes the results of the network traffic analysis using CICFlowMeter with labeled flows based on the time stamp, source, and destination IPs, source and destination ports, protocols and attack (CSV files). Also available is the extracted features definition. 

### Install CICflowmeter

```sh
git clone https://github.com/ayush1409/cicflowmeter-edited.git
cd cicflowmeter-edited
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

#### Now run the Network IDS

```
python manage.py runserver
```
Now in the main page, upload **flows.csv** file. The result screen will look like

![alt text](https://github.com/ayush1409/Advances-in-Network-IDS-using-different-classifiers/blob/main/NetworkIDS_output.jpg)
