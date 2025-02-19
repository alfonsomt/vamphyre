#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        VAMPhyRE launcher
# Purpose:     Automate the pipeline for calculating Virtual Genomic Finger-
#              prints (VH5cmdl), counts the number of processing cores and 
#              creates a subprocess for each core, followed by parsing results
#              and calculation of a global table of hybridization (VHRP) and
#              comparison of fingerprints for calculation of distances/similarities.
#
# Author:      Mario Angel Lopez-Luis
#
# Created:     18/02/2025
# Copyright:   Alfonso Mendez-Tenorio 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.model_selection import train_test_split as TTS
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.metrics import roc_curve, auc, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.naive_bayes import GaussianNB as GNB
from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn.linear_model import LogisticRegression as LR 
from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.neural_network import MLPClassifier as NNW
import time
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import learning_curve
from sklearn.manifold import TSNE
import seaborn as sns
import argparse

parser = argparse.ArgumentParser()
print('minimal use:' + '\n' + 'ML_analysis_CVA.py -file vh_global.csv -meta metadatos.csv -clase Poblacion -RD PCA -T 8 -method MNB')

parser.add_argument('-f','--file', type = str, metavar = '', 
                    help = 'vh_global.csv file')

parser.add_argument('-m','--meta', type = str, metavar = '',
                    help = 'file.csv with metadata')
              
parser.add_argument('-l','--method', type = str, metavar = '', 
                    help = 'Machine LeArning Model [SVM],[SVM-PCA],[LR],[LR-PCA],[MNB],[GNB],[MLP], [DT] (default = MNB)',
                    default = 'MNB')

parser.add_argument('-c','--clase', type = str, metavar = '', 
                    help = 'Column name of class to classify')

parser.add_argument('-k','--fold',  metavar = '', type = int,
                    default = 1, help = 'K-fold (default = 10)')  
 
parser.add_argument('-lc','--l_curve', type = str, metavar = '',
                    help = 'Learning curve [yes/no]  (default = no)', default = 'no')

parser.add_argument('-d','--RD', metavar = '', type = str, 
                    help = 'Reduction dimension method PCA/tSNE/]', default = 'PCA')

parser.add_argument('-t','--T',  metavar = '', help = '# Threads (default = 1)', type = int,
                    default = 1)  

parser.add_argument('-s','--scale', type = str, metavar = '',
                    help = 'scale data [yes/no]  (default = no)', default = 'no')

parser.add_argument('-normalize', type = str, metavar = '',
                    help = 'normalize data [yes/no]  (default = no)', default = 'no')

var = parser.parse_args()

print("\n")
print('Opciones Selecionadas' +  "\n" +
      '##############################################################################')
print('Archivo Vamphyre: ' + var.file + "\n" +
      'Archivo con los metadatos: ' + var.meta + "\n" +
      'Columna de metadatos: ' + var.clase + "\n"
      'var.method de reducción de dimension: ' + var.RD + "\n")
print('##############################################################################')


t = time.strftime('%I:%M:%S')
print('[%s] Leyendo archivos...' %t)
vh_global = pd.read_csv(var.file, index_col = 0)
clase = var.clase
datos = vh_global.T
datos = datos.iloc[0:, 0:]
data = datos.sort_index(ascending = True)
colnames = vh_global.iloc[0:, 0]
met = pd.read_csv(var.meta)
metadata = met.sort_values('ID')
Lista_son = list(vh_global.iloc[0:, 0])

t = time.strftime('%I:%M:%S')
print('[%s] Generando analisis de reduccion de dimension...' %t)
y = metadata[clase].values
le = LE()
y = le.fit_transform(y)
X = data.iloc[0:, 0:].values

if var.RD == 'PCA':
    rd = PCA(n_components = (len(le.classes_)))
elif var.RD == 'tSNE':
    rd = TSNE(n_components = len(le.classes_) , learning_rate = 'auto', init = 'random',
          perplexity = 30)
    
X_lda = rd.fit_transform(X, y)
x_lda = np.array(X_lda[0:,0:])

lda_data = pd.DataFrame(x_lda, 
                        columns = [('PC' + str(i + 1)) for i in range(len(le.classes_))],
                        index = metadata[clase].values)

lda_data.to_csv('%s_Red_Dim_data.csv' %var.RD)

joint_plot = sns.jointplot(data=lda_data, 
                           x = 'PC1', 
                           y = 'PC2', 
                           hue = lda_data.index)
                           
ax = joint_plot.ax_joint
handles, labels = ax.get_legend_handles_labels() 
ax.legend(handles, labels, title = var.clase)  
plt.savefig(var.RD + '_plot.png')
plt.close()

t = time.strftime('%I:%M:%S')
print('[%s] Inicia Machine Learnining...' %t)
X_train, X_test, y_train, y_test = TTS(X, y, train_size = 0.80,
                                       random_state = 0, 
                                       stratify = y)

if var.scale == 'yes':
    stc = StandardScaler()
    stc.fit(X)
    X_test = stc.transform(X_test)
    X_train = stc.transform(X_train)

if var.scale == 'yes':
    norm = MinMaxScaler(feature_range = (0, 1))
    X_test = norm.fit_transform(X_test)
    X_train = norm.fit_transform(X_train)

if var.method == 'SVM':
    clf =  make_pipeline(StandardScaler(),
                         SVC(probability = (True),max_iter = -1))

elif var.method == 'SVM-PCA':
    clf = make_pipeline(StandardScaler(),
                        PCA(n_components = 2), 
                              SVC(probability = (True),max_iter = -1))
elif var.method == 'LR':
    clf = make_pipeline(StandardScaler(), 
                              LR(max_iter = 5000))

elif var.method == 'LR-PCA':
    clf = make_pipeline(StandardScaler(),
                        PCA(n_components = 2), 
                              LR(max_iter = 50))

elif var.method == 'MNB':
    clf = MNB()

elif var.method == 'GNB':
    clf = GNB()

elif var.method == 'MLP':
    clf = NNW(hidden_layer_sizes = (500,), max_iter = 1000)

elif var.method == 'RF':
    clf = RF(n_estimators = 1000)
    
elif var.method == 'DT':
    clf = DTC(criterion = 'entropy', max_depth = 9, 
              max_leaf_nodes = 20,
              min_impurity_decrease = 0.0001)
    

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
lr_ef = clf.score(X_test, y_test)
print('%s_base_ef = ' %var.method, lr_ef)

t =time.strftime('%I:%M:%S')
print('[%s] Obteniendo eficiencia de la validadcion...' %t)
######Validacion cruzada anidada
scores = cross_val_score(clf, X_train, y_train,
                         scoring = 'roc_auc_ovr',
                         cv = 10, 
                         n_jobs = var.T)

print('CVA accuracy: %.3f +/- %.3f' % (np.mean(scores),
                                      np.std(scores)))

conf_matrix = confusion_matrix(y_test, y_pred)
print('Confusion matrix: \n')
print(conf_matrix)
print('\n')

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average = 'macro')
recall = recall_score(y_test, y_pred, average = 'macro')
f1 = f1_score(y_test, y_pred, average = 'macro')

print('Accuracy:', accuracy)
print('Precision:', precision)
print('Recall:', recall)
print('F1 Score:', f1)

t = time.strftime('%I:%M:%S')
print('[%s] Graficando Curva ROC...' %t)

y_pred_proba = clf.predict_proba(X_test)
plt.figure(figsize = (8, 6))
mean_fpr = np.linspace(0, 1, 100)
mean_tpr = np.zeros_like(mean_fpr)

for i in range(len(clf.classes_)):
    fpr, tpr, _ = roc_curve(y_test == clf.classes_[i], y_pred_proba[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, lw=2,
             label=f'ROC curve ({le.inverse_transform([i])[0]}) (AUC = {roc_auc:.2f})')

    mean_tpr += np.interp(mean_fpr, fpr, tpr)

mean_tpr /= len(clf.classes_)
mean_auc = auc(mean_fpr, mean_tpr)
plt.plot(mean_fpr, mean_tpr, color='b', 
         linestyle='--', lw = 2,
         label=f'Mean ROC (AUC = {mean_auc:.2f})')

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate (FPR)')
plt.ylabel('True Positive Rate (TPR)')
plt.title('ROC_%s' %var.method)
plt.legend(loc='best')
plt.savefig('ROC_AUC_%s' %var.method + '.png', dpi = 400)
plt.close()

if var.l_curve == 'yes':
    t = time.strftime('%I:%M:%S')
    print('[%s] Graficando curva de aprendizaje...' %t)
    train_sizes, train_scores, test_scores = learning_curve(estimator = clf,
                                   X = X,
                                   y = y,
                                   train_sizes = np.linspace(0.1, 1.0, 10),
                                   cv = var.fold,
                                   n_jobs = var.T)

    train_mean = np.mean(train_scores, axis = 1)
    train_std = np.std(train_scores, axis = 1)
    test_mean = np.mean(test_scores, axis = 1)
    test_std = np.std(test_scores, axis = 1)

    plt.plot(train_sizes, train_mean,
             color = 'blue', marker = 'o',
             markersize = 6, label = 'training accuracy')

    plt.fill_between(train_sizes,
                     train_mean + train_std,
                     train_mean - train_std,
                     alpha = 0.15, color = 'blue')

    plt.plot(train_sizes, test_mean,
             color = 'green', linestyle = '--',
             marker ='s', markersize = 5,
             label ='validation accuracy')

    plt.fill_between(train_sizes,
                     test_mean + test_std,
                     test_mean - test_std,
                     alpha = 0.15, color = 'green')

    plt.grid()
    plt.xlabel('Number of training samples')
    plt.ylabel('Accuracy')
    plt.legend(loc = 'lower right')
    plt.tight_layout()
    plt.savefig('learning_curve_%s' %var.method + '.png', dpi = 1080)
    plt.show()
    plt.close()

if var.method == 'GNB':
    t = time.strftime('%I:%M:%S')
    print('[%s] escribiendo tabla de varianza...' %t)
    gnb = GNB(var_smoothing = 1e-20)
    gnb.fit(X, y)
    prob = pd.DataFrame(gnb.var_, index = le.classes_).transpose()
    prob['sonda'] = X.columns
    prob.to_csv('matriz_var_%s.csv' %var.method, index = None)

elif var.method == 'MNB':
    t = time.strftime('%I:%M:%S')
    print('[%s] escribiendo tabla de probabilidades...' %t)
    mnb = MNB(alpha = 1e-6)
    mnb.fit(X, y)
    prob = pd.DataFrame(mnb.feature_log_prob_, index = le.classes_).transpose()
    prob['sonda'] = data.columns
    prob.to_csv('matriz_prob_%s.csv' %var.method, index = None)


print('Analisis finalizado' + "\n")
print('Amsiedad⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
print('⠀⠀⠀⠀⠀⠀⠀⠀⡴⢻⣦⡲⠤⡀⠹⡋⢷⡇⣿⡷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
print('⠀⠀⠀⠀⠀⠀⠀⢼⢠⣿⡟⠃⢀⣠⡄⠱⠀⣿⣿⠛⢻⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
print('⠀⠀⠀⠀⠀⠀⠠⣿⣿⣛⡀⠚⠟⠛⠁⠀⠀⠙⠈⣧⣰⣽⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
print('⠀⠀⠀⠀⠀⣠⣾⣿⡟⠏⠀⠀⠀⠀⠀⠀⡀⠀⣸⡟⢃⠼⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
print('⠀⠀⠀⠀⢰⣿⣿⡿⢆⣀⢠⡶⠀⠀⠀⣠⠆⠐⠁⠀⠃⢀⣼⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀')
print('⠀⠀⠀⠀⠀⠈⠛⠳⡾⡾⠛⠀⠀⠀⡎⠁⠀⠀⠀⡀⠀⠈⠁⠀⠳⡀⠀⠀⠀⠀⠀⠀⠀')
print('⠀⠀⠀⠀⠀⠀⠀⠀⢹⠀⠀⠀⠀⠀⢣⡀⠀⣠⠖⠁⠀⠀⠀⠀⢠⡟⢦⡀⠀⠀⠀⠀⠀')
print('⠀⠀⠀⠀⠀⠀⠀⠀⢸⡀⠀⠀⠀⠀⠈⠣⠊⠁⠀⠀⠀⠀⠀⢠⠟⠇⢀⣿⣄⠀⠀⠀⠀')
print('⠀⠀⠀⠀⠀⠀⠀⠀⡾⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠴⠀⠃⠀⠀⠀⢼⡏⠘⢇⠀⠀⠀')
print('⠀⠀⠀⠀⠀⠀⠀⢠⣇⡀⠀⠀⠀⠀⠀⢀⠤⠒⠁⠀⢀⡄⠀⠀⠀⢰⠊⠀⠀⣾⡄⠀⠀')
print('⠀⠀⠀⠀⠀⠀⠀⠸⡿⢤⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⡾⠂⠀⠀⠘⠉⠀⠀⣴⢻⢷⡀⠀')
print('⠀⠀⠀⠀⠀⠀⠀⠀⢿⠬⠑⠤⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⢀⠀⠀⠐⠃⢘⣿⣷⠀')
print('⠀⠀⠀⠀⠀⠀⠀⠀⣼⡇⠀⠀⠀⠀⠀⠀⠀⡘⠁⡀⠀⠀⠀⢠⡟⠀⠀⠀⠟⣈⣻⣿⡇')
print('⠀⠀⠀⠀⠀⠀⠀⠀⣻⡇⠀⠀⣸⡁⠀⠀⠀⢷⣸⠀⠀⠀⠀⣯⠀⣄⣫⣤⣺⣿⣿⡿⠀')
print('⠀⠀⠀⠀⠀⣀⠤⠚⣹⡂⠀⢰⣿⣿⣦⠤⠤⠾⡟⠀⠀⠀⣼⣿⣧⣿⣿⣿⣿⣿⠟⠁⠀')
print('⢀⣠⠒⠋⠉⢁⣠⠴⣻⠁⢠⣼⠛⠁⠀⠀⠀⠀⣷⠀⠀⢠⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀')
print('⠈⠛⠛⠒⠉⠉⣀⢤⠃⢀⣿⠷⠴⠤⣄⣀⡀⠀⡿⠀⢀⣾⣿⣿⣿⠿⠛⠁⠀⠀⠀⠀⠀')
print('⠀⠀⣠⠤⠒⠉⡠⠃⠀⢨⠏⠀⠀⠀⠀⠀⠉⠉⡇⠀⢸⡟⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀')
print('⠀⠈⠛⠧⣶⠟⢠⠀⣠⠋⠀⠀⠀⠀⠀⠀⠀⢠⠇⠀⢸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
print('⠀⠀⠀⠀⠿⢴⡷⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⡞⠀⠀⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⡄⢀⡀⢸⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀')
print('⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⣇⣸⡥⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀')

