## How to run

Prepare environment

- Install pip modules, i.e. `pip install -r requirements.txt`
- Download GCSIM executable to project root directory, i.e. `python .\scripts\download_gcsim.py`

Run project

- Copy GOOD file to `.\data\data.json`
- Change `gcsim_actions` variable in `main` function in `main.py` file
- Uncomment wich part of the code should be executed (e.g. genetic algorithm)
- Execute project, i.e. `python main.py`

## Code improvements

- Add linters
- Add virtual env for dependencies
- Usar poetry instead of pip
- Receive team name via CLI arg
