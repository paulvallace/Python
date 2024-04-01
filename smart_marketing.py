
import pandas as pd
import re
from sklearn.linear_model import LinearRegression, LogisticRegression
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


#test_y = pd.read_csv("data/test1_y.csv")


def train_dataframe(train_users, train_logs, y):
    logs_dict = {}
    for item in range (len(train_logs)):
        user_id = train_logs.at[train_logs.index[item], "user_id"]
        if user_id not in logs_dict:
            logs_dict[user_id] = [1]
        else:
            logs_dict[user_id][0] += 1

    for idx in logs_dict:
        valc = 0 
        secs = 0
        df = train_logs[train_logs["user_id"] == idx]
        urls = df['url']
        for item in urls:
            val = re.findall(r"/(\D+)\.", item)[0]
            if val == "laptop":
                valc += 1 
        seconds = df["seconds"]
        for item in seconds:
            secs += int(item)
        logs_dict[idx].append(secs)
        logs_dict[idx].append(valc)

    for item in range(len(train_users)):
        if item not in logs_dict:
            logs_dict[item]= [0,0,0]
    new_logs = dict(sorted(logs_dict.items(), key = lambda x : x[0]))
    user_ids = list(new_logs.keys())
    sec_list = []
    click_list = []
    val_list = []
    for item in new_logs:
        clicks = new_logs[item][0]
        seconds = new_logs[item][1]
        vals = new_logs[item][2]
        sec_list.append(seconds)
        click_list.append(clicks)
        val_list.append(vals)

    items = {'user_id' : user_ids, "total_seconds" : sec_list, "clicks" : click_list, "laptop_searches": val_list}

    df = pd.DataFrame(items)

    df2 = y.copy()

    merge = pd.merge(df, df2, on = "user_id")
    final_df = pd.merge(merge, train_users[['user_id','age','past_purchase_amt',
                                       'badge']], on = "user_id")
    final_df.total_seconds /= 60
    
    badge = list(final_df.badge)
    for item in range(len(badge)):
        val = badge[item]
        if val == "gold":
            badge[item] = 3
        if val == "silver":
            badge[item] = 2
        if val == "bronze":
            badge[item] = 1
    final_df["badge"] = badge
    return final_df
    
    
def test_dataframe(train_users, train_logs):
    index = list(train_users["user_id"])
    test_dict = {}
    for item in range (len(train_logs)):
        user_id = train_logs.at[train_logs.index[item], "user_id"]
        if user_id not in test_dict:
            test_dict[user_id] = [1]
        else:
            test_dict[user_id][0] += 1

    for idx in test_dict:
        valc = 0 
        secs = 0
        df = train_logs[train_logs["user_id"] == idx]
        urls = df['url']
        for item in urls:
            val = re.findall(r"/(\D+)\.", item)[0]
            if val == "laptop":
                valc += 1 
        seconds = df["seconds"]
        for item in seconds:
            secs += int(item)
        test_dict[idx].append(secs)
        test_dict[idx].append(valc)

    for item in range(index[0], index[-1]):
        if item not in test_dict:
            test_dict[item]= [0,0,0]
            
    new_logs = dict(sorted(test_dict.items(), key = lambda x : x[0]))
    user_ids = list(new_logs.keys())
    sec_list = []
    click_list = []
    val_list = []
    for item in new_logs:
        clicks = new_logs[item][0]
        seconds = new_logs[item][1]
        vals = new_logs[item][2]
        sec_list.append(seconds)
        click_list.append(clicks)
        val_list.append(vals)

    items = {'user_id' : user_ids, "total_seconds" : sec_list, "clicks" : click_list, "laptop_searches": val_list}

    df3 = pd.DataFrame(items)

    final_df = pd.merge(df3, train_users[['user_id','age','past_purchase_amt',
                                       'badge']], on = "user_id")
    final_df.total_seconds /= 60
    
    badge = list(final_df.badge)
    for item in range(len(badge)):
        val = badge[item]
        if val == "gold":
            badge[item] = 3
        if val == "silver":
            badge[item] = 2
        if val == "bronze":
            badge[item] = 1
    final_df["badge"] = badge
    return final_df


class UserPredictor():
    def __init__(self):
        self.model = None
        
    def fit(self, train_users, train_logs, y):
        final_df = train_dataframe(train_users, train_logs, y)
        
        train, test = train_test_split(final_df, test_size=0.20, random_state=200)
        xcols = ["clicks", "laptop_searches", "total_seconds", "past_purchase_amt", "badge"]
        ycol = "y"
        model = LogisticRegression()
        self.model = model.fit(train[xcols], train[ycol])
        return self.model
    def predict(self, train_users, train_logs):
        final_df = test_dataframe(train_users, train_logs)
        xcols = ["clicks", "laptop_searches", "total_seconds", "past_purchase_amt", "badge"]
        return self.model.predict(final_df[xcols])
