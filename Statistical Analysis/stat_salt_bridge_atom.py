import pandas as pd
import numpy as np

# path to input files and output file
simulation_1 = pd.read_csv(".csv")
simulation_2 = pd.read_csv(".csv")
simulation_3 = pd.read_csv(".csv")
simulation_4 = pd.read_csv(".csv")
output_file = ".csv"

# concatenate dfs
merged_salt_bridge = pd.concat([simulation_1,simulation_2,simulation_3,simulation_4]).reset_index().drop(columns=["index","COUNT"])
# count occurences & add it as a new column
merged_salt_bridge["REPEAT"]=merged_salt_bridge.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","PROT_IDX_LIST","LIG_IDX_LIST","INTERACTION TYPE"]).transform("size")
# combine percentages
merged_salt_bridge['PERCENT % LIST'] = merged_salt_bridge.groupby(["RESNR", "RESTYPE", "RESCHAIN", "RESNR_LIG", "RESTYPE_LIG", "RESCHAIN_LIG","PROT_IDX_LIST","LIG_IDX_LIST", "INTERACTION TYPE"])["PERCENT %"].transform(lambda x: "|".join(map(str, x)))
# remove duplicate rows
salt_bridge_data=merged_salt_bridge.drop_duplicates()
# define function to convert string to list of floats & apply to df
def string_to_float_list(string):
    substrings = string.split("|")
    float_list = [float(substring) for substring in substrings]
    return float_list
salt_bridge_data['PERCENT % LIST'] = salt_bridge_data['PERCENT % LIST'].apply(string_to_float_list)
# calculate mean & standard deviation
salt_bridge_data["MEAN"] = salt_bridge_data["PERCENT % LIST"].apply(lambda x: np.mean(x))
salt_bridge_data["STD_DEV"] = salt_bridge_data["PERCENT % LIST"].apply(lambda x: np.std(x))
# remove duplicates & unnecessary columns
final_salt_bridges_data = salt_bridge_data.drop(columns="PERCENT %")
final_salt_bridges_data.drop_duplicates(subset=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","PROT_IDX_LIST","LIG_IDX_LIST"],keep="first",inplace=True)
# write output to csv file
final_salt_bridges_data.to_csv(output_file,index=False)