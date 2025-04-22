import pandas as pd
import os,sys
import sqlite3
from datetime import datetime
from uuid import uuid4

def load_data(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    return pd.read_csv(filepath)

def clean_data(df):
    df.columns = df.columns.str.strip().str.lower()

    required_columns = [
        'cpe_title',
        'cpe_22_uri',
        'cpe_23_uri',
        'reference_links',
        'cpe_22_deprecation_date',
        'cpe_23_deprecation_date'
    ]

    df = df[required_columns]
    df.drop_duplicates(inplace=True)

    df['cpe_id'] = [str(uuid4()) for _ in range(len(df))]

    df['cpe_22_deprecation_date'] = pd.to_datetime(df['cpe_22_deprecation_date'], errors='coerce').dt.date
    df['cpe_23_deprecation_date'] = pd.to_datetime(df['cpe_23_deprecation_date'], errors='coerce').dt.date

    df['reference_links'] = df['reference_links'].apply(
        lambda x: [i.strip() for i in x.split(',')] if isinstance(x, str) else []
    )

    return df

def store_data(df, db_name="cpes.db", table_name="cpes"):
    conn = sqlite3.connect(db_name)

    df['reference_links'] = df['reference_links'].apply(lambda x: str(x))
    df.insert(0, 'id', range(1, len(df) + 1))

    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def main(file_path):
    df = load_data(file_path)
    df = clean_data(df)
    store_data(df)
    print("CPE data loaded into the database !")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python load_data_to_db.py <csv_file_path>")
        sys.exit(1)

    csv_file_path = sys.argv[1]

    
    main(csv_file_path)
