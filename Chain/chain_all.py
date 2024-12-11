import pandas as pd
import os
import time

# path to the input directory
input_directory = os.getcwd()  # current working directory ./
# path to the output file
output_file = ".csv"


# define a functions to extract interaction information
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


# store datas in a lists
dfs_hyd = []
dfs_hb = []
dfs_sb= []
dfs_pc= []
dfs_ps = []

# start time
start_time = time.time()

# iterate through each file in the input directory
for file_name in os.listdir(input_directory):
    if file_name.endswith(".txt"):
        file_path = os.path.join(input_directory, file_name)

        # hydrophobic 
        hydrophobic_int_data = extract_hydrophobic_int(file_path, file_name)
        df_hyd = pd.DataFrame(hydrophobic_int_data, columns=["RESNR", "RESTYPE", "RESCHAIN", "RESNR_LIG", "RESTYPE_LIG", "RESCHAIN_LIG", "LIGCARBONIDX", "PROTCARBONIDX", "SOURCE"])
        df_hyd = df_hyd[~((df_hyd['RESCHAIN'] == 'RESCHAIN') & (df_hyd['RESCHAIN_LIG'] == 'RESCHAIN_LIG'))]
        df_hyd = df_hyd[["RESCHAIN", "RESCHAIN_LIG", "SOURCE"]]
        dfs_hyd.append(df_hyd)

        # hydrogen
        hydrogen_bonds_data = extract_hydrogen_bonds(file_path,file_name)
        df_hb = pd.DataFrame(hydrogen_bonds_data, columns=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","DONORIDX", "ACCEPTORIDX","SOURCE"])
        df_hb = df_hb[~((df_hb['RESCHAIN'] == 'RESCHAIN') & (df_hb['RESCHAIN_LIG'] == 'RESCHAIN_LIG'))]
        df_hb = df_hb[["RESCHAIN", "RESCHAIN_LIG", "SOURCE"]]
        dfs_hb.append(df_hb)

        # salt bridge
        salt_bridges_data = extract_salt_bridges(file_path,file_name)
        df_sb = pd.DataFrame(salt_bridges_data, columns=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","PROT_IDX_LIST","LIG_IDX_LIST","SOURCE"])
        df_sb = df_sb[~((df_sb['RESCHAIN'] == 'RESCHAIN') & (df_sb['RESCHAIN_LIG'] == 'RESCHAIN_LIG'))]
        df_sb = df_sb[["RESCHAIN", "RESCHAIN_LIG", "SOURCE"]]
        dfs_sb.append(df_sb)

        # pi-Cation
        pi_cation_data = extract_pi_cation_int(file_path,file_name)
        df_pc = pd.DataFrame(pi_cation_data, columns=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","PROT_IDX_LIST","LIG_IDX_LIST","SOURCE"])
        df_pc = df_pc[~((df_pc['RESCHAIN'] == 'RESCHAIN') & (df_pc['RESCHAIN_LIG'] == 'RESCHAIN_LIG'))]
        df_pc = df_pc[["RESCHAIN", "RESCHAIN_LIG", "SOURCE"]]
        dfs_pc.append(df_pc)

        # pi stacking
        pi_stacking_data = extract_pi_stacking(file_path,file_name)
        df_ps = pd.DataFrame(pi_stacking_data, columns=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","PROT_IDX_LIST","LIG_IDX_LIST","SOURCE"])
        df_ps = df_ps[~((df_ps['RESCHAIN'] == 'RESCHAIN') & (df_ps['RESCHAIN_LIG'] == 'RESCHAIN_LIG'))]
        df_ps = df_ps[["RESCHAIN", "RESCHAIN_LIG", "SOURCE"]]
        dfs_ps.append(df_ps)

# concatenate interactions in their respective list
final_hydrophobic = pd.concat(dfs_hyd, ignore_index=True)
final_hydrogen = pd.concat(dfs_hb, ignore_index=True)
final_salt = pd.concat(dfs_sb, ignore_index=True)
final_pi_cation = pd.concat(dfs_pc, ignore_index=True)
final_pi_stacking = pd.concat(dfs_ps, ignore_index=True)

# concatenate interactions dfs
all_interactions = pd.concat([final_hydrophobic,final_hydrogen,final_salt,final_pi_cation,final_pi_stacking]).reset_index()

# count occurences by each source & add as a new column 
all_interactions["COUNT_by_source"] = all_interactions.groupby(["RESCHAIN","RESCHAIN_LIG","SOURCE"]).transform("size")

# group by chain & reset index by count_by_source
a_i=all_interactions.groupby(["RESCHAIN","RESCHAIN_LIG","SOURCE"]).size().reset_index(name='COUNT_by_source')

# count overall occurences
a_i["COUNT"] = a_i.groupby(["RESCHAIN","RESCHAIN_LIG"]).transform("size")

# source + number of occurences = sources => add as a new column
a_i['SOURCES'] = a_i['SOURCE'] + ': ' + a_i['COUNT_by_source'].astype(str)

# merge duplicate sources
final_a_i=a_i.groupby(["RESCHAIN","RESCHAIN_LIG","COUNT"])['SOURCES'].apply(lambda x: '|'.join(x)).reset_index()

# make unique list of sources and sort
final_a_i['SOURCES'] = final_a_i['SOURCES'].apply(lambda x: '|'.join(sorted(set(x.split('|')))))

# calculate percentage and add result as a new column
final_a_i["PERCENT %"] = (final_a_i["COUNT"] * 100) / 1002

# write output to a csv file
final_a_i.to_csv(output_file, index=False)

# calculate execution time
execution_time = time.time() - start_time

print("Execution time:", execution_time, "seconds")
