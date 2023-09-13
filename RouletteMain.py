
import json
import requests
from RouletteGameCycle import RouletteGameCycle
dev_env = 'http://10.10.20.133:10002'
local_env = 'http://localhost:10002'
ui_env = 'http://10.10.20.135:10002'
qc_env = 'http://10.10.20.134:10002'
login_url= '/casino/api/noAuth/dealer/login'
status_url = '/roulette/api/game/status'
create_game_url = '/roulette/api/game/create'
deal_url = '/roulette/api/game/deal'

login_json = { 
    "username":"roulette",
     "password":"123456",
     "tableId":"Rou1hq4jo2etrjg3",
     "shortId":"RO01",
    "studioId":"1"
}
deal_roulette_json={
                "spot":"SPOT_NUMBER",
                "index":0,
                "card":0
}


def readText(fileName):
    data_list = []
    with open(fileName, 'r') as f:
        for line in f:
            data_list.append(json.loads(line))
    return data_list

if __name__ == "__main__":
    test_cases = readText("roulette-results.txt")
    print(f"{len(test_cases)} cases need to test")
    # dealer - login
    login_response = requests.post(url=dev_env+login_url, json=login_json).json()
    if(login_response.get("status") ==  "SUCCESS"):
        token = login_response.get("result").get("token")
        header = {
            'Authorization': f"Bearer {token}",
        }
        roulette_game = RouletteGameCycle(dev_env+status_url,dev_env+create_game_url,header,dev_env+deal_url)
        roulette_game.set_deal_json(deal_roulette_json)
        roulette_game.set_expected_output(test_cases)
        roulette_game.start()

        # for i in range(0, len(test_cases)):
        #     roulette_game
        
    else:
        raise Exception(f"game-not-created : {login_response}")