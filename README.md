# parsedate

parsedate.py is a Python module to process various human input dates or date ranges into a uniformed format. 

Developed for a [code4lib mailing list request](https://lists.clir.org/cgi-bin/wa?A2=ind1710&L=CODE4LIB&P=R24263&1=CODE4LIB&9=A&I=-3&J=on&d=No+Match%3BMatch%3BMatches&z=4).

## What is possible?

Take a look at the original data in [testData.csv](testData.csv). After processing, it becomes [Processed_testData.csv](Processed_testData.csv). 

You can also change the date delimiter and date range delimiter in the output to anything you want when you use the module.

input | output
--- | ---
1947 | 1947
August 1947 | 1947-08
August 3, 1947 | 1947-08-03
August 3-7, 1947 | 1947-08-03/1947-08-07
July 24, 1914 - January 30, 1915 | 1914-07-24/1915-01-30
May 23, 1957-June 20, 1957 | 1957-05-23/1957-06-20
1947 (August) | 1947-08
1947 (August 3) | 1947-08-03
1947 (August 3-7) | 1947-08-03/1947-08-07
May 14 (?) | ERROR
1917? | 1917
May 14, ____ | ERROR
ca. 1947 | 1947
ca. 1971-1972 | 1971/1972
ca. 1980s | 1980/1989
circa 1947 | 1947
circa 1939-1940 | 1939/1940
1944 (April - May) | 1944-04/1944-05
1939 (November) - 1940 (August) | 1939-11/1940-08
1955 (Jan.-June) | 1955-01/1955-06
1939 (November 6) - 1940 (August 7) | 1939-11-16/1940-08-07
June-December 1983 | 1983-06/1983-12
August 24 1988; October 31, 1988 | 1988-08-24/1988-10-31
Winter 1985-1986 | 1985/1986
1986- | 1986
through 1983 | ERROR
thru 198 | ERROR 
1933, 1937-1938, 1941 | 1933/1941
1897, 1906 | 1897/1906
pre-1975 | ERROR
pre-1975 (May) | ERROR
1965-1975, n.d. | 1965/1975
undated | 
n.d. | 
1932, 1940s-1975, n.d. | 1932/1975
1960s | 1960/1969
1930s-1950s | 1930/1959
1954 and undated | 1954
5/9/1970 | 1970-05-09
Saturday, 9 May 1970 | 1970-05-09
20 Jan 1973 | 1973-01-20
1944-1950 [died Aug. 1949] | ERROR
1967-onward | 1967
January 27, 1975 [1974?] | ERROR 
re: 1906 | 1906 
Easter 1961 | 1961
May 31, 1964-Fall 1965 | 1964-05-31/1965
June 2 - ____, 1971 | ERROR
n.d.; May 26, 1976 | 1976-05-26
May 1973 - Jul7 1973 | 1973-05/1973-07-07
May 1973-July 1973 | 1973-05/1973-07

## Installation

Download or clone this github repository.

## Usage

Save your orginal data file into the same folder as test.py and parsedate.py. The data file does not need to be a .csv, it could be a plain text file as long as each entry starts at a new line. 

In test.py, replace the input file name with the name of your data file, then run:

	python test.py

You can also change the date delimiter and date range delimiter to anything you want when using the parse() method.

