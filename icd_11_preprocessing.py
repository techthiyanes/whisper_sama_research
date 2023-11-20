# Define the function to limit words
def limit_to_approx_60_words(sentence, limit_=60, backtrack_limit=10):
    words = sentence.split()
    if len(words) <= limit_:
        return sentence

    # Initial cut-off at the word limit
    limited_text = " ".join(words[:limit_])

    # Search for the last punctuation within the backtrack_limit
    for i in range(limit_ - 1, limit_ - backtrack_limit, -1):
        if words[i][-1] in ".?!;,":  # Add any other punctuation marks if needed
            return " ".join(words[: i + 1])

    # If no punctuation is found within the backtrack_limit, return the limited_text
    return limited_text


def common_preprocessing(df):
    df = df.dropna(subset=['definition'])
    df = df.drop_duplicates(subset=['definition'])
    df = df.drop_duplicates(subset=['title'])
    df = df[~df['code'].str.contains(r'\.')]
    df['len'] = df['definition'].apply(lambda x: len(x.split()))
    df = df.sort_values('len', ascending = True)
    return df
    

import pandas as pd
df = pd.read_csv('icd_data.csv')

df = common_preprocessing(df)
df = df[df['len']>=40]
df['definition'] = df['definition'].apply(lambda x: limit_to_approx_60_words(x))
df = common_preprocessing(df)
df
