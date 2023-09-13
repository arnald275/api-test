from abc import ABC,abstractmethod
import time
import requests
class GameCycle(ABC):

    def __init__(self,status_url,create_url,header):
        self.status_url = status_url
        self.create_url = create_url
        self.header = header

    def create_game(self):
        status_res = self.check_status(self.status_url,self.header)
        if(status_res.get("status") == "NEW_GAME"):
            requests.post(url=self.create_url,headers=self.header)
        else:
            raise Exception(f"game-not-created : {status_res}")
        
    
    def bet_timer(self):
        status_res = self.check_status(self.status_url,self.header)
        if(status_res.get("status") == "BET_TIMER"):
            time.sleep(status_res.get("result").get("secs"))
        else: 
            raise Exception(f"bad response {status_res}")
        self.check_bet_timer_ends()
        

    @abstractmethod
    def card_deal(self):
        pass

    @abstractmethod
    def verify_result(self):
        pass

    def result_timer(self):
        status_res = self.check_status()
        if(status_res.get("status") == "RESULT_TIMER"):
            time.sleep(status_res.get("result").get("secs"))
        self.check_result_timer_ends()

    def check_status(self):
        return requests.get(url=self.status_url,headers=self.header).json()

    def check_bet_timer_ends(self):
        status = self.check_status().get("status")
        if(status=="NEXT_CARD"):
            return True
        if(self.check_bet_timer_ends() !=True):
            time.sleep(0.5)
            self.check_bet_timer_ends()

    def check_result_timer_ends(self):
        status = self.check_status().get("status")
        if(status=="NEW_GAME"):
            return True
        if(self.check_result_timer_ends() !=True):
            time.sleep(0.5)
            self.check_result_timer_ends()

            
       