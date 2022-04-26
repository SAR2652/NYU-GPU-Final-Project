import sys, subprocess, json, socket, shutil
from utils import BagOfWordsGenerator
args = sys.argv

file_name = args[1]

bow_gen = BagOfWordsGenerator(file_name)

bow_gen.saveJSON()