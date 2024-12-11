import pandas as pd
import os
import time

# path to the input directory
input_directory = os.getcwd()  # current working directory 
# path to the output file
output_file = ".csv"

def extract_pi_stacking(file_path,source):
    data = []
    in_pi_stacking_section = False

    with open(file_path,"r") as file:
        # extract only relevant part (from pi-Stacking to next **)
        for line in file:
            line = line.strip()
            if line.startswith("**pi-Stacking**"):
                in_pi_stacking_section = True
                continue
            elif line.startswith("**"):
                in_pi_stacking_section = False
                continue
            if in_pi_stacking_section and line.startswith("|"):
                # split lines based on delimiter
                columns = [col.strip() for col in line.split("|") if col.strip()]
                # extract the relevant columns
                "RESNR | RESTYPE | RESCHAIN | RESNR_LIG | RESTYPE_LIG | RESCHAIN_LIG | PROT_IDX_LIST | LIG_IDX_LIST | SOURCE "
                RESNR = columns[0]
                RESTYPE = columns[1]
                RESCHAIN = columns[2]
                RESNR_LIG = columns[3]
                RESTYPE_LIG = columns[4]
                RESCHAIN_LIG = columns[5]
                PROT_IDX_LIST = columns[6]
                LIG_IDX_LIST = columns[11]
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
        pi_stacking_data = extract_pi_stacking(file_path,file_name)
         # convert list of lists to dataframes
        df = pd.DataFrame(pi_stacking_data, columns=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","PROT_IDX_LIST","LIG_IDX_LIST","SOURCE"])
        # filter rows 
        df = df[~((df['RESNR'] == 'RESNR') & (df['RESTYPE'] == 'RESTYPE'))]
        # append the df to the list
        dfs.append(df)
        
# concatenate all df in the list
pi_stacking = pd.concat(dfs, ignore_index=True)
# add interaction type
pi_stacking["INTERACTION TYPE"] = "pi Stacking"
# remove unnecessary columns
pi_stacking.drop(columns=["RESNR","RESTYPE","RESNR_LIG","RESTYPE_LIG","PROT_IDX_LIST","LIG_IDX_LIST"],inplace=True)
# count occurences by each source & add as a new column; group by chain & reset index by count_by_source
pi_stacking["COUNT_by_source"] = pi_stacking.groupby(["RESCHAIN","RESCHAIN_LIG","INTERACTION TYPE","SOURCE"]).transform("size")
pi_s=pi_stacking.groupby(["RESCHAIN","RESCHAIN_LIG","INTERACTION TYPE","SOURCE"]).size().reset_index(name="COUNT_by_source")
# count overall occurences
pi_s["COUNT"] = pi_s.groupby(["RESCHAIN","RESCHAIN_LIG","INTERACTION TYPE"]).transform("size")
# source + number of occurences = sources => add as a new column
pi_s["SOURCES"] = pi_s["SOURCE"] + ": " + pi_s["COUNT_by_source"].astype(str)
# join/merge duplicate sources
p_s = pi_s.groupby(["RESCHAIN","RESCHAIN_LIG","INTERACTION TYPE","COUNT"])["SOURCES"].apply(lambda x: "|".join(x)).reset_index()
# make unique list of sources
p_s['SOURCES'] = p_s['SOURCES'].apply(lambda x: '|'.join(set(x.split('|'))))
# calculate percentage and add result as a new column
p_s["PERCENT %"] = (p_s["COUNT"] * 100) / 1002
# write output to a csv file
p_s.to_csv(output_file,index=False)

# calculate execution time
execution_time = time.time() - start_time

print("Execution time:", execution_time, "seconds")