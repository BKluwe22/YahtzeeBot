from ev_calculations import build_tables
from strategy import YahtzeeAgent
from yahtzee import Yahtzee


# RANDOM SEED IS 22 (Check strategy.py)
def main(): 
    
    build_tables()
    
    env = Yahtzee()
    agent = YahtzeeAgent(env)
    
    agent.strategy_benchmark_report(1000000)
    
    
    
if __name__ == "__main__":
    main()