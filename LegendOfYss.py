import random
import os

class Item:
    def __init__(self, name, effect_type, effect_value, gold_value=0):
        self.name = name
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.gold_value = gold_value  
        self.upgrade_level = 0  

    def apply_effect(self, player):
        if self.effect_type == 'health':
            player.health += self.effect_value
            print(f"\033[92mTwoje zdrowie zwiększyło się o {self.effect_value} punktów!\033[0m")
        elif self.effect_type == 'attack': #bronie
            player.attack += self.effect_value
            print(f"Twoja siła ataku zwiększyła się o {self.effect_value} punktów!")
        elif self.effect_type == 'armor':
            player.armor += self.effect_value
            print(f"\033[94mTwój pancerz zwiększył się o {self.effect_value} punktów!\033[0m")
        elif self.effect_type == 'attack_boost':  #dla przedmiotów
            player.attack += self.effect_value
            print(f"\033[93mTwoja siła ataku zwiększyła się o {self.effect_value} punktów!\033[0m")
        print(f"Zastosowano efekt przedmiotu: {self.name}")

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack = 7
        self.armor = 0
        self.gold = 0
        self.inventory = []
        self.active_weapon = None  
        self.experience = 0
        self.battle_count = 0
        self.unlocked_locations = ["Mroczny las"]
        self.current_location = "Mroczny las"

    def unlock_desert(self):
        self.unlocked_desert = True

    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage, attacker):
        effective_damage = max(0, damage - self.armor)
        self.health -= effective_damage
        print(f"\033[91m{attacker.name} zadał Ci {effective_damage} obrażeń\033[0m")


    def attack_enemy(self, enemy):
        if self.active_weapon:
            base_damage = random.randint(int(self.active_weapon.effect_value * 0.8), self.active_weapon.effect_value)
        else:
            base_damage = random.randint(int(self.attack * 0.8), self.attack)

        if random.random() < 0.1:  
            damage = int(base_damage * 1.3)
            print("\033[95mObrażenia krytyczne!\033[0m")
        else:
            damage = base_damage
        enemy.take_damage(damage)
        print(f"\033[93mZadałeś {enemy.name} {damage} obrażeń\033[0m")
        return damage

    def show_status(self):
        print(f"\n{self.name} status:")
        print(f"Zdrowie: {self.health}")
        print(f"Podstawowy atak: {self.attack}")
        if self.active_weapon:
            weapon_name = self.active_weapon.name
            weapon_attack = self.active_weapon.effect_value
            weapon_upgrade = self.active_weapon.upgrade_level
            print(f"Aktywna broń: {weapon_name} (Atak: {weapon_attack}, Poziom: +{weapon_upgrade})")
            print(f"Atak po założeniu broni: {self.attack + weapon_attack}")
        else:
            print(f"Aktywna broń: Brak")
            print(f"Atak po założeniu broni: {self.attack}")
        print(f"Pancerz: {self.armor}")
        print(f"Złoto: {self.gold}")
        print(f"Doświadczenie: {self.experience}")
        print(f"Liczba walk: {self.battle_count}")  
        print(f"Ekwipunek: {', '.join([item.name for item in self.inventory]) if self.inventory else 'Puste'}\n")

    def choose_weapon(self):
        print("Wybierz broń z ekwipunku:")
        weapons = [item for item in self.inventory if item.effect_type == 'attack']
        if not weapons:
            print("Nie masz żadnej broni w ekwipunku.")
            return
        for i, weapon in enumerate(weapons):
            print(f"{i+1}. {weapon.name} (Atak: {weapon.effect_value}, Poziom: +{weapon.upgrade_level})")
        choice = int(input("Podaj numer broni, którą chcesz aktywować: ")) - 1
        if 0 <= choice < len(weapons):
            self.active_weapon = weapons[choice]
            print(f"Aktywowałeś broń: {self.active_weapon.name}")
        else:
            print("Niepoprawny wybór.")
    
    def activate_item(self):
        print("Wybierz przedmiot do aktywacji:")
        items = [item for item in self.inventory if item.effect_type in ['armor', 'health','attack_boost']]
        if not items:
            print("Nie masz żadnych przedmiotów do aktywacji w ekwipunku.")
            return
        for i, item in enumerate(items):
            print(f"{i+1}. {item.name} (Typ: {item.effect_type.capitalize()}, Wartość: {item.effect_value})")
        choice = int(input("Podaj numer przedmiotu, który chcesz aktywować: ")) - 1
        if 0 <= choice < len(items):
            selected_item = items[choice]
            selected_item.apply_effect(self)
            self.inventory.remove(selected_item)
            print(f"Aktywowałeś przedmiot: {selected_item.name}")
        else:
            print("Niepoprawny wybór.")

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
        base_damage = random.randint(int(self.attack * 0.8), self.attack)
        if random.random() < 0.1:  
            damage = int(base_damage * 1.4)
            print(f"\033[95m{self.name} zadaje obrażenia krytyczne!\033[0m")
        else:
            damage = base_damage
        player.take_damage(damage, self)
        return damage


def visit_city(player):
    wiedzący = Wiedzący()
    kowal = Kowal()
    print("Witaj w mieście! Możesz tu ulepszyć swoją postać lub broń, albo handlować.")
    while True:
        action = input("(U)lepsz postać, (K)owal, (H)andluj, (W)róć do gry: ").lower()
        if action == 'u':
            wiedzący.upgrade(player)
        elif action == 'k':
            kowal.upgrade_weapon(player)
        elif action == 'h':
            visit_merchant(player)
        elif action == 'w':
            break
        else:
            print("Zły klawisz. Wciśnij 'u', 'k', 'h' lub 'w'")
            

class Kowal:
    def __init__(self):
        self.upgrade_costs = {
            1: 50,
            2: 100,
            3: 200,
            4: 400,
            5: 800
        }

    def upgrade_weapon(self, player):
        if not player.active_weapon:
            print("Nie masz aktywnej broni do ulepszenia.")
            return
        
        current_level = getattr(player.active_weapon, 'upgrade_level', 0)
        if current_level >= 5:
            print("Twoja broń osiągnęła maksymalny poziom ulepszenia.")
            return
        
        next_level = current_level + 1
        cost = self.upgrade_costs[next_level]
        print(f"Koszt ulepszenia do poziomu +{next_level}: {cost} złota")

        if player.gold >= cost:
            player.gold -= cost
            if current_level == 0:
                player.active_weapon.upgrade_level = 1
            else:
                player.active_weapon.upgrade_level += 1
            player.active_weapon.effect_value += 2 * next_level  # Przyrost ataku o 2 za każdy poziom
            print(f"Ulepszyłeś {player.active_weapon.name} do poziomu +{next_level}")
        else:
            print("Nie masz wystarczająco złota.")

def visit_merchant(player):
    merchant = Merchant()
    print("Witaj u kupca! Możesz tu kupować i sprzedawać przedmioty.")
    while True:
        action = input("(K)up przedmiot, (S)przedaj przedmiot, (W)róć: ").lower()
        if action == 'k':
            merchant.buy(player)
        elif action == 's':
            merchant.sell(player)
        elif action == 'w':
            break
        else:
            print("Zły klawisz. Wciśnij 'k', 's' lub 'w'")

class Merchant:
    def __init__(self):
        self.inventory = [
            Item("Eliksir zdrowia", "health", 30, 20),
            Item("Eliksir mocy", "attack_boost", 10, 25),
            Item("Pancerz ze skóry", "armor", 3, 15),
            Item("Miecz rycerza", "attack", 25, 50)
        ]

    def show_inventory(self):
        print("\nSklep kupca:")
        for i, item in enumerate(self.inventory):
            print(f"{i+1}. {item.name} (Typ: {item.effect_type.capitalize()}, Wartość: {item.effect_value}, Cena: {item.gold_value} złota)")
        print()

    def buy(self, player):
        self.show_inventory()
        choice = int(input("Wybierz numer przedmiotu, który chcesz kupić: ")) - 1
        if 0 <= choice < len(self.inventory):
            item = self.inventory[choice]
            if player.gold >= item.gold_value:
                player.gold -= item.gold_value
                player.inventory.append(item)
                print(f"Kupiłeś {item.name}")
            else:
                print("Nie masz wystarczająco złota, aby kupić ten przedmiot.")
        else:
            print("Niepoprawny wybór.")

    def sell(self, player):
        if not player.inventory:
            print("Nie masz żadnych przedmiotów do sprzedania.")
            return
        print("\nTwój ekwipunek:")
        for i, item in enumerate(player.inventory):
            print(f"{i+1}. {item.name} (Typ: {item.effect_type.capitalize()}, Wartość: {item.effect_value}, Cena sprzedaży: {item.gold_value} złota)")
        choice = int(input("Wybierz numer przedmiotu, który chcesz sprzedać: ")) - 1
        if 0 <= choice < len(player.inventory):
            item = player.inventory.pop(choice)
            player.gold += item.gold_value // 2
            print(f"Sprzedałeś {item.name} za {item.gold_value // 2} złota.")
        else:
            print("Niepoprawny wybór.")




class Bandit(Enemy):
    def __init__(self):
        super().__init__("Bandyta", 70, 20, [Item("Miecz bandyty", "attack", 20, 25)])

class Ghost(Enemy):
    def __init__(self):
        super().__init__("Duch", 35, 10, [Item("Ektoplazma", "health", 20, 15)])

class Skeleton(Enemy):
    def __init__(self):
        super().__init__("Szkielet", 45, 12, [Item("Kościany miecz", "attack", 20, 25)])


class Wiedzący:
    def __init__(self):
        self.upgrades = {
            'health': (100, 10, "\033[92mTwoje zdrowie zwiększyło się o 10 punktów!\033[0m"),
            'attack': (140, 6, "Twoja siła ataku zwiększyła się o 6 punktów!"),
            'armor': (200, 5, "\033[94mTwój pancerz zwiększył się o 5 punktów!\033[0m")
        }

    def upgrade(self, player):
        while True:
            print("Możliwe ulepszenia:")
            for attr, (exp_cost, value, message) in self.upgrades.items():
                print(f"{attr.capitalize()}: Koszt: {exp_cost} doświadczenia, Zysk: {value} punktów")

            choice = input("Wybierz ulepszenie (health, attack, armor) lub (W)róć: ").lower()
            if choice in self.upgrades:
                exp_cost, value, message = self.upgrades[choice]
                if player.experience >= exp_cost:
                    player.experience -= exp_cost
                    if choice == 'health':
                        player.health += value
                    elif choice == 'attack':
                        player.attack += value
                    elif choice == 'armor':
                        player.armor += value
                    print(message)
                    break
                else:
                    print("Nie masz wystarczająco doświadczenia na to ulepszenie.")
            elif choice == 'w':
                break
            else:
                print("Niepoprawny wybór. Spróbuj ponownie.")


def create_event(player):
    if player.current_location == "Mroczny las":
        enemies = [
            Enemy("Goblin", 20, 6, [Item("Drewniana pałka", "attack", 12, 10), Item("Gulasz z Goblina", "health", 45, 5)]),
            Enemy("Ork", 40, 10, [Item("Miecz Orka", "attack", 18, 20)])
        ]
        if player.battle_count >= 4 and player.battle_count < 8:
            enemies.append(Enemy("Zjawa", 65, 18, [Item("Magiczny kaganek", "armor", 5, 15)]))
        
        if player.battle_count == 8:
            return Enemy("Smok", 100, 19, [Item("Odwar z języka smoka", "health", 80, 50)])
    elif player.current_location == "Nawiedzony zamek":
        enemies = [
            Enemy("Upiór", 30, 8, [Item("Przeklęty sztylet", "attack", 24, 40)]),
            Enemy("Cień", 50, 12, [Item("Mroczny płaszcz", "armor", 7, 25)]),
            Ghost(),
            Skeleton()
        ]

    event_prob = random.random()
    
    if player.battle_count >= 4:
        if event_prob < 0.11:  
            if player.gold >= 30:
                choice = input("Wpadłeś w zasadzkę bandytów! Czy chcesz zapłacić 30 złota, aby uniknąć walki? (T)ak / (N)ie: ").lower()
                if choice == 't':
                    player.gold -= 30
                    print("Zapłaciłeś 100 złota i zostałeś puszczony wolno.")
                    return None
                else:
                    print("Musisz walczyć z bandytą!")
                    return Bandit()
            else:
                print("Nie masz wystarczająco złota! Musisz walczyć z bandytą!")
                return Bandit()
        elif event_prob < 0.18:  
            choice = input("Spotkałeś wróżbitę! Czy chcesz zapłacić 10 złota za wywróżenie przyszłości? (T)ak / (N)ie: ").lower()
            if choice == 't':
                if player.gold >= 10:
                    player.gold -= 10
                    fortune = random.choice(["gain_health", "lose_health", "nothing"])
                    if fortune == "gain_health":
                        player.health += 10
                        print("Wróżbita przewiduje pomyślną przyszłość. Zyskałeś 10 punktów życia!")
                    elif fortune == "lose_health":
                        player.health -= 10
                        print("Wróżbita przewiduje mroczną przyszłość. Straciłeś 10 punktów życia!")
                    else:
                        print("Wróżbita nie widzi niczego szczególnego w Twojej przyszłości.")
                else:
                    print("Nie masz wystarczająco złota, aby zapłacić wróżbicie.")
            else:
                print("Nie skorzystałeś z usług wróżbity.")
            return None

    return random.choice(enemies)


def change_location(player):
    print("Dostępne lokacje:")
    for i, location in enumerate(player.unlocked_locations):
        print(f"{i+1}. {location}")
    choice = int(input("Wybierz numer lokacji, do której chcesz się udać: ")) - 1
    if 0 <= choice < len(player.unlocked_locations):
        player.current_location = player.unlocked_locations[choice]
        print(f"Udałeś się do: {player.current_location}")
    else:
        print("Niepoprawny wybór.")


def explore(player):
    print("Eksplorujesz mroczny las...")
    enemy_or_event = create_event(player)
    if isinstance(enemy_or_event, Enemy):
        print(f"Atakuje Cię {enemy_or_event.name}")
        return enemy_or_event
    elif enemy_or_event is None:
        print("Nic się nie wydarzyło.")
        return None

def combat(player, enemy):
    if enemy.name == "Goblin":
        print("""
            ,      ,
           /(.-""-.)\
       |\  \/      \/  /|
       | \ / =.  .= \ / |
       \( \   o\/o   / )/
        \_, '-/  \-' ,_/
          /   \__/   \
          \ \__/\__/ / 
        ___\ \|--|/ /___
      /`    \      /    `\
     /       '----'       \
        """)
    elif enemy.name == "Ork":
        print("""
           __,='`````'=/__
          '//  (o) \(o) \\ `      
         //|     ,_)   (`\\     
        // |  \__/ `---'|  \\  
       //  |   `-----' |   \\ 
      `|    \            /    |`  
       |     \  \     / /     |   
        \     '------'       /  
          \                /       
            `\          /'     
              `\_    _/'       
                 `\_/'           
        """)
    elif enemy.name == "Smok":
        print("""
                  ________
                  /  _____)
         _.----._/ /
       /         /
     __/ (  | (  |
    /__.-'|_|--|_|
        """)
    elif enemy.name == "Zjawa":
        print("""
          _____
         /     \\
        | () () |
         \\  ^  /
          |||||
          |||||
        """)
    elif enemy.name == "Bandyta":
        print("""
           __
          / _)
         / /  
        / /         .-""-.
        | |        /        \\
        | |        |        |
         \\ \\       |        |
          \\ '\\  _,-'\\        /
           \\ \\/   /  `\\    /
            \\    /     |   |
             \\   |     |    |
              \\  |     |    |
        """)

    while player.is_alive() and enemy.is_alive():
        action = input("(A)takuj lub (U)ciekaj ").lower()
        if action == 'a':
            damage = player.attack_enemy(enemy)
            if not enemy.is_alive():
                print(f"Pokonałeś {enemy.name}")
                player.gold += 10
                player.experience += 50
                loot = random.choice(enemy.loot)
                player.inventory.append(loot)
                print(f"Zdobyłeś: {loot.name}")
                player.battle_count += 1
                break
            damage = enemy.attack_player(player)
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

def open_new_terminal():
    if not os.environ.get('GAME_STARTED'):
        os.environ['GAME_STARTED'] = '1'
        os.system('start cmd /k python D:/LegendOfYss/LegendOfYss.py')

def main():
    if not os.environ.get('GAME_STARTED'):
        open_new_terminal()
        return
    print("Witaj w świecie Yss!")
    name = input("Wpisz swoją nazwę: ")
    player = Player(name)
    print(f"Witaj, {player.name}! Twoja przygoda właśnie się zaczyna!")

    while player.is_alive():
        action = input("(G)raj, (S)prawdź stan, (M)iasto, (W)ybierz broń, (A)ktywuj przedmioty, (Z)mień lokalizację, (K)oniec gry ").lower()
        if action == 'g':
            enemy = explore(player)
            if enemy:
                combat(player, enemy)
                if not player.is_alive():
                    break
                if isinstance(enemy, Enemy) and enemy.name == "Smok":
                    player.unlocked_locations.append("Nawiedzony zamek")
                    visit_city(player)
        elif action == 's':
            player.show_status()
        elif action == 'm':
            visit_city(player)
        elif action == 'w':
            player.choose_weapon()
        elif action == 'a':
            player.activate_item()
        elif action == 'z':
            change_location(player)
        elif action == 'k':
            print("Nie podołałeś?")
            break
        else:
            print("Zły klawisz. Wciśnij 'g', 's', 'm', 'w', 'a', 'z' lub 'k' ")
    
    print("Koniec gry!")


if __name__ == "__main__":
    main()