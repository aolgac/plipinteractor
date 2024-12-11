import pandas as pd
import os
import time

# path to the input directory
input_directory = os.getcwd()  # current working directory
# path to the output file
output_file = ".csv"


def extract_hydrophobic_int(file_path, source):
    data = []
    in_hydrophobic_int_section = False

    with open(file_path, "r") as file:
        # extract only relevant part (from hyd int to next **)
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
                # extract the relevant columns
                "| RESNR | RESTYPE | RESCHAIN | RESNR_LIG | RESTYPE_LIG | RESCHAIN_LIG | LIGCARBONIDX | PROTCARBONIDX | SOURCE"
                RESNR = columns[0]
                RESTYPE = columns[1]
                RESCHAIN = columns[2]
                RESNR_LIG = columns[3]
                RESTYPE_LIG = columns[4]
                RESCHAIN_LIG = columns[5]
                LIGCARBONIDX = columns[7]
                PROTCARBONIDX = columns[8]
                # append data
                # use source parameter to see origin of data
                data.append([RESNR, RESTYPE, RESCHAIN, RESNR_LIG, RESTYPE_LIG, RESCHAIN_LIG, LIGCARBONIDX, PROTCARBONIDX, source])
    return data

# store data in a list
dfs = []

# start time
start_time = time.time()

# iterate through each file in the input directory
for file_name in os.listdir(input_directory):
    if file_name.endswith(".txt"):
        file_path = os.path.join(input_directory, file_name)
        hydrophobic_int_data = extract_hydrophobic_int(file_path, file_name)
        # convert list of lists to df
        df = pd.DataFrame(hydrophobic_int_data, columns=["RESNR", "RESTYPE", "RESCHAIN", "RESNR_LIG", "RESTYPE_LIG", "RESCHAIN_LIG", "LIGCARBONIDX", "PROTCARBONIDX", "SOURCE"])
        # filter rows
        df = df[~((df['LIGCARBONIDX'] == 'LIGCARBONIDX') & (df['PROTCARBONIDX'] == 'PROTCARBONIDX'))]
        # append the df to the list
        dfs.append(df)

# concatenate all df in the list
hydrophobic_bond = pd.concat(dfs, ignore_index=True)
# add interaction type column
hydrophobic_bond["INTERACTION TYPE"] = "Hydrophobic Interaction"
# count occurences by each source & add as a new column; group by residue & reset index by count_by_source
hydrophobic_bond["COUNT_by_source"] = hydrophobic_bond.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","SOURCE"]).transform("size")
hydrophobic_b=hydrophobic_bond.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","INTERACTION TYPE",'SOURCE']).size().reset_index(name='COUNT_by_source')
# count overall occurences
hydrophobic_b["COUNT"] = hydrophobic_b.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG"]).transform("size")
# source + number of occurences = sources => add as a new column
hydrophobic_b['SOURCES'] = hydrophobic_b['SOURCE'] + ': ' + hydrophobic_b['COUNT_by_source'].astype(str)
# join/merge duplicate sources
hyd_b=hydrophobic_b.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","INTERACTION TYPE","COUNT"])['SOURCES'].apply(lambda x: '|'.join(x)).reset_index()
# make unique list of sources
hyd_b['SOURCES'] = hyd_b['SOURCES'].apply(lambda x: '|'.join(set(x.split('|'))))
# calculate percetage and add result as a new column
hyd_b["PERCENT %"] = (hyd_b["COUNT"] * 100) / 1002
# write output to a csv file
hyd_b.to_csv(output_file,index=False)

# calculate execution time
execution_time = time.time() - start_time

print("Execution time:", execution_time, "seconds")
