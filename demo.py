"""
demo.py
Spring 2022 PJW

Demonstrate a left join (merge).
"""

import csv
import json

#
#  Set up a function for reading files. Returns a list of dictionaries, one
#  for each row.
#

def read_file(filename):
    fh = open(filename)
    reader = csv.DictReader(fh)
    records = []
    for rec in reader:
        records.append( rec )
    fh.close()
    return records

#%%
#
#  Read the files of state names and populations. Also set up the name of the
#  output file
#

name_list = read_file('state_name.csv')
pop_list = read_file('state_pop.csv')

outfile = 'demo-merged.csv'

#%%
#
#  Print a couple of entries. Notice that everything is a string.
#

n = 3
print( f'\nName file information in first {n} records:' )
print( json.dumps(name_list[:n], indent=4) )

print( f'\nPopulation file information in {n} records:' )
print( json.dumps(pop_list[:n], indent=4) )

#%%
#
#  Now build a dictionary of name information with FIPS codes as keys.
#  Check for duplicate keys along the way (will happen for 00).
#

name_by_fips = {}

for rec in name_list:
    fips = rec['State']

    if fips == "36":
        print('\nFIPS 36 is:',rec,'\n')

    if fips in name_by_fips:
        print('Skipping record with duplicate code:', rec['State'],rec['Name'])
    else:
        name_by_fips[ fips ] = rec

print( '\nname_by_fips["36"]:' )
print( json.dumps( name_by_fips["36"], indent=4 ) )

#
#  Now delete the 00 entry since it's not a state and we don't want it later.
#

del name_by_fips["00"]

#%%
#
#  Build a dictionary of population information with FIPS codes as keys
#

pop_by_fips = {}

for rec in pop_list:
    fips = rec['STATEFP']
    pop_by_fips[ fips ] = rec

print( '\npop_by_fips["36"]:' )
print( json.dumps( pop_by_fips["36"], indent=4 ) )

#%%
#
#  Do a left join of the population data onto the name data. Walk
#  through the name data, look up the population information, and
#  then add it to the name dictionary. Make the population numeric
#  in the process.
#

for fips in name_by_fips.keys():

    name_rec = name_by_fips[fips]

    pop_rec = pop_by_fips[fips]

    name_rec['pop'] = float(pop_rec['pop'])

print( '\nname_by_fips["36"]:' )
print( json.dumps( name_by_fips["36"], indent=4 ) )

#%%
#
#  Print a couple of states
#

print( )
for fips in ['06','48','36']:
    print( f'name_by_fips["{fips}"]:', name_by_fips[fips] )

#%%
#
#  Aggregate the data by division
#

division_total = {}

for rec in name_by_fips.values():

    #  Get the division and population for this state

    div = rec['Division']
    pop = rec['pop']

    #  Add the population to the division's total

    if div in division_total:
        division_total[div] = division_total[div] + pop
    else:
        division_total[div] = pop

#%%
#
#  Compute each state's share in its division population
#

for rec in name_by_fips.values():

    #  Get the division total

    div = rec['Division']
    div_pop = division_total[div]

    #  Compute the percentage and add it to the state record

    pct = 100*rec['pop']/div_pop
    rec['percent'] = pct

#%%
#
#  Write out the merged data. First step is to get the list of fields
#  from one of the entries in the dictionary. Any will do so use New York,
#  which is FIPS 36.
#

fields = list( name_by_fips["36"].keys() )

#
#  Open the output file. The newline argument is needed to avoid extra
#  blank lines because DictWriter() adds them itself.

fh = open(outfile,'w',newline='')

#
#  Set up the writer object
#

writer = csv.DictWriter(fh,fields)

#
#  Write the field names to the first line
#

writer.writeheader()

#
#  Write the rest of the entries
#

for name_rec in name_by_fips.values():
    writer.writerow(name_rec)

fh.close()
print( f"\nwrote {outfile}")
