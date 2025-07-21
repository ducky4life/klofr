# region setup
import discord
from discord import app_commands
from discord.ext import commands
import os
import shutil
import time
import keep_alive
from dotenv import load_dotenv
from dyslexicloglog import Autocorrector

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()

client = commands.Bot(
    command_prefix=[f"!klof "],
    intents=intents)

token = os.getenv("KLOFR_TOKEN")
dictionary_dir = "text_files/dictionary"
dictionary_file = "text_files/compiled_dictionary.txt"
custom_dictionary_file = dictionary_dir + "/custom_words.txt"
backup_directory = "text_files/backups"

ac = Autocorrector()

@client.event
async def on_ready():
    print('Roboduck is ready')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="ITS KLOFR THE SHEEP!"))
    await client.tree.sync()

async def autocorrector(query:str, number:int=1, separator:str=" "):
    input_list = query.split(separator)
    if number not in [1,2,3]:
        return "please choose a number between 1 to 3 inclusive"
    
    ac_results = ac.top3(input_list)

    if number == 3:
        return ac_results
    else:
        for key in ac_results:
            for i in range(3-number):
                ac_results[key].pop(-1)
        return ac_results

async def prettify_autocorrector(query:str, number:int=1, separator:str=" "):
    ac_results = await autocorrector(query, number, separator)
    msg = ""
    for key in ac_results:
        output = []
        word_list = ac_results[key.lower()]

        for i in range(1, len(word_list)+1):
            output.append(f"{i}. {word_list[i-1]}")
        msg += f'`{key}`: {" ".join(output)}\n'
    return msg

async def send_codeblock(ctx, msg, *, view=None):
    if len(msg) > 1993:
        if len(msg) > 3993:
            first_msg = msg[:1993]
            second_msg = msg[1993:3987]
            third_msg = msg[3987:].strip()
            await ctx.send(f"```{first_msg}```")
            await ctx.send(f"```{second_msg}```")
            await ctx.send(f"```{third_msg}```")
        else:
            first_msg = msg[:1993]
            second_msg = msg[1993:].strip()
            await ctx.send(f"```{first_msg}```")
            await ctx.send(f"```{second_msg}```")
    else:
        await ctx.send(f"```{msg}```", view=view)

@client.hybrid_command()
async def baa(ctx, *, message=None):
    await ctx.message.delete()
    await ctx.send(message)
# endregion

# region autocorrect functions
async def backup_custom_dictionary():
    backup_file_name = f"{backup_directory}/custom_words_{int(time.time())}.txt"
    try:
        shutil.copyfile(custom_dictionary_file, backup_file_name)
        return(f"backed up as `{backup_file_name}`!")
    except Exception as e:
        return e

async def compile_dictionary_from_dir():
    dictionary_list = os.listdir(dictionary_dir)
    with open(dictionary_file, "w", encoding="utf-8") as compiled_dictionary:
        for txt_file in dictionary_list:
            filepath = f"{dictionary_dir}/{txt_file}"
            with open(filepath, "r", encoding="utf-8") as file:
                compiled_dictionary.write(file.read())
                compiled_dictionary.write("\n")
    return("compiled!")

async def add_to_dictionary(word):
    await backup_custom_dictionary()
    with open(custom_dictionary_file, "a", encoding="utf-8") as custom_dictionary:
        custom_dictionary.write("\n")
        custom_dictionary.write(word)
        await compile_dictionary_from_dir()
        return(f"{word} is added to dictionary!")

async def remove_from_dictionary(word):
    await backup_custom_dictionary()
    with open(custom_dictionary_file, "r", encoding="utf-8") as custom_dictionary:
        custom_dictionary_list = custom_dictionary.readlines()
        custom_dictionary_list = [word.replace("\n", "") for word in custom_dictionary_list]
        try:
            custom_dictionary_list.remove(word)
            with open(custom_dictionary_file, "w", encoding="utf-8") as custom_dictionary:
                custom_dictionary.write("\n".join(custom_dictionary_list))
            await compile_dictionary_from_dir()
        except Exception as e:
            return e
        return(f"{word} is removed from dictionary!")

async def get_custom_dictionary():
    with open(custom_dictionary_file, "r", encoding="utf-8") as custom_dictionary:
        custom_dictionary.seek(0)
        custom_dictionary_content = custom_dictionary.read()
        print(custom_dictionary_content)
        return(custom_dictionary_content)
# endregion

# region autocorrect commands
@client.hybrid_command(aliases=['ac'])
@app_commands.describe(number="an integer from 1-3 inclusive, displays top n results")
async def autocorrect(ctx, query:str="None", *, number:str="1"):
    msg = await prettify_autocorrector(query, int(number))
    await ctx.send(msg)

@client.hybrid_command()
async def compile_dictionary(ctx):
    msg = await compile_dictionary_from_dir()
    await ctx.send(msg)

@client.hybrid_command()
async def backup_dictionary(ctx):
    msg = await backup_custom_dictionary()
    await ctx.send(msg)

@client.hybrid_command()
async def add_word(ctx, word):
    msg = await add_to_dictionary(word)
    await ctx.send(msg)

@client.hybrid_command()
async def remove_word(ctx, word):
    msg = await remove_from_dictionary(word)
    await ctx.send(msg)

@client.hybrid_command()
async def get_dictionary(ctx):
    msg = await get_custom_dictionary()
    await ctx.send(f"""```
{msg}
```""")
# endregion


bot_id_list = [1186326404267266059, 839794863591260182, 944245571714170930, 1396935480284680334]
channel_id_list = [1396923821268799649]

@client.event
async def on_message(message: discord.Message):
    await client.process_commands(message)
    if message.channel.id in channel_id_list and message.author.id not in bot_id_list:
        msg = []

        msg_list = message.content.split(" ")
        for word in msg_list:
            ac_query = await autocorrector(word, 1, " ")
            ac_word = ac_query[word][0] if len(word) != 1 else word
            msg.append(ac_word)
        await message.channel.send(" ".join(msg))

keep_alive.keep_alive()
client.run(token)