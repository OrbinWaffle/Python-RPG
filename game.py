#!/usr/bin/env python3

import random
import time

max_health = 100
player_health = 100
dodge_chance = 10
escape_chance = 30
attack_stat = 1
hit_chance = 90
encounter_chance = 30
loot_chance = 70
temp_damage_mod = 0

monster_health = 0

monsters_encountered = 0
rooms_traversed = 0

inventory = []
# name, description, item_id, effect, whether it is an instant use item
loot_types = [
   (0, "apple", "Heals for 5 HP.", "HEALTH/5", False),
   (1, "loaf of bread", "Heals for 10 HP.", "HEALTH/10", False),
   (2, "health potion", "Heals for 20 HP.", "HEALTH/20", False),
   (3, "powerful potion", "Buffs attack by 3. Lasts until the end of a battle.", "DAMAGE_MOD/3", False),
   (4, "ultra potion", "Buffs attack by 5. Lasts until the end of a battle.", "DAMAGE_MOD/5", False),
   (5, "bomb", "Instantly deals 5 damage to the enemy.", "DAMAGE/5", False),
   (6, "big bomb", "Instantly deals 10 damage to the enemy.", "DAMAGE/10", False),
   (7, "powerful ring", "Your attack stat has been permanently boosted by 1!", "PERM_DAMAGE/1", True),
   (8, "sharpening stone", "Your attack stat has been permanently boosted by 2!", "PERM_DAMAGE/2", True),
   (9, "lucky ring", "Your loot chance has been permanently increased by 3%!", "PERM_LOOT/3", True),
   (10, "red gemstone", "Your maximum HP has been permanently increased by 5!", "PERM_HEALTH/5", True),
   (11, "mysterious elixr", "Your maximum HP has been permanently increased by 10!", "PERM_HEALTH/10", True)]

# Large lists of randomized descriptors
# This way, the player will see randomized locations, monsters, etc.
interactable_types = ["Door", "Chest"]
door_types = ["door", "trapdoor", "doorway", "small arch", "secret passage", "gate", "stairwell"]
chest_descriptors = ["dusty", "old", "shiny", "metal", "cobweb-covered", "chipped", "corroded", "splintered"]
chest_types = ["chest", "dresser", "cabinet", "box", "crate", "barrel", "locker"]
monster_descriptors = ["hairy", "slimy", "grotesque", "snarling", "ugly", "dastardly", "foul"]
monster_list = ["monster", "beast", "monstrosity", "creature", "spider", "zombie", "skeleton", "ogre", "cockroach", "goblin", "vampire", "slime"]
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
   print("Room traversed: {0}".format(rooms_traversed))
   print("Monsters encountered: {0}".format(monsters_encountered))
   print("Current HP: {0}/{1}".format(player_health, max_health))
   time.sleep(0.5)
   if(monster_health > 0):
      print("Monster HP:", monster_health)
      time.sleep(0.5)
   print("Your current damage:", (attack_stat + temp_damage_mod))
   time.sleep(0.5)
   print("Inventory: ")
   print_inventory()

def print_inventory():
   print("{0:<3} {1:<20} {2:<10} {3}".format(" ", "Item", "Count", "Description"))
   time.sleep(0.25)
   for i, item in enumerate(inventory):
      print("{0:<3} {1:<20} {2:<10} {3}".format(str(i+1) + ":", item[0][1], item[1], item[0][2]))
      time.sleep(0.25)

# Enter a new room and randomly generate its contents
def enter_room():
   global interactables
   global rooms_traversed
   rooms_traversed += 1
   interactables = []
   index = 0
   # Randomize the number of interactable in the room, then create each one
   num_of_interactables = random.randrange(2, 6)
   while(index < num_of_interactables):
      # Randomize whether the interactable is a door or a chest
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
   # Loops through all the interactables and prints their information
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

# interact with a certain interactable.
# If it is a door, generate a new set of interactables.
# If it is a chest, open the chest.
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

# When the player opens a chest, this method runs a check so see if they find anything
# If they do find something, it randomly picks an item from the loot_types to give them
def open_chest(index):
   global interactables
   chest = interactables[index]
   chest_check = random.randrange(0, 100)
   print()
   if(chest[3] == True and chest_check <= loot_chance):
      loot_found = loot_types[random.randrange(0, len(loot_types))]
      print("You find a {0}!".format(loot_found[1]))
      # If it is a consumable item, add to inventory
      if(loot_found[4] == False):
         edit_inventory(loot_found, 1)
      # If it is an instant-use item, immediately apply effects
      else:
         print(loot_found[2])
         time.sleep(0.5)
         use_item(loot_found[0])
   else:
      print("You find nothing.")      
   temp_chest = list(chest)
   temp_chest[3] = False
   interactables[index] = tuple(temp_chest)
   time.sleep(0.5)

# Edits the player's inventory. Will search for a particular item and increment its count
# If the item does not already exist, add a new entry
# If the item is decremented to 0, remove it from the list
def edit_inventory(item, amount):
   global inventory
   for i, inventory_item in enumerate(inventory):
      if(inventory_item[0] == item):
         temp_item = list(inventory_item)
         temp_item[1] += amount
         inventory[i] = tuple(temp_item)
         if(inventory[i][1] == 0):
            del(inventory[i])
         break
   else:
      inventory.append((item, amount))

# Does the same as the above method, but uses an item index instead of a reference to the item itself
def edit_inventory_index(index, amount):
   global inventory
   inventory_item = inventory[index]
   temp_item = list(inventory_item)
   temp_item[1] += amount
   inventory[index] = tuple(temp_item)
   if(inventory[index][1] == 0):
      del(inventory[index])

# Method to process a combat encounter
def combat_encounter():
   global player_health
   global monster_health
   global temp_damage_mod
   global monsters_encountered

   # Randomize monster description
   descriptor = monster_descriptors[random.randrange(0, len(monster_descriptors))]
   monster = monster_list[random.randrange(0, len(monster_list))]
   encounter_text = encounter_list[random.randrange(0, len(encounter_list))]

   # Randomize monster health
   # Scale monster health and damage based on the amount of monsters already seen
   # This way, the longer the user plays, the harder the monsters get
   monster_health = random.randrange(1, 10) * int((1 + (monsters_encountered * 0.20)))
   monster_attack = random.randrange(1, 10) * int((1 + (monsters_encountered * 0.20)))
   
   monsters_encountered += 1

   time.sleep(0.5)

   print("\nSuddenly, a {0} {1} {2}!".format(descriptor, monster, encounter_text))
   time.sleep(0.5)
   while(monster_health > 0):
      print("\nThe {0} {1} has {2} HP.\nYou have {3}/{4} HP.".format(descriptor, monster, monster_health, player_health, max_health))
      made_selection = False
      while(not made_selection):
         player_action = input("What do you do? (Type \"help\" for a list of commands): ")
         player_action = player_action.upper()
         print()
         match player_action:
            case "ATTACK":
               made_selection = True
               attack_text = attack_list[random.randrange(0, len(attack_list))]
               print("You {0} the {1} {2}!".format(attack_text, descriptor, monster))
               time.sleep(0.5)
               # mod_attack is the actual damage value, adding the attack stat and any bonuses
               final_attack_val = attack_stat + temp_damage_mod
               # Do a random check to see if the player hits the enemy or not
               attack_check = random.randrange(0, 100)
               if(attack_check <= hit_chance):
                  print("Your hit lands and you deal {0} damage.".format(final_attack_val))
                  monster_health -= final_attack_val
               else:
                  print("You miss!")
               time.sleep(0.5)
            case "RUN":
               made_selection = True
               # Do a random check to see if the player successfuly runs away
               run_check = random.randrange(0, 100)
               print("You attempt to run away...")
               time.sleep(1)
               if(run_check <= escape_chance):
                  # reset bonuses and exit function
                  temp_damage_mod = 0
                  monster_health = 0
                  print("You escape!")
                  return
               else:
                  print("You did not escape...")         
            case "STATUS":
               view_stats()
            case "ITEMS":
               select_item()
               print("\nThe {0} {1} has {2} HP.\nYou have {3}/{4} HP.".format(descriptor, monster, monster_health, player_health, max_health))
            case "QUIT":
               quit()
            case "HELP":
               print("\nattack: Attack the monster.\nrun: Attempt to escape.\nstatus: View current status.\nitems: Use an item.\nquit: Exit the game.")
            
         if(monster_health <= 0):
            break
      # Monster turn
      # Monster will attack the player with a slightly randomized attack stat, provided they are still alive  
      if(monster_health > 0):
         print("The {0} {1} lunges at you!".format(descriptor, monster))
         time.sleep(0.5)
         dodge_check = random.randrange(0, 100)
         if(dodge_check <= dodge_chance):
            print("You dodge the attack!")
         else:
            final_monster_attack = random.randrange(1, monster_attack + 1)
            print("The monster deals {0} damage.".format(final_monster_attack))
            player_health -= final_monster_attack
         time.sleep(0.5)
      
      # player health check
      if(player_health <= 0):
         player_dead()
   # reset bonuses and exit function
   temp_damage_mod = 0
   print("\nYou slay the {0} {1}!".format(descriptor, monster))

# Bring up item use prompt
def select_item():
   print("Which item do you want to use?")
   print_inventory()
   player_input = input("Input its index number. (type \"cancel\" to cancel.): ")
   player_input = player_input.upper()
   match player_input:
      case "cancel":
         return
      case _:
         if(player_input.isdigit()):
            selection_num = int(player_input) - 1
            print("You used a {0}!".format(inventory[selection_num][0][1]))
            use_item(inventory[selection_num][0][0])
            edit_inventory_index(selection_num, -1)
            time.sleep(0.5)

# Resolve the effects of a particular item in the player's inventory
def use_item(item_id):
   global player_health
   global max_health
   global temp_damage_mod
   global monster_health
   global attack_stat
   global loot_chance
   effect = loot_types[item_id][3].split("/")
   match effect[0]:
      case "HEALTH":
         player_health += int(effect[1])
         if(player_health > max_health):
            player_health = max_health
      case "DAMAGE_MOD":
         temp_damage_mod += int(effect[1])
      case "DAMAGE":
         monster_health -= int(effect[1])
      case "PERM_DAMAGE":
         attack_stat += int(effect[1])
      case "PERM_LOOT":
         loot_chance += int(effect[1])
      case "PERM_HEALTH":
         max_health += int(effect[1])
         player_health += int(effect[1])

def view_commands():
   print("\nType a number to interact with the corresponding object.\nstatus: View current status.\nlook: Repeat room description.\nquit: Exit the game.")

# Print out stats and then exit program
def player_dead():
   time.sleep(0.5)
   print("\n\nYou died!")
   time.sleep(0.5)
   print("You traversed {0} rooms and encountered {1} monsters.".format(rooms_traversed, monsters_encountered))
   quit()

# Begin of main game loop

print("You find yourself in a large, mysterious mansion.")
time.sleep(0.5)
print("Explore rooms...")
time.sleep(0.5)
print("Find loot...")
time.sleep(0.5)
print("And try not to fall to the numerous creatures lurking in the shadows...")
time.sleep(0.5)
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