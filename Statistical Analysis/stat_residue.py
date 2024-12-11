import pandas as pd
import numpy as np

# path to input files and output file
simulation_1 = pd.read_csv(".csv")
simulation_2 = pd.read_csv(".csv")
simulation_3 = pd.read_csv(".csv")
simulation_4 = pd.read_csv(".csv")
output_file = ".csv"

# concatenate dfs
merged_residue = pd.concat([simulation_1,simulation_2,simulation_3,simulation_4]).reset_index().drop(columns=["index","COUNT"])
# count occurences & add it as a new column
merged_residue["REPEAT"] = merged_residue.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","INTERACTION TYPE"]).transform("size")
# combine percentages
merged_residue['PERCENT % LIST'] = merged_residue.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","INTERACTION TYPE"])["PERCENT %"].transform(lambda x: "|".join(map(str, x)))
# remove duplicate rows
residue_data=merged_residue.drop_duplicates()
# define function to convert string to list of floats & apply to df
def string_to_float_list(string):
    substrings = string.split("|")
    float_list = [float(substring) for substring in substrings]
    return float_list
residue_data['PERCENT % LIST'] = residue_data['PERCENT % LIST'].apply(string_to_float_list)
# calculate mean & standard deviation
residue_data["MEAN"] = residue_data["PERCENT % LIST"].apply(lambda x: np.mean(x))
residue_data["STD_DEV"] = residue_data["PERCENT % LIST"].apply(lambda x: np.std(x))
# remove duplicates & unnecessary columns
final_residue_data = residue_data.drop(columns="PERCENT %")
final_residue_data.drop_duplicates(subset=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG"],keep="first",inplace=True)
# write output to csv file
final_residue_data.to_csv(output_file,index=False)