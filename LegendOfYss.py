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
            player.health = min(player.health + self.effect_value, player.max_health)
            print(f"\033[92mTwoje zdrowie zwiększyło się o {self.effect_value} punktów!\033[0m")
        elif self.effect_type == 'max_health':
            player.max_health += self.effect_value
            print(f"Twoje maksymalne zdrowie zwiększyło się o {self.effect_value}")
        elif self.effect_type == 'attack': #bronie
            player.attack += self.effect_value
            print(f"Twoja siła ataku zwiększyła się o {self.effect_value} punktów!")
        elif self.effect_type == 'armor':
            player.armor += self.effect_value
            print(f"\033[94mTwój pancerz zwiększył się o {self.effect_value} punktów!\033[0m")
        elif self.effect_type == 'attack_boost':  #dla przedmiotów
            player.attack += self.effect_value
            print(f"\033[93mTwoja siła ataku zwiększyła się o {self.effect_value} punktów!\033[0m")
        elif self.effect_type == 'lithium':
            player.lithium += self.effect_value
            player.attack += 4
            player.max_health += 8
            player.health += 8
            print("Czujesz przypływ energii")
        print(f"Zastosowano efekt przedmiotu: {self.name}")

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 400
        self.max_health = 400  
        self.attack = 300
        self.armor = 0
        self.gold = 0
        self.inventory = []
        self.active_weapon = None  
        self.experience = 0
        self.lithium = 0
        self.battle_count = 0
        self.total_battle_count = 0
        self.unlocked_locations = ["Mroczna puszcza"]
        self.current_location = "Mroczna puszcza"
        self.bestiary = Bestiary()  
        self.encyclopedia = Encyclopedia()
        self.merchant_encounters = 0 

    def revive(self):
        self.health = self.max_health
        self.gold = 0
        self.inventory = []
        self.battle_count = 0
        self.experience = 0
        self.current_location = "Miasto"
        self.current_location = "Mroczna puszcza"
        print("\033[91mZostałeś przeniesiony do miasta. Straciłeś cały ekwipunek i złoto, ale zachowałeś aktywną broń.\033[0m")

    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage, attacker):
        effective_damage = max(0, damage - self.armor)
        self.health -= effective_damage
        print(f"\033[91m{attacker.name} zadał Ci {effective_damage} obrażeń\033[0m")

    def attack_enemy(self, enemy):
        if self.active_weapon:
            base_damage = random.randint(int((self.active_weapon.effect_value + self.attack )* 0.8), self.active_weapon.effect_value + self.attack)
        else:
            base_damage = random.randint(int(self.attack * 0.8), self.attack)

        if random.random() < 0.1:  
            damage = int((base_damage + self.attack) * 1.6)
            print("\033[95mObrażenia krytyczne!\033[0m")
        else:
            damage = base_damage
        enemy.take_damage(damage)
        print(f"\033[93mZadałeś {enemy.name} {damage} obrażeń\033[0m")
        return damage

    def show_status(self):
        print(f"\n{self.name} status:")
        print(f"Zdrowie: {self.health}/{self.max_health}")  
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
        items = [item for item in self.inventory if item.effect_type in ['armor', 'health','attack_boost', 'lithium', 'max_health']]
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
    def __init__(self, name, health, attack, loot, experience, description):
        self.name = name
        self.health = health
        self.attack = attack
        self.loot = loot
        self.experience = experience
        self.description = description

    def is_alive(self):
        return self.health > 0
    
    def take_damage(self, damage):
        self.health -= damage

    def attack_player(self, player):
        base_damage = random.randint(int(self.attack * 0.8), self.attack)
        if random.random() < 0.1:  
            damage = int(base_damage * 1.6)
            print(f"\033[95m{self.name} zadaje obrażenia krytyczne!\033[0m")
        else:
            damage = base_damage
        player.take_damage(damage, self)
        return damage

class Bestiary:
    def __init__(self):
        self.entries = {}

    def add_entry(self, enemy_name, description):
        if enemy_name not in self.entries:
            self.entries[enemy_name] = description

    def display_entries(self):
        for enemy_name, description in self.entries.items():
            print(f"\n{enemy_name}: {description}")

class Encyclopedia:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def show_entries(self):
        for entry in self.entries:
            print(f"- {entry}")

def visit_city(player):
    wiedzący = Wiedzący()
    kowal = Kowal()
    print("Witaj w mieście! Możesz tu ulepszyć swoją postać lub broń, albo handlować.")
    while True:
        action = input("(W)iedzący, (K)owal, (H)andluj, (C)ofnij: ").lower()
        if action == 'w':
            wiedzący.upgrade(player)
        elif action == 'k':
            kowal.upgrade_weapon(player)
        elif action == 'h':
            visit_merchant(player)
        elif action == 'c':
            break
        else:
            print("Zły klawisz. Wciśnij 'w', 'k', 'h' lub 'c'")
            

class Kowal:
    def __init__(self):
        self.upgrade_costs = {
            1: 20,
            2: 40,
            3: 60,
            4: 80,
            5: 100
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
            player.active_weapon.effect_value += 2 * next_level  
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
        super().__init__("Bandyta", 70, 20, [Item("Miecz bandyty", "attack", 20, 25)], 60, "Bandyta")

def visit_mysterious_merchant(player):
    player.merchant_encounters += 1 
    if any(item.effect_type == "lithium" for item in player.inventory):  
        choice = input("Spotykasz tajemniczego kupca. Kapelusz z długim rondlem sprawiał, że cień padał na jego twarz. Ubrany był w lekko poszarpane szaty, przypominające strój typowego cyrulika. \nRazoth: Witaj nieznajomy, jestem Razoth, wędrowny kupiec. Myślę, że moje niezwykłe towary mogą Cię zainteresować. Ale uwaga! Przyjmuję płatność tylko w Lithium, którego myślę, że ty masz sporo. Proponuję 30 złota za każdą porcję. (T)ak / (N)ie: ").lower()
        if choice == 't':
            lithium_items = [item for item in player.inventory if item.effect_type == "lithium"]
            total_value = 30 * len(lithium_items) 
            player.gold += total_value
            player.inventory = [item for item in player.inventory if item.effect_type != "lithium"]  
            print(f"Sprzedałeś wszystkie Lithium za {total_value} złota!")

        else:
            print("Razoth: Może innym razem - odpowiada z uśmiechem.")
    else:
        print("Nie masz żadnego Lithium w ekwipunku.")

class Wiedzący:
    def __init__(self):
        self.upgrades = {
            'max_health': (100, 10, "\033[92mTwoje maksymalne zdrowie zwiększyło się o 10 punktów!\033[0m"),
            'attack': (140, 6, "Twoja siła ataku zwiększyła się o 6 punktów!"),
            'armor': (200, 5, "\033[94mTwój pancerz zwiększył się o 5 punktów!\033[0m")
        }

    def upgrade(self, player):
        while True:
            print("Możliwe ulepszenia:")
            for attr, (exp_cost, value, message) in self.upgrades.items():
                print(f"{attr.capitalize()}: Koszt: {exp_cost} doświadczenia, Zysk: {value} punktów")

            choice = input("Wybierz ulepszenie (max_health, attack, armor) lub (W)róć: ").lower()
            if choice in self.upgrades:
                exp_cost, value, message = self.upgrades[choice]
                if player.experience >= exp_cost:
                    player.experience -= exp_cost
                    if choice == 'max_health':
                        player.max_health += value
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
    enemies = []  

    if player.current_location == "Mroczna puszcza":
        enemies = [
            Enemy("Goblin", 30, 7, [Item("Drewniana pałka", "attack", 12, 10), Item("Gulasz z Goblina", "health", 20, 5)], 20,"Prymitywnie rozwinięta rasa goblinów, zamieszkuje szczególnie zalesione tereny na północny wschód od Amro. \nZdrowie: 20 \nAtak: 6"),
            Enemy("Rusałka", 25, 6, [Item("Proszek z skrzydeł Rusałki", "max_health", 2, 40)], 35, "Można je spotkać tylko w najgłębszych częściach kniei. Posiadają wrodzoną zdolność korzystania z magii.\nZdrowie: 40\nAtak: 10"),
            Enemy("La'therag", 42, 9, [Item("Lithium", "lithium", 1, 0)], 40, "Przemieniony człowiek w plugawą istotę.\nZdrowie: 45\nAtak: 6")
        ]
        if player.battle_count >= 4 and player.battle_count < 8:
            enemies.append(Enemy("Zjawa", 65, 18, [Item("Kaganek", "armor", 2, 15)], 50, "Wśród prostaczcków uważa się, że są to błądzące duchy ludzi, którzy popełnii straszliwy czyn\nZdrowie: 65\nAtak: 18"))
        
        event_prob = random.random()
        if event_prob < 0.06:  
            if player.gold >= 30:
                choice = input("Wpadłeś w zasadzkę bandyty! Czy chcesz zapłacić 30 złota, aby uniknąć walki? (T)ak / (N)ie: ").lower()
                if choice == 't':
                    player.gold -= 30
                    print("Zapłaciłeś 30 złota i zostałeś puszczony wolno.")
                    return None
                else:
                    print("Musisz walczyć z bandytą!")
                    return Bandit()
            else:
                print("Nie masz wystarczająco złota! Musisz walczyć z bandytą!")
                return Bandit()
        elif event_prob < 0.09:  
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

        if player.battle_count == 10:
            return Enemy("Pani Puszczy", 120, 21, [Item("Eliksir z krwi Pani Puszczy", "health", 80, 80)], 220, "Wiejska legenda o o potężnej wiedźmie strzerzącej swojego domu przed goścmi, okazała się prawdą\nZdrowie: 120\n Atak: 21")
    elif player.current_location == "Kręgi Świata":
        enemies = [
            Enemy("Śnieżny Troll", 150, 30, [Item("Skóra śnieżnego Trolla", "armor", 4, 120)], 180, "Wyróżniają się największą siłą wśród swojego gatunku\nZdrowie: 150\n Atak: 30"),
            Enemy("Trokowie", 120, 20, [Item("Owoce ostokrzewu", "health", 50, 80)], 130, "Góskie plemię ludzi o własnej rozbudowanej kuturze wierzeń. W lecie schodzą z gór by rabować miasteczka i wsie. W zimie zaszywają się w górach, atakując każdego podróżnika\nZdrowie: 120\n Atak: 20"),
            Enemy("Uzbrojony La'therag", 140, 35, [Item("Duża dawka Lithium", "lithium", 2, 0)], 170,"Przed przemianą był dumnym wojownikiem\nZdrowie: 140\n Atak: 35"),
            Enemy("Szkielet", 130, 40, [Item("Miecz dwuręczny", 'attack', 40, 120)], 150, "W przeklętch miejscach, umarli wstają z grobu\nZdrowie: 130\n Atak: 40"),
            Enemy("Harpia", 100, 22, [Item("Amulet z piór harpii", 'max_health', 8, 150)], 110, "Zamieszkuje wysokie partie gór, nie dostępne dla wrogów skąd wypatruje swojej ofiary\nZdrowie: 100\n Atak: 22")
        ]
        if player.battle_count == 35:
                return Enemy("Gryf", 400, 65, [Item("Odwar z języka Gryfa", "max_attack", 20, 300)], 400, "Szlachetne stworzenie będące w herbie Amro. Zabicie go było czynem okrutnym, ale niestety nieuniknionym\nZdrowie: 400\n Atak: 65")
        
        event_prob = random.random()
        if event_prob < 1:
            # choice = input("Wędrując napotykasz jękającego wędrownego rycerza, który leży oparty o drzewo.\nRycerz: Nieznajomy! Ppp... Podejdź tutaj!\nJestem zarażony. Napadły mnie La'theragi, pokonałem je, lecz jeden z nich zdążył mnie ugryźć Czuję, że za niedługo dokona się przemiana. Zakończ moją mękę. Nie chcę stać się tym czymś.\n (D)obij rycerza lub (Z)ostaw go").lower()
            # if choice == "d":
            #     print("Skracasz męki rycerza i ruszasz w dalszą drogę")
                
            # if choice == "z":
            #     print("Odwracasz się i ruszasz w dalszą drogę. Po chwili dobiegają Cię dziwne odgłosy. Odwracasz się i widzisz La'theraga biegnącego w twoją stronę")
            #     return Enemy("Uzbrojony La'therag", 140, 35, [Item("Duża dawka Lithium", "lithium", 2, 0)], 170,"Przed przemianą był dumnym wojownikiem\nZdrowie: 140\n Atak: 35")
        # elif event_prob < 14:
            visit_mysterious_merchant(player)
                
        if player.merchant_encounters == 3 and player.battle_count == 38:
            print("Na środku drogi spotykasz Tajemniczego kupca Razotha. Jego szaty są poszarpane bardziej niż były gdy go ostatnio widziałeś.  " )
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            return Enemy("Przemieniony Razoth", 600, 90, [Item("Kapelusz Razortha", 'max_attack', 20, 40), 700, "Eksperymentowanie z lithium nie popłaca" ])

    elif player.current_location == "Azar":
        enemies = [
            Enemy("La'therag Niszczyciel", 350, 60, [Item("Wielki miecz Niszczyciela", 'attack', 60, 200)], 350, "La'therag z ogromnym mieczem stworzony do zabijania"),
            Enemy("Czempion La'theragow", 450, 50, [Item("Łuska z tarczy Czempiona", 'armor', 5, 300)], 350, "Wojownik zasłaniający się ogromną trójkątną tarczą")
        ]
        if event_prob < 8:
            choice = input("Eksplorując Azar znajdujesz bogato zdobioną skrzynię.\n(O)twierasz czy (z)ostawiasz?").lower()
            if choice == 'o':
                fortune.random_choice(["Mimik", "Nagroda"])
                if fortune == "Mimik":
                    print("Skrzynia przemienia się w Mimika, który z szyderczym śmiechem atakuje Cię.")
                    return("Mimik", 460, 50, [Item("Perła z Thiedam", "max_health", 30)], 400, "Przemieniają się w różne przedmioty, zastawiając pułapkę na nieostrożnych wędrowców")
                if fortune == "Nagroda":
                    print("W skrzyni znajdujesz Perłę")
                    return Item("Perła z Thiedam", "max_health", 30)

        if player.battle_count == 40:
            print("Docierasz do pałacu w Thiedam. Najwidoczniej nie tylko ty szukałeś klejnotu. Wchodząc do wielkiej sali w pałacu widzisz La'theraga większego od innych w drogich szatach i z dużym, charakterystycznym hełmem.\n")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            print("La'therag Generał: Długo drogę pokonałeśby tu dotrzeć. Tak, my też chcemy dostać klejnot.")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            return Enemy("La'therag Generał", 500, 80, [Item("Zbroja generała","armor", 10,  500)], 800, "Potężny La'therag dowodzący innym przemienionym. Ciekawe...Czyżby La'theragi miały swoją hierarchię?\nZdrowie: 500\n Atak: 80")
    elif player.current_location == "Ghest":
        return Enemy("Przywódca La'theragów", 700, 100, [None], [None], [None])

    if enemies:  
        return random.choice(enemies)
    else:
        print("Nie znaleziono żadnych wrogów w tej lokalizacji.")
        return None
    
def compendium(player):
    action = input("(E)ncyklopedia, (B)estiariusz")
    if action == 'e':
        print("\nKrólestwo Lazoreth zostało ogarnięte plagą. Ludzie zmieniają się w przerażające istoty zwane La'theragami. Gdy zostaje zaatakowana wioska, w której mieszkasz uciekasz z innymi ocalałymi na północ do Amro - stolicy królestwa i największego miasta Bezkresnych Wyżyn. By poradzić sobie w nowym otoczeniu postanawiasz kraść. Niefortunnie wpadasz przy pewnej mniejszej akcji. Trafiasz do lochu i przed Wielki Sąd. Masz do wyboru szafot, lub wstąpienie do Oczyszczonych. Po szybkiej rachubie decydujesz się na drugą opcję. Od tamtej chwili twoja przeszłość przestaje mieć znaczenie. \n")
        print(f"Nadałeś sobie imię {player.name}.\n")
        print("Oczyszczeni to pradawny zakon mający na celu chronić ludzkość przed plagą. Wokół zakonu obrosło wiele tajemnic. Nie udzielają się publicznie a ich główna kwatera Twierdza Ghest mieści się na odludziu na wschód od Amore. Rytuał dołączenia częściowo zmienia genetykę co sprawia, że Oczyszczeni mają ograniczone emocje - łatwiej jest im podejmować decyzje, które mają na uwadze dobro królestwa. Od początku wpajają rekrutom, że La'theragi już nie są ludźmi. Szkolenie ma za zadanie wyzbyć nowicjuszy z wyrzutów sumienia, jakie mogą mieć miejsce podczas walki z przemienionymi. Wiele mieszkańców, mniejszych wiosek którzy nie wychylają nosa poza swoją oborę, traktuje Oczyszczonych tylko jako legendę.\n")
        print("Po przybyciu do twierdzy zostajesz poddany treningowi. Mimo, że nie trwa on długo, szybko przyswajasz nowe umiejętności. Twój Wiedzący (mentor) Ozahim wydobył z Ciebie w tym krótkim czasie, ogromny potencjał.")
        print("Zostajesz wysłany w podróż - twoim celem jest odnalezienie klejnotu Yss. Jego moc odpowiednio użyta ma powstrzymać plagę. Według zapisków, które od dawna studiują Skrybowie bractwa znajduje się w mieście Thiedam, które było 'perłą' dawnego królestwa Yss.\n")
        player.encyclopedia.show_entries()
    elif action == 'b':
        print("\nOpis przeciwników\n")
        player.bestiary.display_entries()

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
    print(f"Eksplorujesz {player.current_location}...")
    enemy_or_event = create_event(player)
    if isinstance(enemy_or_event, Enemy):
        print(f"Atakuje Cię {enemy_or_event.name}")
        return enemy_or_event
    elif enemy_or_event is None:
        print("Nic się nie wydarzyło.")
        return None
    
def end_game(player):
    print("Krwisto czerwony klejnot wielkości głowy, promieniuje ciepłem. Czujesz, że przyzywa Cię, chce byś się z nim zjednoczył.")
    print("1. Zabierz klejnot")
    print("2. Spróbuj pochłonąć jego moc")
    choice = input()
    if choice == '1':
        if player.lithium == 0:
            print("Zabrałeś klejnot i udałeś się w drogę powrotną do Ghest. Podróż minęła szybko i bezpiecznie. Prędko pobiegłeś spotkać się z Mistrzem Izyghorem. Gdy tylko dostał w ręce klejnot zwołał radę...")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            print("Czekasz w holu gdy nagle wbiega goniec i pędzi w kierunku sali obrad. Wchodząc do sali krzyczy o Armii La'theragów zbliżających się do twierdzy.")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
                print("To ostatnia szansa, żeby przygotować się do finałowej walki.")
                break
        else:
            print("Gdy przykładasz dłoń do kryształu, zaczyna on wciągać Cię wgłąb siebie. Próbujesz się przeciwstawić, ale jest zbyt silny. Wchłonąłeś zbyt dużo Lithium.")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            print("Otwierasz oczy. Widzisz pałac, w którym się jeszcze przed chwilą znajdowałeś, lecz nie jest on zniszczony zębem czasu. Wygląda jak za swoich najlepszych czasów. Dopiero teraz docierają do Ciebie odgłosy zabawy z wszystkich stron. Nie jesteś sam. Wokół trwa prawdziwy bal. Ludzie w pięknych, bogato zdobionych strojach tańczą, piją i ucztują. Nigdy nie widziałeś na oczy takich szat. Całkowicie się różnią od tych z twojego królestwa. Nagle zaczepia Cię ktoś. Jegomość z długą brunatną brodą i w zielonych szatach.")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            print("Bronto: Witaj! Jestem Bronto! - mówi podając Ci rękę. Widzę, że jesteś tutaj nowy. Zapewne tak jak my, chciałeś posmakować mocy klejnota! Ciekawe...dawno nikt nas nie odwiedzał. Dużo się zmienio w naszym Yss? Czekaj! Nie odpowiadaj. W sumie to nie obchodzi mnie to. Baw się z nami ile tylko zapragniesz! - woła odchodząc tanecznym krokiem.")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            print("Nie wiesz co powiedzieć. Czujesz, że pożera Cię pustka. Zawiodłeś wszystkich, któzy liczyli na Ciebie")
            exit()

    elif choice == '2':
        if player.lithium == 0:
            if player.max_health >= 400:
                print("Nie możesz się oprzeć. Masz wizję władzy i bogactwa przed oczami. Przykładasz dłoń do klejnotu. Czujesz jak topnieje pod wpływem twojego dotyku i wchłania się w twoje ciało. Czujesz się jakby krew w twoich żyłach się gotowała. Po chwili tracisz świadomość.")
                player.max_health += 300
                player.health += 300
                player.attack += 300
                while True:
                    key = input("Naciśnij 'k', aby kontynuować: ").lower()
                    if key == 'k':
                        break
                print("Nie wiesz ile czasu minęło gdy się budzisz. Czujesz w sobie coś nowego, niodkrytego. Masz wrażenie, że słyszysz szmery wkoło siebie. Jakbyś nie był tu sam. Wstajesz i kierujesz się do wyjścia. Nie możesz wrócić do Twierdzy Ghest, więc ruszasz w kierunku Amro. Gdy przybywasz do miasta okazuje się, że jest prawie opustoszałe. PRAWIE. Jedynymi jej mieszkańcami są La'theragi pozostawione do pilnowania Pałacu. Czując w sobie niezwykłą moc, stajesz z nimi do walki. Trwa ona niezwykle krótko. Miażdzysz je swoimi ciosami. Na koniec zostawiasz sobie ich kapitana.")
                while True:
                    key = input("Naciśnij 'k', aby kontynuować: ").lower()
                    if key == 'k':
                        break
                return Enemy("Kapitan La'theragów", 500, 150, [None], None, None)
            
            else:
                print("Gdy przykładasz dłoń do kryształu, zaczyna on wciągać Cię wgłąb siebie. Próbujesz się przeciwstawić, ale jest zbyt silny. Wchłonąłeś zbyt dużo Lithium.")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            print("Otwierasz oczy. Widzisz pałac, w którym się jeszcze przed chwilą znajdowałeś, lecz nie jest on zniszczony zębem czasu. Wygląda jak za swoich najlepszych czasów. Dopiero teraz docierają do Ciebie odgłosy zabawy z wszystkich stron. Nie jesteś sam. Wokół trwa prawdziwy bal. Ludzie w pięknych, bogato zdobionych strojach tańczą, piją i ucztują. Nigdy nie widziałeś na oczy takich szat. Całkowicie się różnią od tych z twojego królestwa. Nagle zaczepia Cię ktoś. Jegomość z długą brunatną brodą i w zielonych szatach.")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            print("Bronto: Witaj! Jestem Bronto! - mówi podając Ci rękę. Widzę, że jesteś tutaj nowy. Zapewne tak jak my, chciałeś posmakować mocy klejnota! Ciekawe...dawno nikt nas nie odwiedzał. Dużo się zmienio w naszym Yss? Czekaj! Nie odpowiadaj. W sumie to nie obchodzi mnie to. Baw się z nami ile tylko zapragniesz! - woła odchodząc tanecznym krokiem.")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            print("Nie wiesz co powiedzieć. Czujesz, że pożera Cię pustka. Zawiodłeś wszystkich, któzy liczyli na Ciebie")
            exit()
        else:
            print("Gdy przykładasz dłoń do kryształu, zaczyna on wciągać Cię wgłąb siebie. Próbujesz się przeciwstawić, ale jest zbyt silny. Wchłonąłeś zbyt dużo Lithium.")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            print("Otwierasz oczy. Widzisz pałac, w którym się jeszcze przed chwilą znajdowałeś, lecz nie jest on zniszczony zębem czasu. Wygląda jak za swoich najlepszych czasów. Dopiero teraz docierają do Ciebie odgłosy zabawy z wszystkich stron. Nie jesteś sam. Wokół trwa prawdziwy bal. Ludzie w pięknych, bogato zdobionych strojach tańczą, piją i ucztują. Nigdy nie widziałeś na oczy takich szat. Całkowicie się różnią od tych z twojego królestwa. Nagle zaczepia Cię ktoś. Jegomość z długą brunatną brodą i w zielonych szatach.")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            print("Bronto: Witaj! Jestem Bronto! - mówi podając Ci rękę. Widzę, że jesteś tutaj nowy. Zapewne tak jak my, chciałeś posmakować mocy klejnota! Ciekawe...dawno nikt nas nie odwiedzał. Dużo się zmienio w naszym Yss? Czekaj! Nie odpowiadaj. W sumie to nie obchodzi mnie to. Baw się z nami ile tylko zapragniesz! - woła odchodząc tanecznym krokiem.")
            while True:
                key = input("Naciśnij 'k', aby kontynuować: ").lower()
                if key == 'k':
                    break
            print("Nie wiesz co powiedzieć. Czujesz, że pożera Cię pustka. Zawiodłeś wszystkich, któzy liczyli na Ciebie")
            exit()

def ending1(player):
    player.total_battle_count == 0
    print("Przywódca pada od pchnięcia w klatkę piersiową, które przebiło jego zbroję. Łapie szybko każdy oddech jego ostatnich chwil życia. Z trudem ściąga hełm. W jego oczach powoli zanikają dwa płomienne niebieskie ogniki")
    print("Przywódca La'theragów: Kiedyś byłem lordem daleko na zachodnich ziemiach. Pewnej nocy ugościłem pod moim dachem wędrowca. Nie wiedzieliśmy, że jest zarażony. Jeszcze tej samej nocy przemienił się i ugryzł mnie gdy spałem. Rano obudziłem się cały w krwi mojej rodziny. Żona, córka i syn. Wiesz... Nie poczułem się z tym źle. Wręcz przeciwnie. Nigdy nie czułem takiego przypływu mocy jak wtedy. Czułem, że... że mogę wszystko. Odszukałem innych zarażonych. W trakcie naszej wędrówki na Amro codziennie dołączali do nas nowi zarażeni. Nigdy się nie dowieszjak to jest płonąć prawdziwym ogniem rządzy krwi.")
    while True:
            key = input("Naciśnij 'k', aby kontynuować: ").lower()
            if key == 'k':
                break
    print("Oczyszczeni dmą w trąby. Na najwyższej wieży stoi mistrz Izyghor trzymając klejnot Yss. 'W końcu' - myślisz. Wypowiada zaklęcie znalezione w książkach o starym królestwie. Klejnot zaczyna świecić blaskiem mocniejszym od słońca. Wkoło walka ustępuje. Nagle od Twierdzy przechodzi fala uderzeniowa wzbijająca obłoki kurzu na polu walki. Klejnot gaśnie i zamienia się w pył a razem z nim wszystkie La'theragi.")
    while True:
            key = input("Naciśnij 'k', aby kontynuować: ").lower()
            if key == 'k':
                break
    print("20 lat później...")
    print('"Klejnot Amro"- tak nazywa się twoje nowo otwarte muzeum. Można zobaczyć w nim na wystawie wszystkie artefakty znalezione przez Ciebie w królestwie Yss. Po pokonaniu plagi otrzymałeś tytuł Obieżyświata a twoim zadaniem zostało zbadanie starego królestwa i zebranie informacji o jego dawnych mieszkańcach i pladze. Muzeum nad którym ciężko pracowałeś jest twoim dziełem, na które poświęciłeś większość swojego życia.')

def ending2(player):
    print("Wchodzisz do sali obrad. Na ogromnym owalnym stole znajdujesz list. 'Zabarykadowaliśmy się w zamku. Armia La'theragów ciągle napiera. 2 dni temu rankiem zrobili wyłomy w murach i zdobyli miasto. Ich siła jest nie z tego świata. W działaniach musi wspierać ich sam bóg ciemności Higun, któy dał początek pladze.\nNie pozostało nam nic innego jak czekać na śmierć. Wszyscy mieszkańcy naszego królestwa szukali u nas schronienia. Twierdza Ghest padła. To koniec tej ery. Ery człowieka. \nPantosie, miej nas w swojej opiece.'")
    while True:
            key = input("Naciśnij 'k', aby kontynuować: ").lower()
            if key == 'k':
                break
    print("3 miesiące później...")
    while True:
            key = input("Naciśnij 'k', aby kontynuować: ").lower()
            if key == 'k':
                break
    print("Wędrujesz po świecie szukając odkupienia. Twoja pycha zgubiła krółestwo. Zabijając kolejne grupy La'theragów zmierzasz powoli ku drodze do szaleństwa. Głosy w twojej głowie ciągle narastają. Twoja misja dobiegnie końca gdy nikt żywy nie pozostanie na tej ziemi.")
    
    
def combat(player, enemy):
    while player.is_alive() and enemy.is_alive():
        action = input("(A)takuj lub (U)ciekaj ").lower()
        if action == 'a':
            damage = player.attack_enemy(enemy)
            if not enemy.is_alive():
                print(f"Pokonałeś {enemy.name}")
                player.gold += 10
                player.experience += enemy.experience
                if enemy.loot:
                    loot = random.choice(enemy.loot)
                    player.inventory.append(loot)
                    print(f"Zdobyłeś: {loot.name}")
                else:
                    print("Nie zdobyłeś żadnych przedmiotów.")
                if enemy.name == "Pani Puszczy":
                    player.encyclopedia.add_entry("Pani puszczy pokonana. Pierwszy etap twojej podróży został zakończony. Po wyjściu z puszczy trafiasz pod spód Kręgów Świata. Najwyższego znanego Łańcucha Górskiego. Legenda głosi, że podczas pierwszej plagi ocalali przekroczyli je i założyli nowe miasta po tej stronie gór. Oznaczałoby to, że są naszymi przodkami. ")
                elif enemy.name == "La'therag":
                    player.encyclopedia.add_entry("Lithium to substancja wydzielana przez La'theragi. Mimo swoich właściwości wzmacniających nie zaleca się jej spożywania")
                elif enemy.name == "Gryf":
                    player.encyclopedia.add_entry("Po pokonaniu Gryfa droga do krainy Yss stoi przed tobą otworem. Po wyjściu z przełęczy, widzisz w oddali rozpościerające się pagórki pokryte wyschniętą trawą. Na horyzoncie majaczy twój cel. Miasto z charakterystyczntymi wysokimi, smukłymi wieżami - Thiedam, stolica prawie zapomnianego królestwa Yss.")
                if enemy.name == "La'therag Generał":
                    end_game(player)
                if enemy.name == "Przywódca La'theragów":
                    ending1(player)
                if enemy.name == "Kapitan La'theragów":
                    ending2(player)
                player.battle_count += 1
                player.total_battle_count += 1
                player.bestiary.add_entry(enemy.name, enemy.description)
                if player.total_battle_count == 150:
                    print("Nie zdążyłeś uratować królestwa")
                    exit()
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
    if not player.is_alive():
        player.revive()
        visit_city(player)

def open_new_terminal():
    if not os.environ.get('GAME_STARTED'):
        os.environ['GAME_STARTED'] = '1'
        os.system('start cmd /k python D:/LegendOfYss/LegendOfYss.py')

def main():
    if not os.environ.get('GAME_STARTED'):
        open_new_terminal()
        return
    
    print("Królestwo Lazoreth zostało ogarnięte plagą. Ludzie zmieniają się w przerażające istoty zwane La'theragami. Gdy zostaje zaatakowana wioska, w której mieszkasz uciekasz z innymi ocalałymi na północ do Amro - stolicy królestwa i największego miasta Bezkresnych Wyżyn. By poradzić sobie w nowym otoczeniu postanawiasz kraść. Niefortunnie wpadasz przy pewnej mniejszej akcji. Trafiasz do lochu i przed Wielki Sąd. Masz do wyboru szafot, lub wstąpienie do Oczyszczonych. Po szybkiej rachubie decydujesz się na drugą opcję. Od tamtej chwili twoja przeszłość przestaje mieć znaczenie. '")
    while True:
        key = input("Naciśnij 'k', aby kontynuować: ").lower()
        if key == 'k':
            break
    
    name = input("Nadaj sobie nowe imię: ")
    player = Player(name)
    print(f"Wybierając nowe imię,  przypieczętowałeś swój los. Witaj wśród Oczyszczonych Bracie {player.name}\n")
    while True:
        key = input("Naciśnij 'k', aby kontynuować: ").lower()
        if key == 'k':
            break

    while player.is_alive():
        action = input("(G)raj, (S)prawdź stan, (T)wierdza, (B)roń, (A)ktywuj przedmioty, (Z)mień lokalizację, (K)ompedium (W)yjście").lower()
        if action == 'g':
            enemy = explore(player)
            if enemy:
                combat(player, enemy)
                if not player.is_alive():
                    player.revive()
                    visit_city(player)
                if isinstance(enemy, Enemy) and enemy.name == "Pani Puszczy":
                    print('Odblokowano nową lokalizację: "Kręgi Świata"')
                    player.unlocked_locations.append("Kręgi Świata")
                if isinstance(enemy, Enemy) and enemy.name == "Gryf":
                    print('Odblokowano nową lokalizację: "Azar"')
                    player.unlocked_locations.append("Azar")    
                if isinstance(enemy, Enemy) and enemy.name == "La'therag Generał":
                    print('Odblokowano nową lokalizację: "Ghest"')
                    player.unlocked_locations.append("Ghest")                  
        elif action == 's':
            player.show_status()
        elif action == 't':
            visit_city(player)
        elif action == 'b':
            player.choose_weapon()
        elif action == 'a':
            player.activate_item()
        elif action == 'z':
            change_location(player)
        elif action == 'k':
            compendium(player)
        elif action == 'w':
            print("Nie podołałeś?")
            break
        else:
            print("Zły klawisz. Wciśnij 'g', 's', 'm', 'w', 'a', 'z' lub 'k' ")
    
    print("Koniec gry!")


if __name__ == "__main__":
    main()

    