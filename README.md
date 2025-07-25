# klofr

klofr is a discord.py bot for the FQ-HLL autocorrection algorithm library (pronounced "clover")

## hyperloglog

uses the extremely cool, [accurate, and low-memory-usage](https://github.com/shun4midx/FQ-HyperLogLog-Autocorrect/tree/main/fq_hll_py#results) autocorrect algorithm library which you can read more about [here](https://github.com/shun4midx/FQ-HyperLogLog-Autocorrect)!!! star the repository and `pip install fq-hll` or `pip install DyslexicLogLog` :D

https://github.com/shun4midx/FQ-HyperLogLog-Autocorrect

### features

- compile a custom dictionary from a directory from command
- add/remove/compile/backup/get dictionary from command
- autocorrect words from command (/autocorrect)
- autocorrect files from command (/autocorrect_file)
- autocorrect words from every message in a channel using autoresponder
- add/remove/get autorespond channels from command

### directory structure

the default dictionary `20k_shun4midx.txt` packaged can be found [here](https://github.com/shun4midx/FQ-HyperLogLog-Autocorrect/blob/main/fq_hll_py/src/fq_hll/test_files/20k_shun4midx.txt), feel free to delete it and add as many txt files as you want in the dictionary directory. custom directories and file names can be set at roughly line 20 of `klofr.py`.

```
.
├── keep_alive.py
├── klofr.py
├── requirements.txt
└── text_files
    ├── compiled_dictionary.txt
    ├── autorespond_channels.txt
    ├── backups
    │   ├── (backup files)
    └── dictionary
        ├── custom_words.txt
        ├── 20k_shun4midx.txt
        └── (other dictionary files)
```

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
5. put your secrets in the .env file (without the brackets: `[ ]`)
   ```
   KLOFR_TOKEN="[your bot token]"
   ```
6. create directory structure as shown [here](https://github.com/ducky4life/klofr?tab=readme-ov-file#directory-structure)
7. run klofr.py
   ```
   python klofr.py
   ```

### todo

- [x] togglable channels to autorespond
