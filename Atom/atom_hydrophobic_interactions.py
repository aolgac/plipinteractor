import pandas as pd
import os
import time

# path to the input directory
input_directory = os.getcwd()  # current working directory
# path to the output file
output_file = ".csv"

def extract_hydrophobic_int(file_path):
    data = []
    in_hydrophobic_int_section = False

    with open(file_path,"r") as file:
        # extract only relevant part (from hydrophobic int to next **)
        for line in file:
            line = line.strip()
            if line.startswith("**Hydrophobic Interactions"):
                in_hydrophobic_int_section = True
                continue
            elif line.startswith("**"):
                in_hydrophobic_int_section = False
                continue
            if in_hydrophobic_int_section and line.startswith("|"):
                # split lines based on delimiter
                columns = [col.strip() for col in line.split("|") if col.strip()]
                # extract teh relevant columns
                "RESNR | RESTYPE | RESCHAIN | RESNR_LIG | RESTYPE_LIG | RESCHAIN_LIG | LIGCARBONIDX | PROTCARBONIDX "
                RESNR = columns[0]
                RESTYPE = columns[1]
                RESCHAIN = columns[2]
                RESNR_LIG = columns[3]
                RESTYPE_LIG = columns[4]
                RESCHAIN_LIG = columns[5]
                LIGCARBONIDX = columns[7]
                PROTCARBONIDX = columns[8]
                # append data
                data.append([RESNR,RESTYPE,RESCHAIN,RESNR_LIG,RESTYPE_LIG,RESCHAIN_LIG,LIGCARBONIDX,PROTCARBONIDX])
    return data

# store data in a list
dfs = []

# start time
start_time = time.time()

# iterate through each file in the input directory
for file_name in os.listdir(input_directory):
    if file_name.endswith(".txt"):
        file_path = os.path.join(input_directory, file_name)
        hydrophobic_int_data = extract_hydrophobic_int(file_path)
        # convert list of lists to dataframes
        df = pd.DataFrame(hydrophobic_int_data, columns=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","LIGCARBONIDX","PROTCARBONIDX"])            
        # filter rows
        df = df[~((df['LIGCARBONIDX'] == 'LIGCARBONIDX') & (df['PROTCARBONIDX'] == 'PROTCARBONIDX'))]
        # append the df to the list
        dfs.append(df)
        
# concatenate all df in the list
hydrophobic_int = pd.concat(dfs, ignore_index=True)
# add new column that shows interaction type
hydrophobic_int["INTERACTION TYPE"] = "Hydrophobic Interaction"
# calculate occurence count
hydrophobic_int['COUNT'] = hydrophobic_int.groupby(['LIGCARBONIDX', 'PROTCARBONIDX']).transform('size')
# find percentage
hydrophobic_int["PERCENT %"] = (hydrophobic_int["COUNT"] * 100) / 1002
# drop duplicates 
drop_hydrophobic_int = hydrophobic_int.drop_duplicates(keep="first").reset_index(drop=True)
# save output to a csv file 
drop_hydrophobic_int.to_csv(output_file, index=False)

# calculate execution time
execution_time = time.time() - start_time

print("Execution time:", execution_time, "seconds")