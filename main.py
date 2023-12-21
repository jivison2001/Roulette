import random as rnd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

class Player:
    def __init__(self, starting_balance):
        self.balance = starting_balance
        self.balance_history = np.array([starting_balance])
        
    def update_balance_history(self):
        self.balance_history = np.append(self.balance_history, self.balance)

class Roulette:
    def __init__(self):
        self.numbers = dict()
        self.red_numbers = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
        self.black_numbers = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
        
        for i in self.red_numbers:
            self.numbers[i] = "red"
            
        for i in self.black_numbers:
            self.numbers[i] = "black"
            
        self.numbers[0] = "green"
        #sort by number
        self.numbers = dict(sorted(self.numbers.items()))
        
    #simulates spinning the wheel
    #returns the number of colour of what the ball landed on
    def spin(self):
        number = rnd.randint(0,36)
        colour = self.numbers[number]
        return number, colour
    
    def bet_odd_even(self, player: Player, stake: float, bet_type: str):
        # if stake > player.balance:
        #     print("Not enough account credit to stake this much")
        
        player.balance -= stake
        number, colour = self.spin()
        #even bet
        if bet_type == "even":
            if number % 2 == 0 and number != 0:
                player.balance += stake*2
                return True
        #odd bet
        elif bet_type == "odd":
            if number % 2 != 0 and number != 0:
                player.balance += stake*2
                return True
            
        return False
                
    def bet_red_black(self, player: Player, stake: float, bet_type: str):
        if stake > player.balance:
            print("Not enough account credit to stake this much")
        
        player.balance -= stake
        number, colour = self.spin()
        #red bet
        if bet_type == "red":
            if self.numbers[number] == "red":
                player.balance += stake*2
                return True
        #odd bet
        elif bet_type == "black":
            if self.numbers[number] == "black":
                player.balance += stake*2
                return True
                
        return False
    
    def simulate(self, n_spins):
        results = []
        for i in range(n_spins):
            number, colour = self.spin()
            results.append(number)
            
        return results
   
def report_results(data1, data2, title: str):
    plt.plot(data1, label="max", color='red')
    plt.plot(data2, label="min", color='blue')
    plt.title(title)
    plt.legend()
    plt.show()
         
if __name__ == "__main__":
    r = Roulette()
    p = Player(10)
    
    max_balances = np.array([])
    max_averages = np.array([])
    min_balances = np.array([])
    min_averages = np.array([])
    
    n_trials = 1000 #number of games of roulette to play per simulation
    n_sims = 100 #number of simulations to perform
    stake = 1
    loss_threshold = 0
    n_losses = 0
    prev_result = True #true if last game was won
    for j in range(n_sims):
        p = Player(50)
        stake=1
        for i in range(n_trials):
            if p.balance <= loss_threshold:
                n_losses += 1
                break
            if prev_result == False:
                stake = stake*2
                current_result = r.bet_odd_even(p, stake, "even")
            else:
                stake = 1
                current_result = r.bet_odd_even(p, stake, "even")
            
            p.update_balance_history()
            prev_result = current_result
        
        max_val = np.amax(p.balance_history)
        min_val = np.amin(p.balance_history)
        max_balances = np.append(max_balances, max_val)
        min_balances = np.append(min_balances, min_val)
        max_averages = np.append(max_averages, np.mean(max_balances))
        min_averages = np.append(min_averages, np.mean(min_balances))
     
    loss_percentage = (n_losses/n_sims)*100
    print(np.mean(max_balances))
    print(np.mean(min_balances))
    print("Percentage of losses: " + str(loss_percentage) + "%")    
    report_results(max_balances, min_balances, "Maximum and minimum balances for each game")
    report_results(max_averages, min_averages, "Average max and min balance after each game")
    