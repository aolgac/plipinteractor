import pandas as pd
import numpy as np

# path to input files and output file
simulation_1 = pd.read_csv(".csv")
simulation_2 = pd.read_csv(".csv")
simulation_3 = pd.read_csv(".csv")
simulation_4 = pd.read_csv(".csv")
output_file = ".csv"

# concatenate dfs
merged_hydrogen_bond = pd.concat([simulation_1,simulation_2,simulation_3,simulation_4]).reset_index().drop(columns=["index","COUNT"])
# count occurences & add it as a new column
merged_hydrogen_bond["REPEAT"]=merged_hydrogen_bond.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","DONORIDX","ACCEPTORIDX","INTERACTION TYPE"]).transform("size")
# combine percentages
merged_hydrogen_bond['PERCENT % LIST'] = merged_hydrogen_bond.groupby(["RESNR", "RESTYPE", "RESCHAIN", "RESNR_LIG", "RESTYPE_LIG", "RESCHAIN_LIG","DONORIDX","ACCEPTORIDX", "INTERACTION TYPE"])["PERCENT %"].transform(lambda x: "|".join(map(str, x)))
# remove duplicate rows
hydrogen_bonds_data=merged_hydrogen_bond.drop_duplicates()
# define function to convert string to list of floats & apply to df
def string_to_float_list(string):
    substrings = string.split("|")
    float_list = [float(substring) for substring in substrings]
    return float_list
hydrogen_bonds_data['PERCENT % LIST'] = hydrogen_bonds_data['PERCENT % LIST'].apply(string_to_float_list)
# calculate mean & standard deviation
hydrogen_bonds_data["MEAN"] = hydrogen_bonds_data["PERCENT % LIST"].apply(lambda x: np.mean(x))
hydrogen_bonds_data["STD_DEV"] = hydrogen_bonds_data["PERCENT % LIST"].apply(lambda x: np.std(x))
# remove duplicates & unnecessary columns
final_hydrogen_bonds_data = hydrogen_bonds_data.drop(columns="PERCENT %")
final_hydrogen_bonds_data.drop_duplicates(subset=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","DONORIDX","ACCEPTORIDX"],keep="first",inplace=True)
# write output to csv file
final_hydrogen_bonds_data.to_csv(output_file,index=False)