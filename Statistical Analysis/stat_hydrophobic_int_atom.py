import pandas as pd
import numpy as np

# path to input files and output file
simulation_1 = pd.read_csv(".csv")
simulation_2 = pd.read_csv(".csv")
simulation_3 = pd.read_csv(".csv")
simulation_4 = pd.read_csv(".csv")
output_file = ".csv"

# concatenate dfs
merged_hydrophobic_interaction = pd.concat([simulation_1,simulation_2,simulation_3,simulation_4]).reset_index().drop(columns=["index","COUNT"])
# count occurences & add it as a new column
merged_hydrophobic_interaction["REPEAT"]=merged_hydrophobic_interaction.groupby(["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","LIGCARBONIDX","PROTCARBONIDX","INTERACTION TYPE"]).transform("size")
# combine percentages
merged_hydrophobic_interaction['PERCENT % LIST'] = merged_hydrophobic_interaction.groupby(["RESNR", "RESTYPE", "RESCHAIN", "RESNR_LIG", "RESTYPE_LIG", "RESCHAIN_LIG", "LIGCARBONIDX","PROTCARBONIDX", "INTERACTION TYPE"])["PERCENT %"].transform(lambda x: "|".join(map(str, x)))
# remove duplicate rows
hydrophobic_interaction_data=merged_hydrophobic_interaction.drop_duplicates()
# define function to convert string to list of floats & apply to df
def string_to_float_list(string):
    substrings = string.split("|")
    float_list = [float(substring) for substring in substrings]
    return float_list
hydrophobic_interaction_data['PERCENT % LIST'] = hydrophobic_interaction_data['PERCENT % LIST'].apply(string_to_float_list)
# calculate mean & standard deviation
hydrophobic_interaction_data["MEAN"] = hydrophobic_interaction_data["PERCENT % LIST"].apply(lambda x: np.mean(x))
hydrophobic_interaction_data["STD_DEV"] = hydrophobic_interaction_data["PERCENT % LIST"].apply(lambda x: np.std(x))
# remove duplicates & unnecessary columns
final_hydrophobic_interaction_data=hydrophobic_interaction_data.drop(columns="PERCENT %")
final_hydrophobic_interaction_data.drop_duplicates(subset=["RESNR","RESTYPE","RESCHAIN","RESNR_LIG","RESTYPE_LIG","RESCHAIN_LIG","LIGCARBONIDX","PROTCARBONIDX"],keep="first",inplace=True)
# write output to csv file
final_hydrophobic_interaction_data.to_csv(output_file,index=False)