from g_data import *

'''
Stats: Prints: 28, Finished: 26, Failed: 2
Stats: Total time: 11d 21h 42m 59s, Longest job: 5d 12h 41m 17s
Stats: Filament used: 628.09m
'''
x = "Stats: Prints: 28, Finished: 26, Failed: 2\nStats: Total time: 11d 21h 42m 59s, Longest job: 5d 12h 41m 17s\nStats: Filament used: 628.09m"

data_obj = g_data()
data_obj.parsedata(136,x)
for key in data_obj.stats:
	print(data_obj.stats[key])
