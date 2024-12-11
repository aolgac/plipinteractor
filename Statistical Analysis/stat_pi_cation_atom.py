import pandas as pd
import numpy as np

# path to input files and output file
simulation_1 = pd.read_csv(".csv")
simulation_2 = pd.read_csv(".csv")
simulation_3 = pd.read_csv(".csv")
simulation_4 = pd.read_csv(".csv")
output_file = ".csv"

# concatenate dfs
merged_pi_cation = pd.concat([simulation_1,simulation_2,simulation_3,simulation_4]).reset_index().drop(columns=["index","COUNT"])
# count occurences & add it as a new column
merged_pi_cation["REPEAT"]=merged_pi_cation.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","PROT_IDX_LIST","LIG_IDX_LIST","INTERACTION TYPE"]).transform("size")
# combine percentages
merged_pi_cation['PERCENT % LIST'] = merged_pi_cation.groupby(["RESNR", "RESTYPE", "RESCHAIN", "RESNR_LIG", "RESTYPE_LIG", "RESCHAIN_LIG", "PROT_IDX_LIST","LIG_IDX_LIST", "INTERACTION TYPE"])["PERCENT %"].transform(lambda x: "|".join(map(str, x)))
# remove duplicate rows
pi_cation_data=merged_pi_cation.drop_duplicates()
# define function to convert string to list of floats & apply to df
def string_to_float_list(string):
    substrings = string.split("|")
    float_list = [float(substring) for substring in substrings]
    return float_list
pi_cation_data['PERCENT % LIST'] = pi_cation_data['PERCENT % LIST'].apply(string_to_float_list)
# calculate mean & standard deviation
pi_cation_data["MEAN"] = pi_cation_data["PERCENT % LIST"].apply(lambda x: np.mean(x))
pi_cation_data["STD_DEV"] = pi_cation_data["PERCENT % LIST"].apply(lambda x: np.std(x))
# remove duplicates & unnecessary columns
final_pi_cation_data=pi_cation_data.drop(columns="PERCENT %")
final_pi_cation_data.drop_duplicates(subset=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","PROT_IDX_LIST","LIG_IDX_LIST"],keep="first",inplace=True)
# write output to csv file
final_pi_cation_data.to_csv(output_file,index=False)