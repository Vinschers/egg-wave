import numpy as np
import pandas as pd

def funcao(param):
	if param == 'NEGATIVE':
		return -1
	elif param == 'NEUTRAL':
		return 0
	elif param == 'POSITIVE':
		return 1
	else:
		return param

df = pd.read_csv('emotions.csv')
df = df.applymap(funcao)
df.to_csv('emotions2.csv')