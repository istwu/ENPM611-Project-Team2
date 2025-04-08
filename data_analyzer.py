import json
from dataclasses import dataclass
from typing import List
from typing import Any
from nameparser import HumanName
from nltk.corpus import names
import re

events_list = []
creator_set = set()
state_set = set()
label_set = set()
event_type_set = set()

def add_creator_to_global_set_and_return_creator(creator: str):
    creator_set.add(creator)
    return creator

def add_state_to_global_set_and_return_state(state: str):
    state_set.add(state)
    return state

def add_label_to_global_set_and_return_label(label: str):
    label_set.add(label)
    return label

def add_event_type_to_global_set_and_return_event_type(event_type: str):
    event_type_set.add(event_type)
    return event_type

class Event:
    event_type: str
    author: str
    event_date: str
    label: str
    comment: str

    def __init__(self, event_type: str, author: str, event_date: str, label: str, comment: str):
        self.event_type = event_type
        self.author = author
        self.event_date = event_date
        self.label = label
        self.comment = comment

    @staticmethod
    def from_dict(obj: Any) -> 'Event':
        _event_type = add_event_type_to_global_set_and_return_event_type(str(obj.get("event_type")))
        _author = add_creator_to_global_set_and_return_creator(str(obj.get("author")))
        _event_date = str(obj.get("event_date"))
        _label = add_label_to_global_set_and_return_label(str(obj.get("label"))) if obj.get("label") else None
        _comment = str(obj.get("comment")) if "comment" in obj else None
        return Event(_event_type, _author, _event_date, _label, _comment)
    
    @staticmethod
    def add_event_to_global_list_and_return_event(obj: Any) -> 'Event': 
        events_list.append(Event.from_dict(obj))
        return len(events_list) - 1

@dataclass
class Issue:
    url: str
    creator: str
    labels: List[str]
    state: str
    assignees: List[str]
    title: str
    text: str
    number: int
    created_date: str
    updated_date: str
    timeline_url: str
    events: List[int]

    def __init__(self, url: str, creator: str, labels: List[str], state: str, assignees: List[str],
                 title: str, text: str, number: int, created_date: str, updated_date: str, 
                 timeline_url: str, events: List[int]):
        self.url = url
        self.creator = creator
        self.labels = labels
        self.state = state
        self.assignees = assignees
        self.title = title
        self.text = text
        self.number = number
        self.created_date = created_date
        self.updated_date = updated_date
        self.timeline_url = timeline_url
        self.events = events

    @staticmethod
    def from_dict(obj: Any) -> 'Issue':
        _url = str(obj.get("url"))
        _creator = add_creator_to_global_set_and_return_creator(str(obj.get("creator")))
        _labels = [add_label_to_global_set_and_return_label(str(label)) for label in obj.get("labels")]
        _state = add_state_to_global_set_and_return_state(str(obj.get("state")))
        _assignees = [add_creator_to_global_set_and_return_creator(str(assignee)) for assignee in obj.get("assignees")]
        _title = str(obj.get("title"))
        _text = str(obj.get("text"))
        _number = int(obj.get("number"))
        _created_date = str(obj.get("created_date"))
        _updated_date = str(obj.get("updated_date"))
        _timeline_url = str(obj.get("timeline_url"))
        _events = [Event.add_event_to_global_list_and_return_event(event) for event in obj.get("events")]
        return Issue(_url, _creator, _labels, _state, _assignees, _title, _text, _number, _created_date, _updated_date, _timeline_url, _events)


file_contents = None
with open("poetry.json") as data_file: 
    file_contents = data_file.read()

parsed_json = json.loads(file_contents)

issue_list = []
for issue in parsed_json:
    issue_list.append(Issue.from_dict(issue))

# =====  Print the number of issues, events, and so on  ==== #

print("# of issues:", len(issue_list))
print("# of events:", len(events_list))
print("# of creators:", len(creator_set))
print("# of states:", len(state_set))
print("# of labels:", len(label_set))
print("# of event types:", len(event_type_set))
print("Is event types' set subset of label's set:", event_type_set.issubset(label_set))

# ==== Write data to text files ==== #
# Write issues
with open("text-files/issues.txt", "w", encoding="utf-8") as f:
    for issue in issue_list:
        f.write(json.dumps(issue.__dict__, indent=2) + "\n")

# Write events
with open("text-files/events.txt", "w", encoding="utf-8") as f:
    for event in events_list:
        f.write(json.dumps(event.__dict__, indent=2) + "\n")

# Write creators
with open("text-files/creators.txt", "w", encoding="utf-8") as f:
    for creator in sorted(creator_set):
        f.write(creator + "\n")

# Write states
with open("text-files/states.txt", "w", encoding="utf-8") as f:
    for state in sorted(state_set):
        f.write(state + "\n")

# Write labels
with open("text-files/labels.txt", "w", encoding="utf-8") as f:
    for label in sorted(label_set):
        f.write(label + "\n")

# Write event_types.txt
with open("text-files/event_types.txt", "w", encoding="utf-8") as f:
    for event_type in sorted(event_type_set):
        f.write(event_type + "\n")

# ==== Identiy bot and ai crators ==== #
# Load real names from NLTK
real_names = set(n.lower() for n in names.words())
def looks_human(word):
    """
    Improved check to determine if a word or prefix is likely a human name.
    """
    word = re.sub(r'[^a-zA-Z]', ' ', word).strip().lower()
    
    # Heuristic 1: Split hyphenated or camelCase into parts
    parts = re.split(r'[-_\s]', word)
    
    for part in parts:
        if len(part) < 2:
            continue

        # Heuristic 2: Check if it exists in a real name corpus
        if part in real_names:
            return True

        # Heuristic 3: Try parsing with HumanName library
        name_obj = HumanName(part)
        if name_obj.first and name_obj.first.lower() in real_names:
            return True
        if name_obj.last and name_obj.last.lower() in real_names:
            return True

    return False

bot_users = set()
ai_users = set()

for username in creator_set:
    uname = username.lower()

    # Exact suffix match
    if uname.endswith("-bot") or uname.endswith("[bot]") or uname.endswith(" bot"):
        bot_users.add(username)
    elif uname.endswith("-ai") or uname.endswith("[ai]"):
        ai_users.add(username)
    # Soft suffix match requiring validation
    elif uname.endswith("bot") and not uname.endswith(("-bot", "[bot]", " bot")):
        prefix = uname[:-3]
        if not looks_human(prefix):
            bot_users.add(username)
    elif uname.endswith("ai") and not uname.endswith(("-ai", "[ai]")):
        prefix = uname[:-2]
        if not looks_human(prefix):
            ai_users.add(username)

# Save to files
with open("text-files/bot_users.txt", "w", encoding="utf-8") as f:
    for user in sorted(bot_users):
        f.write(user + "\n")

with open("text-files/ai_users.txt", "w", encoding="utf-8") as f:
    for user in sorted(ai_users):
        f.write(user + "\n")