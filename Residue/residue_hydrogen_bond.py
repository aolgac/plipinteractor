import os
import pandas as pd
import time

# path to the input directory
input_directory = os.getcwd()  # current working directory ./
# path to the output file
output_file = ".csv"

# define a function to extract hydrogen bonds info
def extract_hydrogen_bonds(file_path,source):
    # store data in a list
    data = []
    in_hydrogen_bonds_section = False

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # extract only relevant part (from hydrogen bond to next **)
            if line.startswith("**Hydrogen Bonds**"):
                in_hydrogen_bonds_section = True
                continue
            elif line.startswith("**"):
                in_hydrogen_bonds_section = False
                continue

            if in_hydrogen_bonds_section and line.startswith("|"):
                # split the line into columns based on the delimiter "|"
                columns = [col.strip() for col in line.split("|") if col.strip()]
                # extract the relevant columns
                "| RESNR | RESTYPE | RESCHAIN | RESNR_LIG | RESTYPE_LIG | RESCHAIN_LIG | DONORIDX | ACCEPTORIDX | SOURCE "
                RESNR = columns[0]
                RESTYPE = columns[1]
                RESCHAIN = columns[2]
                RESNR_LIG = columns[3]
                RESTYPE_LIG = columns[4]
                RESCHAIN_LIG = columns[5]
                DONORIDX = columns[11]
                ACCEPTORIDX = columns[13]
                # append the extracted data to the list
                # use source parameter to see origin of data
                data.append([RESNR,RESTYPE,RESCHAIN,RESNR_LIG,RESTYPE_LIG,RESCHAIN_LIG,DONORIDX, ACCEPTORIDX, source])

    return data

# store data in a list
dfs = []

# start time
start_time = time.time()

# iterate through each file in the input directory
for file_name in os.listdir(input_directory):
    if file_name.endswith(".txt"):
        file_path = os.path.join(input_directory, file_name)
        hydrogen_bonds_data = extract_hydrogen_bonds(file_path,file_name)
        # convert list of lists to dataframes
        df = pd.DataFrame(hydrogen_bonds_data, columns=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","DONORIDX", "ACCEPTORIDX","SOURCE"])
        # filter rows 
        df = df[~((df['DONORIDX'] == 'DONORIDX') & (df['ACCEPTORIDX'] == 'ACCEPTORIDX'))]
        # append the df to the list
        dfs.append(df)

# concatenate all df in the list
hydrogen_bond = pd.concat(dfs, ignore_index=True)
# add interaction type column
hydrogen_bond["INTERACTION TYPE"] = "Hydrogen Bond"
# count occurences by each source & add as a new column; group by residue & reset index by count_by_source
hydrogen_bond["COUNT_by_source"] = hydrogen_bond.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","SOURCE"]).transform("size")
hydrogen_b=hydrogen_bond.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","INTERACTION TYPE",'SOURCE']).size().reset_index(name='COUNT_by_source')
# count overall occurences
hydrogen_b["COUNT"] = hydrogen_b.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG"]).transform("size")
# source + number of occurences = sources => add as a new column
hydrogen_b['SOURCES'] = hydrogen_b['SOURCE'] + ': ' + hydrogen_b['COUNT_by_source'].astype(str)
# join/merge duplicate sources
h_b=hydrogen_b.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","INTERACTION TYPE","COUNT"])['SOURCES'].apply(lambda x: '|'.join(x)).reset_index()
# make unique list of sources
h_b['SOURCES'] = h_b['SOURCES'].apply(lambda x: '|'.join(set(x.split('|'))))
# calculate percetage and add result as a new column
h_b["PERCENT %"] = (h_b["COUNT"] * 100) / 1002
# write output to a csv file
h_b.to_csv(output_file,index=False)

# calculate execution time
execution_time = time.time() - start_time

print("Execution time:", execution_time, "seconds")