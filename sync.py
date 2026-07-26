import requests
import json
import os
import subprocess
from datetime import datetime

def save_state(last_second):
    state = {"last_epoch_second": last_second}
    with open("state.json", "w") as f:
        json.dump(state, f)

def load_state():
    try:
        with open("state.json", "r") as f:
            state = json.load(f)
        return state["last_epoch_second"]
    except FileNotFoundError:
        return 0

# 1, 前回どこまでやったかを読み込む
from_second = load_state()

# 2, 今回の値を取得してくる
url = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions"
params = {
    "user": "monstera",
    "from_second": from_second,
}

response = requests.get(url, params=params)
data = response.json()

# 3, 次回のために保存
if data:
    new_last_second = max(sub["epoch_second"] for sub in data)
    save_state(new_last_second + 1)

# AC絞る
ac_subs = []
for sub in data:
    if sub["result"] == "AC":
        ac_subs.append(sub)

os.makedirs("solutions", exist_ok = True)

# ファイル作成
for sub in ac_subs:
    filename = "solutions/" + sub["problem_id"] + ".txt"
    with open(filename, "w") as f:
        f.write("solved: " + sub["problem_id"])
    #　日付型変換
    dt = datetime.fromtimestamp(sub["epoch_second"])
    dt_str = dt.isoformat()
    print(dt_str)
    #ぎっと
    subprocess.run(["git", "add", filename])
    subprocess.run(["git", "commit", "-m", "solve: " + sub["problem_id"], "--date", dt_str])


