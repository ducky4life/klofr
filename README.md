# klofr

klofr is a discord.py bot for the FQ-HLL autocorrection algorithm library

### features

- compile a custom dictionary from a directory from command
- add/remove/compile/backup dictionary from command
- autocorrect words from command (/autocorrect)
- autocorrect words from channel

### usage

make sure you have [python](https://www.python.org/downloads/) installed.

1. clone the repository
   ```
   git clone https://github.com/ducky4life/klofr.git
   ```
2. move to directory
   ```
   cd klofr
   ```
3. install dependencies
   ```
   pip install -r requirements.txt
   ```
4. create .env file
   ```
   touch .env
   ```
5. put your secrets in the .env file (without the brackets: [ ])
   ```
   KLOFR_TOKEN="[your bot token]"
   ```
6. run klofr.py
   ```
   python klofr.py
   ```

### todo

- [ ] togglable channels to autorespond