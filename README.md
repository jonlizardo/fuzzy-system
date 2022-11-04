### Setup
Install poetry
```
curl -sSL https://install.python-poetry.org | python3 -
```

Make sure you have installed 3.8 or higher version of Python and install dependencies by running from the root folder of the project.

```
poetry install
```

### Tasks
Use the CLI to run the tasks, make sure you add `poetry run` at the beginning.
All task also require of a `--path` parameter to indicate the folder where both .csv are located. Assuming the names are still the same.

#### Monthly flights
```
poetry run python app.py quantexa --path ~/path/to/files monthly-flights
```

#### Frequent flyers
Use the `-t/--top` to limit the output to the top N passengers.
```
poetry run python app.py quantexa --path ~/path/to/files monthly-flights
```


#### Longest run
Use the `-x` or `--exclude` parameter to exclude countries (optional).
```
poetry run python app.py quantexa --path ~/path/to/files longest-run -x uk -x us
```

#### Flown together
Available parameters:
* `-d/--dates` to narrow down your search.
* `-m/--min-shared` to indicate the min of flights in common to be part of the list.
* `-t/--top` to limit the output to the top N passengers sharing flights.
```
poetry run python app.py quantexa --path ~/Downloads/data most-flown-together -d 2017-01-01 2017-02-01
```
