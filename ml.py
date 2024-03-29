#!/usr/bin/env python
# encoding: utf-8

### general machine learning quick check using gradient boosting. 
### supports classification/regression, validation, lasso, etc. 
### notice, importance always come from full model using all data. (CV is irrelevant here) 
### notice, by default input ml needs to have rownames in the first column, header can have 1 fewer fields

import numpy as np



## import args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='inFile', help='input tsv file with Xs (featuers) and Y (label); needs a header; needs first column as rownames')
parser.add_argument('-l', dest='label', help='columnName in the header used as the label column.')
parser.add_argument('-m', dest='mode', default="classification", help='regression or classification.')
parser.add_argument('-n', dest='cvFold', default=0, help='number of CV fold; use 0 if no CV is needed. Default:0')
parser.add_argument('-t', dest='ntree', default=100 , help='number of trees. Default:100')
parser.add_argument('-p', dest='ncpu', default=-1 , help='number of CPU process. Default:1')
parser.add_argument('-I', dest='impFile', default="impFile.tsv" , help='output importance file. Default: impFile.tsv')
parser.add_argument('-P', dest='predFile', default="predFile.tsv" , help='output Y-pred file. Default: predFile.tsv')
parser.add_argument('-O', dest='plotFile', default="plotFile" , help='header name for the output AUC plot, only works for classification and when cvFold > 0! eg. -m classification -n 5 -O test. Default: plotFile')
parser.add_argument('-L', dest='lasso', default=False , help='use lasso, default to False; otherwise use a number for alpha: 0 to 1; 0 for an ordinary least square, 1 for conanical L1 lasso. Default: False')
parser.add_argument('-T', dest='transpose', action='store_true', default=False, help='transpose the data from using samples on the columns (and features/label on the rows) to samples on the rows(and features/label on the columns), Default=False')
parser.add_argument('-s', dest='use_scale', default=False, help='scale the features by z = (x-u) / s per row (sample), default = False')
args = parser.parse_args()

## check args
inFile = args.inFile
label = args.label
ntree = int(args.ntree)
ncpu = int(args.ncpu)
cvFold = int(args.cvFold)
mode = args.mode
impFile = args.impFile
predFile = args.predFile
plotFile = args.plotFile
lasso = float(args.lasso) if args.lasso else False
transpose = args.transpose
use_scale = True if args.use_scale else False

## default values
sep = "\t" # used to parse the inFile
header = 0 # use the first line as header
index_col = 0 # use the first column as the rowname
random_state = 0 # random state

## debug
#inFile = "data.more.tsv"
#label = "TMP"
#ntree = 100
#ncpu = -1
#cvFold = 5
#mode = "regression"
#impFile = "testImp.tsv"

## read inFile
import pandas as pd
df = pd.read_csv(inFile, header = header, sep = sep, index_col = index_col)
if transpose:
	df = df.transpose()
y = df[label]
fts = list(df.columns)
fts.remove(label)
X = df[fts]

## pre-processing
from sklearn.preprocessing import StandardScaler

def preproc(X):
	# z = (x-u)/s
	print("scaling X...")
	scaler = StandardScaler()
	X_scaled = scaler.fit_transform(X)
	X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
	return X_scaled_df

if use_scale:
	X = preproc(X)

## ML model
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
if mode == "classification":
	model = GradientBoostingClassifier(n_estimators = ntree, random_state=random_state, max_features="log2", max_depth=3)
else:
	model = GradientBoostingRegressor(n_estimators = ntree, random_state=random_state, max_features="log2", max_depth=3)

## performance eval
from numpy import mean, std
from sklearn.metrics import roc_auc_score, average_precision_score, explained_variance_score, r2_score, roc_curve,  precision_recall_curve
from scipy.stats import spearmanr

## lasso
from sklearn.linear_model import Lasso
# return lasso filtered freatures based on training set.
def go_lasso(X, y, alpha):
	lassoFS = Lasso(alpha = alpha)
	lassoFS.fit(X, y)
	coefs = lassoFS.coef_
	fts_ids = [int(i) for i, coef in enumerate(coefs) if coef!=0]
	print(f"Lasso kept {len(fts_ids)} features")
	return fts_ids


# get performance
from sklearn.metrics import confusion_matrix
def get_performance(y, predp, threshold=0.5, mode="classification"):
	if mode.upper().startswith("C"):
		# Apply the threshold to get predicted classes
		pred = (predp > threshold).astype(int)
		# Calculate the confusion matrix
		tn, fp, fn, tp = confusion_matrix(y, pred).ravel()
		# Sensitivity (True Positive Rate)
		sensitivity = tp / (tp + fn) if (tp + fn) != 0 else 0
		# Specificity (True Negative Rate)
		specificity = tn / (tn + fp) if (tn + fp) != 0 else 0
		# AUC-ROC and AUC-PRC scores
		auROC = roc_auc_score(y, predp)
		auPRC = average_precision_score(y, predp)
		# Return the list of performance metrics
		performance_list = [sensitivity, specificity, auPRC, auROC]
		return performance_list

## main

## for plotting
import matplotlib.pyplot as plt

## has CV
if cvFold > 0:
	from sklearn.model_selection import KFold
	kf = KFold(n_splits=cvFold, random_state=random_state, shuffle=True)
	kf.get_n_splits(X)
	s1s, s2s, s3s, s4s = [], [], [], []
	preds, Ys = [], []
	fold = 0
	print("Fold\tSens\tSpec\tauROC\tauPRC")
	for train_index, test_index in kf.split(X):
		fold += 1
		X_train, X_test = X.iloc[train_index,:], X.iloc[test_index,:]
		y_train, y_test = y.iloc[train_index], y.iloc[test_index]
		if lasso:
			fts_ids = go_lasso(X_train, y_train, alpha = lasso)
			X_train = X_train.iloc[:,fts_ids]
			X_test = X_test.iloc[:,fts_ids]
		model.fit(X_train, y_train)
		pred = model.predict(X_test)
		if mode == "classification" or "c" or "C":
			predp = model.predict_proba(X_test)[:,1]
			sensitivity, specificity, auPRC, auROC = get_performance(y_test, predp)
			## for plot
			# ROC
			plt.figure(1)
			fpr, tpr, _ = roc_curve(y_test, predp)
			plt.plot(fpr, tpr, label= "fold :" + str(fold))
			# PRC
			plt.figure(2)
			precision, recall, _ = precision_recall_curve(y_test, predp)
			plt.plot(recall, precision,	label = "fold :" + str(fold))
			## for score
			print("{0:d}\t{1:.3f}\t{2:.3f}\t{3:.3f}\t{4:.3f}".format(fold, sensitivity, specificity, auROC, auPRC))
			s1s.append(sensitivity)
			s2s.append(specificity)
			s3s.append(auROC)
			s4s.append(auPRC)
		else:
			r2 = r2_score(y_test, pred)
			varExp = explained_variance_score(y_test, pred)
			print("r2\t{}\tvarExp\t{}".format(r2, varExp))
			s1s.append(r2)
			s2s.append(varExp)
		# for predFile
		preds += list(pred)
		Ys += list(y_test)
	print("Avg:\t{}\t{}\t{}\t{}".format(round(mean(s1s),3), round(mean(s2s),3), round(mean(s3s),3), round(mean(s4s),3)))

	if mode in ["classification", "c", "C"]:
		## plotting: ROC curve
		plt.figure(1)
		plt.xlim([-0.05,1.05])
		plt.ylim([-0.05,1.05])
		plt.xlabel('False Positive Rate')
		plt.ylabel('True Positive Rate')
		plt.legend()
		plt.savefig(plotFile + ".ROC.pdf")
		## plotting: PRC curve
		plt.figure(2)
		plt.xlim([-0.05,1.05])
		plt.ylim([-0.05,1.05])
		plt.xlabel('Precision')
		plt.ylabel('Recall')
		plt.legend()
		plt.savefig(plotFile + ".PRC.pdf")


## no CV; regardless, full model is computed, imp should come from here. 
if lasso:
	fts_ids = go_lasso(X, y, alpha = lasso)
	X = X.iloc[:,fts_ids]
	fts = [fts[fts_id] for fts_id in fts_ids]
modelFull = model
modelFull.fit(X, y)
predFull = modelFull.predict(X)
## importance
## print imp
def getImp(model, fts):
	lines = []
	for i, e in enumerate(sorted(list(zip(model.feature_importances_, fts)), reverse=True)):
		line = "\t".join(map(str,e))
		lines.append(line)
	return "\n".join(lines)
## write imp
with open(impFile, "w") as f:
	f.write(getImp(modelFull, fts))

## otherwise print full model performance.
if cvFold <= 0:
	if mode in ["classification", "c", "C"]:
		predp = modelFull.predict_proba(X)[:,1]
		sensitivity, specificity, auPRC, auROC = get_performance(y, predp)
		print("Sens\tSpec\tauROC\tauPRC")
		print("{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}".format(sensitivity, specificity, auROC, auPRC))
	else:
		r2 = r2_score(y, predFull)
		varExp = explained_variance_score(y, predFull)
		print("r2\t{}\tvarExp\t{}".format(r2, varExp))
	# for predFile
	Ys = y
	preds = predFull

## pred-Y
with open(predFile, "w") as f:
	f.write("\n".join(["{}\t{}".format(pair[0], pair[1]) for pair in zip(Ys, preds)]))

