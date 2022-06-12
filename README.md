# Soloq Team Analyzer
An advanced program that analyzes the soloq of players in competitive teams.
## Installation
To run the program you need the newest version of Python 3 and pip installed.
Then download the repository and type the following in the terminal:
```bash
$ pip install requirements.txt 
```
Then you must edit file named *config.json* and enter to it your **Riot API Key**
## Usage
Enter this command into the terminal to run the app in the folder which you've downloaded earlier:
```bash
$ python main.py
```
Your next step is typing the *team name* and *number of days* you want the statistics to be shown of.
At the end you have to enter the correct filename (e.g. **file.xlsx**)
## Example Usage
This is an example statistic for players of LEC Team: Fnatic - these stats are from 7 days of their soloq
### Example Input
```bash
Fnatic
7
Fnatic_7d.xlsx
```
### Example Output

![Example Output](https://media.discordapp.net/attachments/978222427626700803/985614412155080755/unknown.png)
