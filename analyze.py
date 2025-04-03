import json
from dataclasses import dataclass
from typing import List
from typing import Any

creator_set = set()
events_list = []

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

        # Add the author name in set
        creator_set.add(self.author)

    @staticmethod
    def from_dict(obj: Any) -> 'Event':
        _event_type = str(obj.get("event_type"))
        _author = str(obj.get("author"))
        _event_date = str(obj.get("event_date"))
        _label = str(obj.get("label")) if "label" in obj else None
        _comment = str(obj.get("comment")) if "comment" in obj else None
        return Event(_event_type, _author, _event_date, _label, _comment)
    
    @staticmethod
    def add_event(obj: Any) -> 'Event': 
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

        # Add the creator name in a set
        creator_set.add(self.creator)

    @staticmethod
    def from_dict(obj: Any) -> 'Issue':
        _url = str(obj.get("url"))
        _creator = str(obj.get("creator"))
        _labels = [str(y) for y in obj.get("labels")]
        _state = str(obj.get("state"))
        _assignees = [str(y) for y in obj.get("assignees")]
        _title = str(obj.get("title"))
        _text = str(obj.get("text"))
        _number = int(obj.get("number"))
        _created_date = str(obj.get("created_date"))
        _updated_date = str(obj.get("updated_date"))
        _timeline_url = str(obj.get("timeline_url"))
        _events = [Event.add_event(y) for y in obj.get("events")]
        return Issue(_url, _creator, _labels, _state, _assignees, _title, _text, _number, _created_date, _updated_date, _timeline_url, _events)


file_contents = None
with open("poetry.json") as data_file: 
    file_contents = data_file.read()

parsed_json = json.loads(file_contents)

issue_list = []
for issue in parsed_json:
    issue_list.append(Issue.from_dict(issue))
print("Issues:", len(issue_list))

print("Creators:", len(creator_set))

print("Events:", len(events_list))