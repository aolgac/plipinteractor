
import pandas as pd
import numpy as np

# path to input files and output file
simulation_1 = pd.read_csv(".csv")
simulation_2 = pd.read_csv(".csv")
simulation_3 = pd.read_csv(".csv")
simulation_4 = pd.read_csv(".csv")
output_file = ".csv"

# concatenate dfs
merged_chain = pd.concat([simulation_1,simulation_2,simulation_3,simulation_4]).reset_index().drop(columns=["index","COUNT"])
# count occurences & add it as a new column
merged_chain["REPEAT"] = merged_chain.groupby([	"RESCHAIN","RESCHAIN_LIG","INTERACTION TYPE"]).transform("size")
# combine percentages
merged_chain['PERCENT % LIST'] = merged_chain.groupby(["RESCHAIN","RESCHAIN_LIG","INTERACTION TYPE"])["PERCENT %"].transform(lambda x: "|".join(map(str, x)))
# remove duplicate rows
chain_data=merged_chain.drop_duplicates()
# define function to convert string to list of floats & apply it to df
def string_to_float_list(string):
    substrings = string.split("|")
    float_list = [float(substring) for substring in substrings]
    return float_list
chain_data['PERCENT % LIST'] = chain_data['PERCENT % LIST'].apply(string_to_float_list)
# calculate mean & standard deviation
chain_data["MEAN"] = chain_data["PERCENT % LIST"].apply(lambda x: np.mean(x))
chain_data["STD_DEV"] = chain_data["PERCENT % LIST"].apply(lambda x: np.std(x))
# remove duplicates & unnecessary columns
final_chain_data = chain_data.drop(columns="PERCENT %")
final_chain_data.drop_duplicates(subset=["RESCHAIN","RESCHAIN_LIG","INTERACTION TYPE"],keep="first",inplace=True)
# write output to csv file
final_chain_data.to_csv(output_file,index=False)
