import pandas as pd
import os
import time

# path to the input directory
input_directory = os.getcwd()  # current working directory
# path to the output file
output_file = ".csv"

def extract_salt_bridges(file_path,source):
    data = []
    in_salt_bridges_section = False

    with open(file_path,"r") as file:
        # extract only relevant part (from salt bridges to next **)
        for line in file:
            line = line.strip()
            if line.startswith("**Salt Bridges**"):
                in_salt_bridges_section = True
                continue
            elif line.startswith("**"):
                in_salt_bridges_section = False
                continue
            if in_salt_bridges_section and line.startswith("|"):
                # split lines based on delimiter
                columns = [col.strip() for col in line.split("|") if col.strip()]
                # extract teh relevant columns
                "RESNR | RESTYPE | RESCHAIN | RESNR_LIG | RESTYPE_LIG | RESCHAIN_LIG | PROT_IDX_LIST | LIG_IDX_LIST | SOURCE "
                RESNR = columns[0]
                RESTYPE = columns[1]
                RESCHAIN = columns[2]
                RESNR_LIG = columns[4]
                RESTYPE_LIG = columns[5]
                RESCHAIN_LIG = columns[6]
                PROT_IDX_LIST = columns[3]
                LIG_IDX_LIST = columns[10]
                # append data
                data.append([RESNR,RESTYPE,RESCHAIN,RESNR_LIG,RESTYPE_LIG,RESCHAIN_LIG,PROT_IDX_LIST,LIG_IDX_LIST,source])
    return data

# store data in a list
dfs = []

# start time
start_time = time.time()

# iterate through each file in the input directory
for file_name in os.listdir(input_directory):
    if file_name.endswith(".txt"):
        file_path = os.path.join(input_directory, file_name)
        salt_bridges_data = extract_salt_bridges(file_path,file_name)
        # convert list of lists to dataframes
        df = pd.DataFrame(salt_bridges_data, columns=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","PROT_IDX_LIST","LIG_IDX_LIST","SOURCE"])
        # filter rows 
        df = df[~((df['RESNR'] == 'RESNR') & (df['RESTYPE'] == 'RESTYPE'))]
        # append the df to the list
        dfs.append(df)
        
# concatenate all df in the list
salt_bridge = pd.concat(dfs, ignore_index=True)

# add interaction type column
salt_bridge["INTERACTION TYPE"] = "Salt Bridge"
# count occurences by each source & add as a new column; group by residue & reset index by count_by_source
salt_bridge["COUNT_by_source"] = salt_bridge.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","SOURCE"]).transform("size")
salt_b=salt_bridge.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","INTERACTION TYPE",'SOURCE']).size().reset_index(name='COUNT_by_source')
# count overall occurences
salt_b["COUNT"] = salt_b.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG"]).transform("size")
# source + number of occurences = sources => add as a new column
salt_b['SOURCES'] = salt_b['SOURCE'] + ': ' + salt_b['COUNT_by_source'].astype(str)
# join/merge duplicate sources
s_b=salt_b.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","INTERACTION TYPE","COUNT"])['SOURCES'].apply(lambda x: '|'.join(x)).reset_index()
# make unique list of sources
s_b['SOURCES'] = s_b['SOURCES'].apply(lambda x: '|'.join(set(x.split('|'))))
# calculate percetage and add result as a new column
s_b["PERCENT %"] = (s_b["COUNT"] * 100) / 1002
# write output to a csv file
s_b.to_csv(output_file,index=False)

# calculate execution time
execution_time = time.time() - start_time

print("Execution time:", execution_time, "seconds")