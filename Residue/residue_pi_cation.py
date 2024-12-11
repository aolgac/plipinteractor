import pandas as pd
import os
import time

# path to the input directory
input_directory = os.getcwd()  # current working directory
# path to the output file
output_file = ".csv"

def extract_pi_cation_int(file_path,source):
    data = []
    in_pi_cation_section = False

    with open(file_path,"r") as file:
        # extract only relevant part (from pi-cation to next **)
        for line in file:
            line = line.strip()
            if line.startswith("**pi-Cation Interactions**"):
                in_pi_cation_section = True
                continue
            elif line.startswith("**"):
                in_pi_cation_section = False
                continue
            if in_pi_cation_section and line.startswith("|"):
                # split lines based on delimiter
                columns = [col.strip() for col in line.split("|") if col.strip()]
                # extract the relevant columns
                "RESNR | RESTYPE | RESCHAIN | RESNR_LIG | RESTYPE_LIG | RESCHAIN_LIG | PROT_IDX_LIST | LIG_IDX_LIST | SOURCE"
                RESNR = columns[0]
                RESTYPE = columns[1]
                RESCHAIN = columns[2]
                RESNR_LIG = columns[4]
                RESTYPE_LIG = columns[5]
                RESCHAIN_LIG = columns[6]
                PROT_IDX_LIST = columns[3]
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
        pi_cation_data = extract_pi_cation_int(file_path,file_name)
        # convert list of lists to dataframes
        df = pd.DataFrame(pi_cation_data, columns=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","PROT_IDX_LIST","LIG_IDX_LIST","SOURCE"])
        # filter rows 
        df = df[~((df['RESNR'] == 'RESNR') & (df['RESTYPE'] == 'RESTYPE'))]
        # append the df to the list
        dfs.append(df)
        
# concatenate all df in the list
pi_cation = pd.concat(dfs, ignore_index=True)
# add interaction type column
pi_cation["INTERACTION TYPE"] = "pi-Cation Interaction" 
# count occurences by each source & add as a new column; group by residue & reset index by count_by_source
pi_cation["COUNT_by_source"] = pi_cation.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","SOURCE"]).transform("size")
pi_c=pi_cation.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","INTERACTION TYPE",'SOURCE']).size().reset_index(name='COUNT_by_source')
# count overall occurences
pi_c["COUNT"] = pi_c.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG"]).transform("size")
# source + number of occurences = sources => add as a new column
pi_c['SOURCES'] = pi_c['SOURCE'] + ': ' + pi_c['COUNT_by_source'].astype(str)
# join/merge duplicate sources
p_c=pi_c.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","INTERACTION TYPE","COUNT"])['SOURCES'].apply(lambda x: '|'.join(x)).reset_index()
# make unique list of sources
p_c['SOURCES'] = p_c['SOURCES'].apply(lambda x: '|'.join(set(x.split('|'))))
# calculate percetage and add result as a new column
p_c["PERCENT %"] = (p_c["COUNT"] * 100) / 1002
# write output to a csv file
p_c.to_csv(output_file,index=False)

# calculate execution time
execution_time = time.time() - start_time

print("Execution time:", execution_time, "seconds")