import pandas as pd
import datetime
import csv
import os
from werkzeug.security import generate_password_hash, check_password_hash

def chek_credidentals(user_id, password):
    try:
        df = pd.read_csv("user_detail.csv")
        df = df.applymap(lambda x: str(x).strip().strip('"').strip("'"))

        user_row = df.loc[df["User Id"] == user_id]
        if user_row.empty:
            return None

        stored_hash = user_row.iloc[0]["Password"]
        if check_password_hash(stored_hash, password):
            return user_row.iloc[0]  # return user details
        return None
    except FileNotFoundError:
        return None


def for_signup(user_id,password,email):
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    current_date = datetime.date.today().strftime("%d/%m/%y")
    hashed_password = generate_password_hash(password)
    new_entry = pd.DataFrame(
        [[current_date, email, user_id, hashed_password, current_time]],
        columns=["Date", "Email","User Id", "Password", "Time"]
    )

    file_exists = os.path.exists("user_detail.csv")
    new_entry.to_csv(
        "user_detail.csv",
        mode="a",
        header=not file_exists,
        index=False,
        quoting=csv.QUOTE_ALL,
        escapechar="\\",
    )

def for_update(email,password):
    try:
        df = pd.read_csv("user_detail.csv")
        df = df.applymap(lambda x: str(x).strip().strip('"').strip("'"))

        user_row = df.loc[df["Email"] == email]
        
        if user_row.empty:
            return None

        stored_hash = user_row.iloc[0]["Password"]
        if check_password_hash(stored_hash, password):
            return "please make different from present once"  # return user details
        else:
            hashed_password = generate_password_hash(password)
            # df.loc[df["Email"]==email,"Password"]= hashed_password
            df.loc[df["Email"] == email, "Password"] = hashed_password
            df.to_csv("user_detail.csv", index=False)
            
        
            # file_exists = os.path.exists("user_detail.csv")     
        return None
    except FileNotFoundError:
        return None