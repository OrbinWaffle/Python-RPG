import random
import time

player_health = 100
dodge_chance = 10
escape_chance = 25
attack_stat = 1
hit_chance = 90
encounter_chance = 30
loot_chance = 75
temp_damage_mod = 0

monster_health = 0

inventory = []
loot_types = [("apple", 0, "HEALTH/5", False), ("powerful potion", 1, "DAMAGE_MOD/3", False), ("bomb", 2, "DAMAGE/5", False)]
interactable_types = ["Door", "Chest"]
door_types = ["door", "trapdoor", "doorway", "small arch"]
chest_descriptors = ["dusty", "old", "shiny", "metal", "cobweb-covered", "chipped", "corroded", "splintered"]
chest_types = ["chest", "dresser", "cabinet", "box", "crate", "barrel"]
monster_descriptors = ["hairy", "slimy", "grotesque", "snarling", "ugly", "dastardly"]
monster_list = ["monster", "beast", "monstrosity", "creature", "spider", "zombie", "skeleton", "ogre", "cockroach", "goblin", "vampire"]
encounter_list = ["appears", "pops out at you", "attacks you", "emerges from the shadows", "falls from the ceiling", "bursts from a nearby doorway"]
attack_list = ["lunge at", "swing your sword at", "fire your bow at", "punch", "kick", "slash at", "backhand"]
room_descriptors = ["large", "damp", "quiet", "dark", "mysterious", "ominious", "warm", "cold", "dusty", "musty", "bright", "smelly", "gaudy"]
room_types = ["room", "tower", "dining room", "hallway", "basement", "kitchen", "bedroom", "study", "bathroom", "library", "ballroom", "armory"]
interactables = []

room_descriptor = ""
room_type = ""

# yourHealth, enemyHealth, playerDamageMod

# View various statistics about the player, such as health and inventory.
def view_stats():
   print("Current HP:", player_health)
   time.sleep(0.5)
   print("Inventory: ")
   time.sleep(0.5)
   for i, item in enumerate(inventory):
      print(str(i+1) + ":", item[0][0], "x" + str(item[1]))
      time.sleep(0.25)

# Enter a new room and randomly generate its contents
def enter_room():
   global interactables
   interactables = []
   index = 0
   num_of_interactables = random.randrange(2, 6)
   while(index < num_of_interactables):
      interactable_type = interactable_types[random.randrange(0, len(interactable_types))] if not index == num_of_interactables-1 else "Door"
      if(interactable_type == "Door"):
         door_type = door_types[random.randrange(0, len(door_types))]
         r_descriptor = room_descriptors[random.randrange(0, len(room_descriptors))]
         r_type = room_types[random.randrange(0, len(room_types))]
         interactables.append((interactable_type, door_type, r_descriptor,  r_type))
      if(interactable_type == "Chest"):
         chest_descriptor = chest_descriptors[random.randrange(0, len(chest_descriptors))]
         chest_type = chest_types[random.randrange(0, len(chest_types))]
         interactables.append((interactable_type, chest_descriptor, chest_type, True))
      index += 1

# Describe a room based on the parameters contained within "interactables"
def view_room():
   global interactables
   print("\nYou are currently standing in a {0} {1}.".format(room_descriptor, room_type))
   time.sleep(0.5)
   print("You see:")
   time.sleep(0.5)
   index = 0
   while(index < len(interactables)):
      interactable = interactables[index]
      interactable_type = interactable[0]
      if(interactable_type == "Door"):
         door_type = interactable[1]
         r_descriptor = interactable[2]
         r_type = interactable[3]
         print("{0}: A {1} leading to a {2} {3}.".format(index + 1, door_type, r_descriptor, r_type))
      if(interactable_type == "Chest"):
         chest_descriptor = interactable[1]
         chest_type = interactable[2]
         empty_text = "" if interactable[3] == True else "empty "
         print("{0}: A {1}{2} {3}".format(index + 1, empty_text, chest_descriptor, chest_type))
      index += 1
      time.sleep(0.1)

def interact(index_of_interactable):
   global room_descriptor
   global room_type
   if(index_of_interactable < 0 or index_of_interactable >= len(interactables)):
      return
   interactable = interactables[index_of_interactable]
   interactable_type = interactable[0]
   if(interactable_type == "Door"):
      door_type = interactable[1]
      r_descriptor = interactable[2]
      r_type = interactable[3]
      room_descriptor = r_descriptor
      room_type = r_type
      print("You walk through the {0}...".format(door_type))
      time.sleep(0.5)
      enter_room()
   elif(interactable_type == "Chest"):
      chest_descriptor = interactable[1]
      chest_type = interactable[2]
      print("You look inside the {0} {1}...".format(chest_descriptor, chest_type))
      time.sleep(0.5)
      open_chest(index_of_interactable)

def open_chest(index):
   global interactables
   chest = interactables[index]
   chest_check = random.randrange(0, 100)
   if(chest[3] == True and chest_check <= loot_chance):
      loot_found = loot_types[random.randrange(0, len(loot_types))]
      print("You find a {0}!".format(loot_found[0]))
      if(loot_found[3] == False):
         edit_inventory(loot_found, 1)
   else:
      print("You find nothing.")      
   temp_chest = list(chest)
   temp_chest[3] = False
   interactables[index] = tuple(temp_chest)
   time.sleep(0.5)

def edit_inventory(item, amount):
   global inventory
   for i, inventory_item in enumerate(inventory):
      if(inventory_item[0] == item):
         temp_item = list(inventory_item)
         temp_item[1] += amount
         inventory[i] = tuple(temp_item)
         break
   else:
      inventory.append((item, amount))

def edit_inventory_index(index, amount):
   global inventory
   inventory_item = inventory[index]
   temp_item = list(inventory_item)
   temp_item[1] += amount
   inventory[index] = tuple(temp_item)

# Method to process a combat encounter
def combat_encounter():
   global player_health
   global monster_health

   # Randomize monster description
   descriptor = monster_descriptors[random.randrange(0, len(monster_descriptors))]
   monster = monster_list[random.randrange(0, len(monster_list))]
   encounter_text = encounter_list[random.randrange(0, len(encounter_list))]

   monster_health = random.randrange(1, 10)
   monster_attack = random.randrange(1, 10)

   time.sleep(0.5)

   print("\nSuddenly, a {0} {1} {2}!".format(descriptor, monster, encounter_text))
   time.sleep(0.5)
   while(monster_health > 0):
      print("\nThe {2} {3} has {0} HP.\nYou have {1} HP.".format(monster_health, player_health, descriptor, monster))
      made_selection = False
      while(not made_selection):
         player_action = input("What do you do? ")
         player_action = player_action.upper()
         print()
         match player_action:
            case "ATTACK":
               made_selection = True
               attack_text = attack_list[random.randrange(0, len(attack_list))]
               print("You {0} the {1} {2}!".format(attack_text, descriptor, monster))
               time.sleep(0.5)
               attack_check = random.randrange(0, 100)
               mod_attack = attack_stat + temp_damage_mod
               if(attack_check <= hit_chance):
                  print("Your hit lands and you deal {0} damage.".format(mod_attack))
                  monster_health -= mod_attack
               else:
                  print("You miss!")
               time.sleep(0.5)
            case "RUN":
               made_selection = True
               run_check = random.randrange(0, 100)
               print("You attempt to run away...")
               time.sleep(1)
               if(run_check <= escape_chance):
                  print("You escape!")
                  return
               else:
                  print("You did not escape...")         
            case "STATUS":
               view_stats()
            case "ITEM":
               select_item()
               
      if(monster_health > 0):
         print("The {0} {1} lunges at you!".format(descriptor, monster))
         time.sleep(0.5)
         dodge_check = random.randrange(0, 100)
         if(dodge_check <= dodge_chance):
            print("You dodge the attack!")
         else:
            print("The monster deals {0} damage.".format(monster_attack))
            player_health -= monster_attack
         time.sleep(0.5)
      if(player_health <= 0):
         player_dead()
   print("\nYou slay the {0} {1}!".format(descriptor, monster))

def select_item():
   print("Which item do you want to use? (type \"cancel\" to cancel.)")
   for i, item in enumerate(inventory):
      print(str(i+1) + ":", item[0][0], "x" + str(item[1]))
      time.sleep(0.25)
   player_input = input("Enter your command (Type \"help\" for a list of commands): ")
   player_input = player_input.upper()
   match player_input:
      case "cancel":
         return
      case _:
         if(player_input.isdigit()):
            selection_num = int(player_input) - 1
            use_item(inventory[selection_num][1])
            edit_inventory_index(selection_num, -1)
            print("You used a {0}!".format(inventory[selection_num][0][0]))

def use_item(item_id):
   global player_health
   global temp_damage_mod
   global monster_health
   effect = loot_types[item_id][2].split("/")
   print(effect[0], effect[1])
   match effect[0]:
      case "HEALTH":
         player_health += int(effect[1])
      case "DAMAGE_MOD":
         temp_damage_mod += int(effect[1])
      case "DAMAGE":
         monster_health -= int(effect[1])

def view_commands():
   print("Type a number to interact with the corresponding object.\nstatus: View current status.\look: repeat room description.\nquit: Exit the game.")

def player_dead():
   print("You died!")
   quit()

room_descriptor = "large"
room_type = "entryway"
enter_room()
view_room()
while(True):
   made_selection = False
   while(not made_selection):
      player_input = input("Enter your command (Type \"help\" for a list of commands): ")
      player_input = player_input.upper()
      match player_input:
         case "QUIT":
            quit()
         case "LOOK":
            view_room()
         case "STATUS":
            view_stats()
         case "HELP":
            view_commands()
         case _:
            if(player_input.isdigit()):
               made_selection = True
               selection_num = int(player_input) - 1
               interact(selection_num)
   encounter_check = random.randrange(0, 100)
   if(encounter_check <= encounter_chance):
      combat_encounter()
   view_room()