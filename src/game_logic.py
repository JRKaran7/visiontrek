import random

class VirtualTrekGame:
    def __init__(self):
        self.player_x = 100  # Player starts at x=100
        self.player_y = 300  # Fixed y-position
        self.score = 0
        self.coins = [(random.randint(200, 800), 300) for _ in range(5)]  # Random coins
        self.facts = [
            "Did you know? The Himalayas are still rising!",
            "Mount Everest grows about 4mm every year!",
            "Walking just 30 minutes a day improves heart health!"
        ]

    def move_player(self):
        self.player_x += 10  # Move forward when legs move
    
    def check_coin_collection(self):
        for coin in self.coins:
            if abs(self.player_x - coin[0]) < 50:  # If player reaches coin
                self.coins.remove(coin)
                self.score += 10
                self.coins.append((random.randint(self.player_x + 200, self.player_x + 500), 300))
                return True  # Coin collected
        return False

    def get_fact(self):
        if self.score % 200 == 0 and self.score > 0:  # Every 20 coins
            return random.choice(self.facts)
        return None
