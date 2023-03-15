# Python-RPG
A simple role-playing game programmed in Python.
## General
- At any time, you may input the "help" command to see a list of available actions to you.
- You have three notable stats:
  - HP: Your current health value. If this runs out, the game ends.
  - Max HP: The maximum amount of HP you can hold. Can be increased with upgrades.
  - Attack: How much damage you will deal to enemies.
## Navigation
- Every time you enter a room, the game will provide a list of the objects in the room.
- You can type in a number to interact with said objects.
  - Chest-type objects will yield loot.
  - Door-type objects will take you to a new room.
## Items
- You can find both consumable items and permament upgrade items in chests.
- At any time, type in the "inventory" command to show a list of your currently owned items and what they do.
  - Consumables may be used in combat.
    - They have various effects, such as healing you, boosting your attack stat for the duration of the battle, etc.
  - Permament upgrades will be applied immediately.
    - These include permament health upgrades, permament damage upgrades, etc.
## Combat
- Every time you perform an action, there is a chance that a monster will spawn. Combat will be immediately initated.
  - The monster health and damage is randomized, but will become higher the more monsters you have previously killed.
  - You may attack, flee, or use an item.
    - Attacking will apply your attack stat to the monster (there is a small chance to miss)
    - Fleeing will attempt to end the battle immediately (30% chance of success)
  - After your turn, the monster will attempt to attack you.
    - This also has a small chance to miss.
  - This cycle will continue until you either defeat the monster, run, or exhaust all of your HP.
## Game Over
- The mansion stretches on endlessly, and the game will only end once your HP falls to zero.
- The game will then print out how many rooms you traversed and how many enemies you encountered before terminating.
