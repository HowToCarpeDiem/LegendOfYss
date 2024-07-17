import random

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack = 7
        self.gold = 0
        self.inventory = []

    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        self.health -= damage

    def attack_enemy(self, enemy):
        damage = random.randint(5, self.attack)
        enemy.take_damage(damage)
        return damage
        

class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        self.health -= damage

    def attack_player(self, player):
        damage = random.randint(5, self.attack)
        player.take_damage(damage)
        return damage

def create_enemy():
    enemies = [
        Enemy("Goblin", 20, 6),
        Enemy("Ork", 50, 12),
        Enemy("Smok", 80, 22)
    ]
    return random.choice(enemies)

def explore():
    print("Eksplorujesz mroczny las...")
    if random.random() < 0.5:
        enemy = create_enemy()
        print(f"Atakuje Cię {enemy.name}")
        return enemy
    else:
        print("Nic nie znalazłeś")
        return None
    
def combat(player, enemy):
    while player.is_alive() and enemy.is_alive():
        action = input("(A)takuj lub (U)ciekaj").lower()
        if action == 'a':
            damage = player.attack_enemy(enemy)
            print(f"Zadałeś {enemy.name} {damage} obrażeń")
            if not enemy.is_alive():
                print(f"Pokonałeś {enemy.name}")
                player.gold += 10
                player.inventory.append(f"{enemy.name} zdobyłeś")
                break
            damage = enemy.attack_player(player)
            print(f"{enemy.name} zadał Ci {damage} obrażeń")
            if not player.is_alive():
                print("Nie żyjesz")
                break
        elif action == 'u':
            print("Uciekłeś!")
            break
        else:
            print("Zły klawisz. Wciśnij 'a' lub 'u'")

def main():
    print("Witaj w świecie Yss!")
    name = input("Wpisz swoją nazwę ")
    player = Player(name)
    print(f"Witaj, {player.name} twoja przygoda właśnie się zaczyna!")

    while player.is_alive():
        action = input("(G)raj lub (Z)akończ przygodę ").lower()
        if action == 'g':
            enemy = explore()
            if enemy:
                combat(player, enemy)
        elif action == 'z':
            print("Nie podołałeś?")
            break
        else:
            print("Zły klawisz. Wciśnij 'g' lub 'z' ")

        print("Koniec gry!")

if __name__ == "__main__":
    main()