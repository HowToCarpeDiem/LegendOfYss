import random

class Item:
    def __init__(self, name, effect_type, effect_value):
        self.name = name
        self.effect_type = effect_type
        self.effect_value = effect_value

    def apply_effect(self, player):
        if self.effect_type == 'health':
            player.health += self.effect_value
            print(f"Twoje zdrowie zwiększyło się o {self.effect_value} punktów!")
        elif self.effect_type == 'attack':
            player.attack += self.effect_value
            print(f"Twoja siła ataku zwiększyła się o {self.effect_value} punktów!")
class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack = 7
        self.gold = 0
        self.inventory = []
        self.battle_count = 0  # Dodany licznik walk

    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        self.health -= damage

    def attack_enemy(self, enemy):
        damage = random.randint(5, self.attack)
        enemy.take_damage(damage)
        return damage

    def show_status(self):
        print(f"\n{self.name} status:")
        print(f"Zdrowie: {self.health}")
        print(f"Złoto: {self.gold}")
        print(f"Ekwipunek: {', '.join([item.name for item in self.inventory]) if self.inventory else 'Puste'}\n")

        

class Enemy:
    def __init__(self, name, health, attack, loot):
        self.name = name
        self.health = health
        self.attack = attack
        self.loot = loot

    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        self.health -= damage

    def attack_player(self, player):
        damage = random.randint(5, self.attack)
        player.take_damage(damage)
        return damage

def create_enemy(battle_count):
    enemies = [
        Enemy("Goblin", 20, 6, [Item("Drewniana pałka", "attack", 5), Item("Gulasz z Goblina", "health", 40)]),
        Enemy("Ork", 50, 12, [Item("Miecz Orka", "attack", 10)])
    ]
    if battle_count >= 3:
        enemies.append(Enemy("Smok", 80, 19, [Item("Odwar z języka smoka", "health", 50)]))
    return random.choice(enemies)


def explore(player):
    print("Eksplorujesz mroczny las...")
    if random.random() < 0.5:
        enemy = create_enemy(player.battle_count)
        print(f"Atakuje Cię {enemy.name}")
        return enemy
    else:
        print("Nic nie znalazłeś")
        return None

    
def combat(player, enemy):
    while player.is_alive() and enemy.is_alive():
        action = input("(A)takuj lub (U)ciekaj ").lower()
        if action == 'a':
            damage = player.attack_enemy(enemy)
            print(f"Zadałeś {enemy.name} {damage} obrażeń")
            if not enemy.is_alive():
                print(f"Pokonałeś {enemy.name}")
                player.gold += 10
                loot = random.choice(enemy.loot)
                player.inventory.append(loot)
                print(f"Zdobyłeś: {loot.name}")
                loot.apply_effect(player)
                player.battle_count += 1  
                break
            damage = enemy.attack_player(player)
            print(f"{enemy.name} zadał Ci {damage} obrażeń")
            if not player.is_alive():
                print("Nie żyjesz")
                break
        elif action == 'u':
            if random.random() < 0.5:
                print("Ucieczka udana!")
                break
            else:
                print("Ucieczka nieudana! Musisz walczyć dalej!")
                damage = enemy.attack_player(player)
                print(f"{enemy.name} zadał Ci {damage} obrażeń")
                if not player.is_alive():
                    print("Nie żyjesz")
                    break
        else:
            print("Zły klawisz. Wciśnij 'a' lub 'u'")



def main():
    print("Witaj w świecie Yss!")
    name = input("Wpisz swoją nazwę: ")
    player = Player(name)
    print(f"Witaj, {player.name}! Twoja przygoda właśnie się zaczyna!")

    while player.is_alive():
        action = input("(G)raj, (S)prawdź stan, (Z)akończ przygodę ").lower()
        if action == 'g':
            enemy = explore(player)
            if enemy:
                combat(player, enemy)
        elif action == 's':
            player.show_status()
        elif action == 'z':
            print("Nie podołałeś?")
            break
        else:
            print("Zły klawisz. Wciśnij 'g', 's' lub 'z' ")

    print("Koniec gry!")

if __name__ == "__main__":
    main()
