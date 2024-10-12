import json
import sys
import random
from typing import List, Optional
from enum import Enum


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Statistic:
    def __init__(self, name: str, value: int = 0, description: str = "", min_value: int = 0, max_value: int = 100):
        self.name = name
        self.value = value
        self.description = description
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self):
        return f"{self.name}: {self.value}"

    def modify(self, amount: int):
        self.value = max(self.min_value, min(self.max_value, self.value + amount))


class Character:
    def __init__(self, name: str = "Bob"):
        self.name = name
        self.health = Statistic("Health", 100, description="Tracks remaining health", min_value=0, max_value=100)
        self.strength = Statistic("Strength", description="Strength is a measure of physical power.")
        self.intelligence = Statistic("Intelligence", description="Barbie's sparkling genius!")
        self.glamour_points = 0  #initialize glamour points to zero 
        # Add more stats as needed

    def __str__(self):
        return f"Character: {self.name}, Strength: {self.strength}, Intelligence: {self.intelligence}"

    def get_stats(self):
        return [self.strength, self.intelligence, self.glamour_points]  # Extend this list if there are more stats
    
    def gain_glamour(self, amount: int):
        """Increase Barbies Glamour Points."""
        self.glamour_points += amount
        print(f"{self.name} just had a total glamour boost! They collected {amount} Glamour Points. Total Glamour Points: {self.glamour_points}")

# rushi 10/11
    def take_damage(self, damage: int):
        self.health.modify(-damage)
        print(f"Oh no!💔 {self.name} took {damage} damage. Remaining health: {self.health.value}")
        if self.health.value <= 0:
            print(f"{self.name} has been totes defeated! Time for a relaxing day to recover...")
# rushi 10/11
    def check_stats(self):
        print(f"Stats for {self.name}:")
        print(f"Health: {self.health.value}")
        print(f"Strength: {self.strength.value}")
        print(f"Intelligence: {self.intelligence.value}")
        print(f"Glamour Points: {self.glamour_points}")

class Enemy:
    def __init__(self, name: str, health: int = 100, strength: int = 10):
        self.name = name 
        self.health = Statistic("Health", health, description="Enemy's health", min_value=0, max_value=100)
        self.strength = Statistic("Strength", strength, description="Enemy's Strength")
    
    def __str__(self):
        return f"Enemy: {self.name}, Health: {self.health}, Strength: {self.strength}"
    
    def take_damage(self, damage: int):
        """Enemy takes damage and decreases health"""
        self.health.modify(-damage)
        if self.health.value <= 0:
            print(f"{self.name} has been defeated!")
    
    def attack(self, target):
        """Enemy attacks a target (character). """
        print(f"{self.name} attacks {target.name} for {self.strength.value} damage!")
        target.take_damage(self.strength.value)


class Event:
    def __init__(self, data: dict):
        self.primary_attribute = data['primary_attribute']
        self.secondary_attribute = data['secondary_attribute']
        self.prompt_text = data['prompt_text']
        self.pass_message = data['pass']['message']
        self.fail_message = data['fail']['message']
        self.partial_pass_message = data['partial_pass']['message']
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser):
        print(self.prompt_text)
        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat)

    def resolve_choice(self, character: Character, chosen_stat: Statistic):
        if chosen_stat.name == self.primary_attribute:
            self.status = EventStatus.PASS
            print(self.pass_message)
        elif chosen_stat.name == self.secondary_attribute:
            self.status = EventStatus.PARTIAL_PASS
            print(self.partial_pass_message)
        else:
            self.status = EventStatus.FAIL
            print(self.fail_message)


class Location:
    def __init__(self, events: List[Event]):
        self.events = events

    def get_event(self) -> Event:
        return random.choice(self.events)


class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location]):
        self.parser = parser
        self.party = characters
        self.locations = locations
        self.continue_playing = True

    def get_valid_input(self, prompt: str, valid_choices: List[int]) -> int: #rushi 10/12
        while True:
            try:
                choice = int(input(prompt))
                if choice in valid_choices:
                    return choice
                else:
                    print(f"Pretty please, enter a valid choice: {valid_choices}")
            except ValueError:
                print("Not quite right! Please enter a number. ♡ ")

    def start(self): # rushi 10/11
        while self.continue_playing:
            print("🎉 Welcome to Barbie's Adventure! 🎉")
            print("What would you like to do?")
            print("1. Check Player Stats")
            print("2. Gain Glamour Points ✨")
            print("3. Simulate a Fight")
            print("4. Exit Game 😔")
            # add manage inventory option number 5 right here
            choice = self.get_valid_input("Enter your number!: ", [1, 2, 3, 4, 5])

            if choice == 1:
                for character in self.party:
                    character.check_stats()

            elif choice == 2:
                amount = int(input("Enter the amount of glamour points to gain: "))
                for character in self.party:
                    character.gain_glamour(amount)

            elif choice == 3:
                enemy = Enemy(name="Glamazon", health=80, strength=15)
                print(f" {enemy.name} appeared! 🌟")
                damage = enemy.strength.value
                for character in self.party:
                    character.take_damage(damage)
                    if character.health.value <= 0:
                        print(f"{character.name} lost all of their sparkle! 🚫")
                print("The battle has ended!")
                
            elif choice == 4:
                # Exit game
                print("Thanks for playing! 💖 See you next time!")
                self.continue_playing = False
            else:
                print("That's not quite right. Please try again.")
        print("Game Over.")

    def check_game_over(self):
        return len(self.party) == 0


class UserInputParser:
    def parse(self, prompt: str) -> str:
        return input(prompt)

    def select_party_member(self, party: List[Character]) -> Character:
        print("Choose a party member:")
        for idx, member in enumerate(party):
            print(f"{idx + 1}. {member.name}")
        choice = int(self.parse("Enter the number of the chosen party member: ")) - 1
        return party[choice]

    def select_stat(self, character: Character) -> Statistic:
        print(f"Choose a stat for {character.name}:")
        stats = character.get_stats()
        for idx, stat in enumerate(stats):
            print(f"{idx + 1}. {stat.name} ({stat.value})")
        choice = int(self.parse("Enter the number of the stat to use: ")) - 1
        return stats[choice]


def load_events_from_json(file_path: str) -> List[Event]:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return [Event(event_data) for event_data in data]


def start_game():
    parser = UserInputParser()
    characters = [Character(f"Character_{i}") for i in range(3)]

    # Load events from the JSON file
    events = load_events_from_json('project_code/location_events/location_1.json')

    locations = [Location(events)]
    game = Game(parser, characters, locations)
    game.start()


if __name__ == '__main__':
    start_game()
