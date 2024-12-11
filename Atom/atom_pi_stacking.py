import pandas as pd
import os
import time

# path to the input directory
input_directory = os.getcwd()  # current working directory
# path to the output file
output_file = ".csv"

def extract_pi_stacking(file_path):
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
                "RESNR | RESTYPE | RESCHAIN | RESNR_LIG | RESTYPE_LIG | RESCHAIN_LIG | PROT_IDX_LIST | LIG_IDX_LIST "
                RESNR = columns[0]
                RESTYPE = columns[1]
                RESCHAIN = columns[2]
                RESNR_LIG = columns[3]
                RESTYPE_LIG = columns[4]
                RESCHAIN_LIG = columns[5]
                PROT_IDX_LIST = columns[6]
                LIG_IDX_LIST = columns[11]
                # append data
                data.append([RESNR,RESTYPE,RESCHAIN,RESNR_LIG,RESTYPE_LIG,RESCHAIN_LIG,PROT_IDX_LIST,LIG_IDX_LIST])
    return data

# store data in a list
dfs = []

# start time
start_time = time.time()

# iterate through each file in the input directory
for file_name in os.listdir(input_directory):
    if file_name.endswith(".txt"):
        file_path = os.path.join(input_directory, file_name)
        pi_stacking_data = extract_pi_stacking(file_path)
        # convert list of lists to dataframes
        df = pd.DataFrame(pi_stacking_data, columns=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","PROT_IDX_LIST","LIG_IDX_LIST"])
        # filter rows 
        df = df[~((df['RESNR'] == 'RESNR') & (df['RESTYPE'] == 'RESTYPE'))]
        # append the df to the list
        dfs.append(df)
        
# concatenate all df in the list
pi_stacking = pd.concat(dfs, ignore_index=True)
# add interaction type column
pi_stacking["INTERACTION TYPE"] = "pi-Stacking"
# count overall occurences
pi_stacking["COUNT"] = pi_stacking.groupby(["PROT_IDX_LIST","LIG_IDX_LIST"]).transform("size")
# calculate percetage and add result as a new column
pi_stacking["PERCENT %"] = (pi_stacking["COUNT"] * 100) / 1002
# drop duplicates
drop_pi_stacking = pi_stacking.drop_duplicates(keep="first").reset_index(drop=True)
# write output to a csv file
drop_pi_stacking.to_csv(output_file,index=False)

# calculate execution time
execution_time = time.time() - start_time

print("Execution time:", execution_time, "seconds")