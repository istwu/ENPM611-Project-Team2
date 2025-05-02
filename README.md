# ENPM611 Project Application - Team 2

This is the repository for Team 2's ENPM611 (Software Engineering) project. This project analyzes GitHub issues from the [python-poetry](https://github.com/python-poetry/poetry/issues) Open Source project.

This application includes four files provided from the [original project template](https://github.com/enpm611/project-application-template):

- `data_loader.py`: Utility to load the issues from the provided data file and returns the issues in a runtime data structure (e.g., objects).
- `model.py`: Implements the data model into which the data file is loaded. The data can then be accessed by accessing the fields of objects.
- `config.py`: Supports configuring the application via the `config.json` file. 
- `run.py`: Module that will be invoked to run the application. Based on the `--feature` command line parameter, one of the three features implemented will be run.

... as well as the following files, implemented as part of Team 2's project:

- `scraper.py`: Uses the GitHub API to scrape issue data from the [python-poetry](https://github.com/python-poetry/poetry/issues) repo, and outputs it to `poetry.json`.
- `poetry.json`: JSON file containing all issue data from [python-poetry](https://github.com/python-poetry/poetry/issues).
- `data_analyzer.py`: Counts the number of issues, events, labels, etc. across `poetry.json` and writes each list to respective text files (all contained in the `text_files` folder). Also contains a function to find bot users from `event_authors.txt` and writes them to `event_authors_bots.txt`.
- `feature1.py`: Finds issues with which labels (eg. bugs, features) tend to have the largest average number of comments, and displays the top 50 in a bar graph.
- `feature2.py`: Finds the number of issue events created by each bot account (eg. github-actions\[bot\]), and displays the number of events per bot in an ordered bar graph.
- `feature3.py`: Prompts the user to input a GitHub username, then counts the total number of issues and events created by that user and prints it to the terminal. 
  - Usernames of issue/event contributors can be found in `text_files/issue_creators.txt` and `text_files/event_authors.txt`.


## Setup

To get started, clone this repository to your local machine.


### Install dependencies

In the root directory of the application, create a virtual environment.
```
pip install virtualenv
python -m venv venv
```

For Windows, activate the environment with 
```
venv/Scripts/activate
```

For MacOS/Linux, use 
```
source venv/bin/activate
```

Finally, install the dependencies.
```
pip install -r requirements.txt
```


### Update `poetry.json`

`poetry.json` was last updated on 3/24/15.

To fetch the issues created in [python-poetry](https://github.com/python-poetry/poetry/issues) since the last update, run `scraper.py` with
```
python scraper.py
```

Before execution, the script will prompt you to input a GitHub API token. (If you do not have one already, they can be generated [here](https://github.com/settings/tokens).) Note that it will take a long time to run due to the large number of issues in python-poetry, as well as the GitHub API rate limit.


### Run an analysis

To run an analysis feature, use the following command (replace `FEATURE` with 1, 2, or 3):

```
python run.py --feature FEATURE
```

Depending on the feature this will either generate a bar chart showing the results, or take a user input and output the results to the command line.

### Unit testing

Run the unit tests with
```
python -m coverage run -m unittest discover -s tests -p "test_*.py"
```

To generate a coverage report, run
```
python -m coverage report --omit="test_*"
```

Overall, the unit test suite covers the functionality of each of the 3 features, as well as `config.py`, `model.py`, and `dataloader.py`. For the feature tests, we created mock issue data and verified that each feature processes the data as expected. 

Testing has revealed a few minor bugs:
- Feature 1: In the nested for loop, there is no check if labels and events in issue are existing lists (problematic if these fields are None)
- Feature 2: Filename is not well handled 
- Feature 3: 
  - Unclear if username should be case sensitive or not (no checks for uppercase or lowercase)
  - No handling for blank username