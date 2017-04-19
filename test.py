import pandas as pd
def read_df(file_path='./comics_output.csv'):
    df = pd.read_csv(file_path)
    return df

df = read_df()

print(df.ix[[1,2]])
