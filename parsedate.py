# Copyright 2017 Dan Lou
# github.io/fishbb

import re

"""
define varialbles used by methods
"""

"""
Date that will becomes "ERROR":
1. contains the word "through" or "thru", regardless of case
2. contains "____"
3. contains "pre-" or "pre"
4. contains square bracket
"""
errors = ['.*(\(\?\)|through|thru|\_\_\_\_|pre[-]*|\[.+\]).*']

"""
Date that will turn into blank field:
1. 'undated' and spaces
2. 'n.d.' and spaces
"""
blank = ['^\s*undated\s*$', '^\s*n\.d\.\s*$']


"""
Words that got removed from date string:
'n.d.', 'ca.', 'circa', 're:', 'winter', 'easter', 'fall', 'onward', 'undated', '?', '(', ')', '.'
"""

subs = '(.*)n\.d\.|ca\.|circa|re:|winter|easter|fall|onward|and|undated|\?|\(|\)|\.(.*)'


"""
Replace month word with month number: avoid using datetime in this simple script

"""
month = ['jan', 'feb', 'mar', 'apri', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']      
month_subs = []      
for m in month:
    pattern = '(.*)('+m+'[a-z]{0,6})(.*)'
    month_subs.append(pattern)  

"""
define help functions
"""

# save result to a file
def saveFile(file, list):
    text_file = open(file, 'w')
    for l in list:
        text_file.write(l+'\n')
    text_file.close()

# read result from a file
def readFile(csv_file):
	lines = []
	# the test file was in a format of "old date | expected output" and we just want the "old date" part
	with open(csv_file) as f:
	    lines = [x.split('|')[0] if '|' in x else x for x in f] 
	return lines
	
def single_parse(date):
    """
    process the single date and ensure month and day are in two digit format
    """
    s = [
        '\s*(\d{4}),\s*(\d{4})[^\d]*$', # year, year
        '\s*(\d{4})[^\d]+(\d{1,2})[^\d]+(\d{1,2})[^\d]*$', # year month day
        '\s*(\d{1,2})[^\d]+(\d{1,2})[^\d]+(\d{4})[^\d]*$', #month day year
        '\s*(\d{4})[^\d]+(\d{1,2})[^\d]*$', #year month
        '\s*(\d{1,2})[^\d]+(\d{4})[^\d]*$', #month year
        '\s*(\d{3})(\d{1})(s)[^\d]*$', # years
        '\s*(\d{4})[^\d]*$', # year
        ]    
    if re.match(s[0],date):
        date = re.sub(s[0], '\g<1>-\g<2>', date)  
        pass
    elif re.match(s[1],date):
        date = re.sub(s[1], '\g<1>/\g<2>/\g<3>', date) 
        pass       
    elif re.match(s[2],date):
        date = re.sub(s[2], '\g<3>/\g<1>/\g<2>', date)
        pass
    elif re.match(s[3],date):
        date = re.sub(s[3], '\g<1>/\g<2>', date)  
        pass
    elif re.match(s[4],date):
        date = re.sub(s[4], '\g<2>/\g<1>', date)   
        pass
    elif re.match(s[5],date):
        date = re.sub(s[5], '\g<1>\g<2>-\g<1>9', date)    
        pass   
    elif re.match(s[6],date):
        date = re.sub(s[6], '\g<1>', date)         
        pass    
    return two_digits_check(date.strip())  

def two_digits_check(date):
    """
    ensure month and day are in two digit format
    """
    if '/' in date:
        parts = filter(bool,date.split('/'))
        new = []
        for p in parts:
            if len(p)==1:
                p = '0' + p
            new.append(p)
        date = '/'.join(new)
    return date
    
def special_range(date_range): 
    """
    divvy up special range date cases. make sure month comes in front of day, and year comes in front of month
    1. year - year
    2. year month day - year month, vise versa
    3. year month - year month
    5. year - year month day, vise versa
    6. year - year month, vise versa
    """
    s = [
        '\s*(\d{1,2})[^\d]+(\d{1,2})[^\d]*\-[^\d]*(\d{1,2})[^\d]+(\d{4})[^\d]*$',
        '\s*(\d{4})[^\d]+(\d{1,2})[^\d]+(\d{1,2})[^\d]*\-[^\d]*(\d{1,2})[^\d]*$',
        '\s*(\d{4})[^\d]+(\d{1,2})[^\d]*\-[^\d]*(\d{1,2})[^\d]*$',
        '\s*(\d{1,2})[^\d]*\-[^\d]*(\d{1,2})[^\d]+(\d{4})[^\d]*$',
    ]
    if re.match(s[0],date_range):
        date_range = re.sub(s[0], '\g<4> \g<1> \g<2>-\g<4> \g<1> \g<3>', date_range)      
    elif re.match(s[1],date_range):
        date_range = re.sub(s[1], '\g<1> \g<2> \g<3>-\g<1> \g<2> \g<4>', date_range)       
    elif re.match(s[2],date_range):
        date_range = re.sub(s[2], '\g<1> \g<2>-\g<1> \g<3>', date_range)  
    elif re.match(s[3],date_range):
        date_range = re.sub(s[3], '\g<3> \g<1>-\g<3> \g<2>', date_range)          
    return date_range 
    
"""
define main functions
"""
        
def handle_error(dates):
    """
    Handle all the errors first. 
    """
    first_pass = []  
      
    for d in dates: 
        new = d.lower()
        new = new.strip()
        if re.match("|".join(errors), new): 
            new = 'ERROR'
        elif re.match("|".join(blank), new): 
            new = ''
        else:
            new = re.sub(subs, '\g<1> \g<2>', new)
            if re.match('[^\d]*(\d{1,2})\s+(['+'|'.join(month)+'][a-z]{0,6})\s+(\d{4}).*',new):
                new = re.sub('[^\d]*(\d{1,2})\s+(['+'|'.join(month)+'][a-z]{0,6})\s+(\d{4}).*','\g<3>/\g<2>/\g<1>', new)  
        first_pass.append(new)  
    return first_pass

def handle_month(dates):
    """
    Convert month to numbers and make sure month always come ahead of day
    """
    second_pass = []
    for new in dates:
        for m in month_subs:
            if re.match(m, new):
                month = str(month_subs.index(m)+1)
                if len(month)<2:
                    month = '0'+month
                new = re.sub(m, r'\g<1> '+month+r' \g<3>', new)   
        second_pass.append(new)
    return second_pass

def handle_range(dates):
    """
    handle date ranges, and ensure there is no extra punctuation in the final output. 
    """
    final = []

    for new in dates:
        new = new.strip()
        new = new.strip(';')
        new = new.strip('-')
        new = new.strip('/')
        if ';' in new:
            new = new.replace(';', '-')
        if new=='' or new == 'ERROR':
            final.append(new)        
        elif '-' in new:
            new = special_range(new)
            items = new.strip().split('-')  
            range = []
            f = ''
            for i in items:
                i = single_parse(i)     
                range.append(i)
            f = '-'.join(range)
            if f.count('-')>1:
                temp = f.split('-')
                f = temp[0]+'-'+temp[-1]
            final.append(f.strip()) 
        else:
            new = single_parse(new)
            final.append(new)
            
    return final

def reformat(entry, date_delimiter, range_delimiter):
    """
    reformat if need different date delimiter and range delimiter
    """
    new = entry
    if '-' in new:
        days = new.split('-')
        new_days = []
        for d in days:
            new_days.append(d.replace('/', date_delimiter))
        new = range_delimiter.join(new_days)            
    elif '/' in entry:
        new = entry.replace('/', date_delimiter)
    return new 

def parse(input_file, date_delimiter='/', range_delimiter='-'):
    '''
    main method.
    parameters: 
    input_file: input file name
    date_delimiter: date delimiter, default is /
    range_delimiter: date range delimiter, default is -
    '''
    dates = readFile(input_file)

#     dates = ['1947 (August)']
    
    temp = handle_range(handle_month(handle_error(dates)))
    
    result = []
    
    if date_delimiter is not '/' or range_delimiter is not '-':
        new_temp = [reformat(t, date_delimiter, range_delimiter) for t in temp]
        result = new_temp
    else:
        result = temp
    print(result)
    saveFile('Processed_'+input_file, result)
            
    
    
