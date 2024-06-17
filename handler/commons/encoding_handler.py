def handle_encoding(df, encoder, features):
    for feature in features:
        df[feature] = encoder[feature].transform(df[feature])

    return df
