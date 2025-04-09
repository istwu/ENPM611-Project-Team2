import json
# from dataclasses import dataclass
from typing import List
from typing import Any
# from nameparser import HumanName
# from nltk.corpus import names
# import re
from data_loader import DataLoader
from model import Issue, Event

events_list = []
creator_set = set()
state_set = set()
label_set = set()
event_type_set = set()

issues:List[Issue] = DataLoader().get_issues()
events = []
creators, states, labels, event_types = set(), set(), set(), set()
for i in issues:
    events.extend(i.events)
    creators.add(i.creator)
    states.add(i.state)
    labels.update(i.labels)
for e in events:
    event_types.add(e.event_type)

# =====  Print the number of issues, events, and so on  ==== #

print("# of issues:", len(issues))
print("# of events:", len(events))
print("# of creators:", len(creators))
print("# of states:", len(states))
print("# of labels:", len(labels))
print("# of event types:", len(event_types))

# ==== Write data to text files ==== #
# # Write issues
# with open("text-files/issues.txt", "w", encoding="utf-8") as f:
#     for issue in issues:
#         f.write(json.dumps(issues, indent=2) + "\n")

# # Write events
# with open("text-files/events.txt", "w", encoding="utf-8") as f:
#     for event in events:
#         f.write(json.dumps(events, indent=2) + "\n")

# Write creators
with open("text-files/creators.txt", "w", encoding="utf-8") as f:
    for creator in sorted(creators):
        f.write(creator + "\n")

# Write states
with open("text-files/states.txt", "w", encoding="utf-8") as f:
    for state in sorted(states):
        f.write(state + "\n")

# Write labels
with open("text-files/labels.txt", "w", encoding="utf-8") as f:
    for label in sorted(labels):
        f.write(label + "\n")

# Write event_types.txt
with open("text-files/event_types.txt", "w", encoding="utf-8") as f:
    for event_type in sorted(event_types):
        f.write(event_type + "\n")

# ==== Identiy bot and ai accounts ==== #
# Load real names from NLTK
# real_names = set(n.lower() for n in names.words())
# def looks_human(word):
#     """
#     Improved check to determine if a word or prefix is likely a human name.
#     """
#     word = re.sub(r'[^a-zA-Z]', ' ', word).strip().lower()
    
#     # Heuristic 1: Split hyphenated or camelCase into parts
#     parts = re.split(r'[-_\s]', word)
    
#     for part in parts:
#         if len(part) < 2:
#             continue

#         # Heuristic 2: Check if it exists in a real name corpus
#         if part in real_names:
#             return True

#         # Heuristic 3: Try parsing with HumanName library
#         name_obj = HumanName(part)
#         if name_obj.first and name_obj.first.lower() in real_names:
#             return True
#         if name_obj.last and name_obj.last.lower() in real_names:
#             return True

#     return False

# bot_users = set()
# ai_users = set()

# for username in creator_set:
#     uname = username.lower()

#     # Exact suffix match
#     if uname.endswith("-bot") or uname.endswith("[bot]") or uname.endswith(" bot"):
#         bot_users.add(username)
#     elif uname.endswith("-ai") or uname.endswith("[ai]"):
#         ai_users.add(username)
#     # Soft suffix match requiring validation
#     elif uname.endswith("bot") and not uname.endswith(("-bot", "[bot]", " bot")):
#         prefix = uname[:-3]
#         if not looks_human(prefix):
#             bot_users.add(username)
#     elif uname.endswith("ai") and not uname.endswith(("-ai", "[ai]")):
#         prefix = uname[:-2]
#         if not looks_human(prefix):
#             ai_users.add(username)

# # Save to files
# with open("text-files/bot_users.txt", "w", encoding="utf-8") as f:
#     for user in sorted(bot_users):
#         f.write(user + "\n")

# with open("text-files/ai_users.txt", "w", encoding="utf-8") as f:
#     for user in sorted(ai_users):
#         f.write(user + "\n")