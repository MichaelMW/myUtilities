#!/usr/bin/env python
# encoding: utf-8

from textgenrnn.textgenrnn import textgenrnn
import os.path
from os import path
import sys


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', dest='inFile', help='Input file for training. Each line is one training sample. eg. a column of names. Note: providing an inFile implies de novo training')
parser.add_argument('-m', dest='model', default="rnnModel", help='Name (prefix) for the model to load/save.')
parser.add_argument('-t', dest='temp', default=0.5, help='temperature: 0 to 1, higher temperature generates more random outputs.')
parser.add_argument('-n', dest='ngen', default=10, help='number of samples to generate.')
parser.add_argument('-b', dest='batch', default = 128, help='Number of batches. Default:128, higher numbers enables more training data.')
parser.add_argument('-e', dest='epoch', default = 1, help='Number of epoch. Default:1, higher numbers enables more hyperparameter tweaking of the model')

## parse and check args
args = parser.parse_args()
inFile = args.inFile
if inFile:
	inFileExist = True if path.exists(inFile) else False
else:
	inFileExist = False
model = args.model
model_voc = model + "_vocab.json"
model_conf = model + "_config.json"
model_weigths = model + "_weights.hdf5"
modelExist = True if (path.exists(model_voc) and path.exists(model_conf) and path.exists(model_weigths)) else False
temp = float(args.temp)
ngen = int(args.ngen)
batch = int(args.batch)
epoch = int(args.epoch)


### main ###

## train a new model
if inFileExist and not modelExist:
	sys.stderr.write("train a new model from inFile:{} -> model:{}\n".format(inFile, model))
	textgen = textgenrnn(name = model)
	textgen.reset()
	textgen.train_from_file(inFile, batch_size = batch, num_epochs = epoch, new_model = True)

## grow an existing model
## this actually generate this model: textgenrnn_weights.hdf5 why?
elif inFileExist and modelExist:
	sys.stderr.write("grow an existing model from inFile:{} -> model:{}\n".format(inFile, model))
	textgen =  textgenrnn(name = model,
							weights_path = model_weigths,
							vocab_path = model_voc,
							config_path = model_conf)
	textgen.train_from_file(inFile, batch_size = batch, num_epochs = epoch, new_model = False)

## load model for prediction
elif not inFileExist and modelExist:
	sys.stderr.write("load model for prediction model:{}\n".format(model))
	textgen =  textgenrnn(weights_path = model_weigths,
							vocab_path = model_voc,
							config_path = model_conf)
	genList = textgen.generate(ngen, return_as_list = True, temperature = temp)
	for gen in genList:
		print(gen)

## otherwise error
else:
	sys.stderr.write("Need at least a valide inFile:{} or model:{}\n".format(inFile, model))
	exit()
