import requests
from AbstractGameCycle import GameCycle

class RouletteGameCycle(GameCycle):

    def __init__(self,header,deal_url):
        # super.__init__(status_url,create_url,header)
        #self.status_url=status_url
        #self.create_url = create_url
        self.deal_url = deal_url
        self.header = header
        self.deal_json = None
        self.expected_output = None

    def set_deal_json(self,json):
        self.deal_json=json

    def set_expected_output(self,ews):
        self.expected_output = ews

    def card_deal(self):
        self.deal_card_first_spot()

    def verify_result(self):
        response_output = requests.get(url=self.status_url,headers=self.header).get("result").get("data").get("ws").get("1")
        res_out = sorted(response_output)
        exp_out = sorted(self.expected_output)
        print(f"response output : {res_out}")
        print(f"expected output : {exp_out}")
        if res_out == exp_out :
            print("pass")
        else:
            print("fail")

    
    def start(self):
        super(RouletteGameCycle,self).create_game()
        super(RouletteGameCycle,self).bet_timer()
        super(RouletteGameCycle,self).card_deal()
        super(RouletteGameCycle,self).verify_result()
        super(RouletteGameCycle,self).result_timer()
        
    def deal_card_first_spot(self,deal_json):
        requests.post(url=self.deal_url,json=deal_json,headers=self.header)
