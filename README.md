# Krewl
## Description
Krewl is a multi purpose bot and one of its main tasks is to get real time data on covid cases.

## Local Setup
- Git clone the repository into your local machine.\
- Set up a virtual environment for the project in the same folder and then activate it.\
> For linux:
`python3 -m venv <project_name> && source <project_name>/bin/activate`
- Download the packages in the `requirements.txt` into your virtual environment\
`pip install -r requirements.txt`
- Refer to this [tutorial](https://www.writebots.com/discord-bot-token/) on how to setup your own bot and to generate a token.
- Copy and paste the token in the `env.py` file.
- Once the bot has been deployed, you can try out the below commands

## Starting Commands

| Command | Description
|---------|----------|
| `?help` | Lists out all the commands. 
| `?help <command>` | Shows the description, alias and usage of a particular command |
| `?covid <country>` | Displays the stats of a country. |

Here's an example

<img src="storage/help.png">