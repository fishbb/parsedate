from parsedate import parse

"""
parameters: 
input file name
date delimiter: default is /. In the following example, change it to -
date range delimiter: default is -. In the following example, change it to /
"""

parse('testData.csv', '-', '/')  
