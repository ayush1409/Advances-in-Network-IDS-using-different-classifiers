from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
import joblib
import pandas as pd
import csv
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
import collections
from keras.models import load_model

# labels = ['BENIGN', 'Infiltration', 'DDoS', 'DoS_slowloris',
#        'DoS_Slowhttptest', 'DoS_Hulk', 'DoS_GoldenEye', 'Heartbleed',
#        'Bot', 'FTP_Patator', 'SSH_Patator', 'Web_Attack_Brute_Force',
#        'Web_Attack_XSS', 'Web_Attack_Sql_Injection', 'PortScan']


labels = ['BENIGN', 'Bot', 'DDoS', 'DoS_GoldenEye', 'DoS_Hulk', 'DoS_Slowhttptest', 'DoS_slowloris', 'FTP_Patator', 'Heartbleed', 'Infiltration', 'PortScan',
 'SSH_Patator', 'Web_Attack_Brute_Force', 'Web_Attack_Sql_Injection', 'Web_Attack_XSS']


final_cols = ['dst_port', 'flow_duration', 'tot_fwd_pkts', 'tot_bwd_pkts', 
 'totlen_fwd_pkts', 'totlen_bwd_pkts', 'fwd_pkt_len_max', 'fwd_pkt_len_min', 
 'fwd_pkt_len_mean', 'fwd_pkt_len_std', 'bwd_pkt_len_max', 'bwd_pkt_len_min', 
 'bwd_pkt_len_mean', 'bwd_pkt_len_std', 'flow_byts_s', 'flow_pkts_s', 
 'flow_iat_mean', 'flow_iat_std', 'flow_iat_max', 'flow_iat_min', 
 'fwd_iat_tot', 'fwd_iat_mean', 'fwd_iat_std', 'fwd_iat_max', 
 'fwd_iat_min', 'bwd_iat_tot', 'bwd_iat_mean', 'bwd_iat_std', 
 'bwd_iat_max', 'bwd_iat_min', 'fwd_psh_flags', 'bwd_psh_flags', 
 'fwd_urg_flags', 'bwd_urg_flags', 'fwd_header_len', 'bwd_header_len', 
 'fwd_pkts_s', 'bwd_pkts_s', 'pkt_len_min', 'pkt_len_max', 
 'pkt_len_mean', 'pkt_len_std', 'pkt_len_var', 'fin_flag_cnt', 
 'syn_flag_cnt', 'rst_flag_cnt', 'psh_flag_cnt', 'ack_flag_cnt', 
 'urg_flag_cnt', 'cwe_flag_count', 'ece_flag_cnt', 'down_up_ratio', 
 'pkt_size_avg', 'fwd_seg_size_avg', 'bwd_seg_size_avg', 'fwd_header_len', 
 'fwd_byts_b_avg', 'fwd_pkts_b_avg', 'fwd_blk_rate_avg', 'bwd_byts_b_avg', 'bwd_pkts_b_avg',
 'bwd_blk_rate_avg', 'subflow_fwd_pkts', 'subflow_fwd_byts', 'subflow_bwd_pkts', 'subflow_bwd_byts',
 'init_fwd_win_byts', 'init_bwd_win_byts', 'fwd_act_data_pkts', 'fwd_seg_size_min',
 'active_mean', 'active_std', 'active_max', 'active_min', 'idle_mean', 'idle_std', 'idle_max',
 'idle_min']


def index(request):

    if request.method == "POST":
        print('Post request hit')
        form = UploadFileForm(request.POST, request.FILES)

        # for field in form:
            # print("Field Error:", field.name,  field.errors)

        if form.is_valid():
            # get the file
            file = request.FILES['log_file']

            # preprocess the file
            # data = preprocess_file(file)
            data = preprocess_csv_file(file)
            # print("File name: {}, File size: {}".format(file.name, file.size))

            # use model to generate the result of the log file
            # 1. load the model
            model_rf = joblib.load("saved_models/IDS_model_RF.joblib")
            model_nn = load_model("saved_models/IDS_model_NN.h5")
            # print(model.get_params)

            # 2. predict the results using model
            # predictions = model.predict(data)
            y_probs = model_nn.predict(data)
            predictions = y_probs.argmax(axis=1)


            # 3. pass the result to the UI
            # print(np.unique(np.array(predictions)))
            unique, counts = np.unique(predictions, return_counts = True)
            # print('unique : {}, count : {}'.format(unique, counts))

            # submit a response to UI saying whether an intrusion happened or not? 
            
            label_count_dict = {}

            for i, label in zip(range(len(labels)), labels):
                label_count_dict[label] = (predictions == i).sum()

            context = {
                'file' : file,
                'label_count_dict' : label_count_dict
            }
            # return HttpResponse("hello")
            return render(request, 'output.html', context)

    else:
        form = UploadFileForm()
    context = {
        'team' : 'Pegasus',
        'form' : form, 
    }
    return render(request, 'team.html', context)


# def output(request):
#     return HttpResponse("Result here")


# function to preprocess the file taken as input
def preprocess_file(file):

    # 1. make pandas df using file content
    csv_file = file.read().decode('utf-8')
    lines = csv_file.split('\n')
    
    data = []
    for line in lines:
        data.append([x.strip() for x in line.split(',')])
    
    df = pd.DataFrame(data[1:], index = None, columns = data[0])
    df = df.sample(frac=1)
    # df.drop('Label', axis=1, inplace=True)
    df.dropna(inplace=True)
    df = df.astype('float64')
    # print(df.info())
    
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)
    # print(df.head())

    X = np.array(df.iloc[:, :])
    # X = X[~np.isnan(X).any(axis=1), :]
    # X.astype('float64')
    
    # for col in df.columns:
        # df[col] = df[col].astype('float64')
    # print(df.columns)

    # 2. Drop the labels column

    # 3. Normalise the data

    scaler = RobustScaler()
    scaler.fit(X)
    X = scaler.transform(X)

    # 4. return the normalised data
    return X

def preprocess_csv_file(file):
    # 1. make pandas df using file content
    csv_file = file.read().decode('utf-8')
    lines = csv_file.split('\n')
    
    data = []
    for line in lines:
        data.append([x.strip() for x in line.split(',')])
    
    df = pd.DataFrame(data[1:], index = None, columns = data[0])
    df = df.sample(frac=1)

    df.drop('src_ip', axis=1, inplace=True)
    df.drop('dst_ip', axis=1, inplace=True)
    df.drop('src_port', axis=1, inplace=True)

    df = df[final_cols]
    # df.drop('Label', axis=1, inplace=True)
    df.dropna(inplace=True)
    df = df.astype('float64')
    # print(df.info())
    
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)
    # print(df.head())

    X = np.array(df.iloc[:, :])
    # X = X[~np.isnan(X).any(axis=1), :]
    # X.astype('float64')
    
    # for col in df.columns:
        # df[col] = df[col].astype('float64')
    # print(df.columns)

    # 2. Drop the labels column

    # 3. Normalise the data

    scaler = RobustScaler()
    scaler.fit(X)
    X = scaler.transform(X)

    return X