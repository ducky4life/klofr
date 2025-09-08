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
return_invalid_words = True
dictionary_dir = "text_files/dictionary"
dictionary_file = "text_files/compiled_dictionary.txt"
custom_dictionary_file = dictionary_dir + "/custom_words.txt"
backup_directory = "text_files/backups"
autorespond_channel_file = "text_files/autorespond_channels.txt"


ac = Autocorrector(dictionary_file)

@client.event
async def on_ready():
    print('Roboduck is ready')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="ITS KLOFR THE SHEEP!"))
    await client.tree.sync()
    global return_invalid_words
    if client.user.id == 1396935480284680334:
       return_invalid_words = False
    await compile_dictionary_from_dir()

async def autocorrector(query:str, number:int=1, separator:str="\n"):
    input_list = query.split(separator)
    if number not in [1,2,3]:
        return "please choose a number between 1 to 3 inclusive"

    global return_invalid_words
    ac_results = ac.top3(input_list, return_invalid_words=return_invalid_words).suggestions

    if number == 3:
        return ac_results
    else:
        for key in ac_results:
            for i in range(3-number):
                ac_results[key].pop(-1)
        return ac_results

async def prettify_autocorrector(query:str, number:int=1, separator:str=" "):
    input_list = query.split(separator)

    if number not in [1,2,3]:
        return "please choose a number between 1 to 3 inclusive"
            
    if separator != "\\n":
        ac_results = await autocorrector(query, number, separator)

    else: # i have no idea why passing "\n" through separator doesn't work but using the default value of "\n" does
        ac_results = await autocorrector(query, number)

    msg = ""
    for key in input_list:
        output = []
        word_list = ac_results[key]

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

@client.command()
async def baa(ctx, *, message=None):
    await ctx.message.delete()
    await ctx.send(message)

@client.hybrid_command()
async def toggle_invalid_words(ctx):
    global return_invalid_words
    return_invalid_words = not return_invalid_words
    await ctx.send(f"ok return invalid words is set to {return_invalid_words}")
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
    global ac
    ac = Autocorrector(dictionary_file)
    return("compiled!")

async def compile_dictionary_from_words(word_list, mode):
    global ac
    if mode == "add":
        ac.add_dictionary(word_list)
    elif mode == "remove":
        ac.remove_dictionary(word_list)
    return("compiled from words!")

async def add_to_dictionary(words, separator):
    await backup_custom_dictionary()
    word_list = words.split(separator)
    for word in word_list:
        with open(custom_dictionary_file, "a", encoding="utf-8") as custom_dictionary:
            custom_dictionary.write("\n")
            custom_dictionary.write(word)
    await compile_dictionary_from_words(word_list, "add")
    return(f"{words} is added to dictionary!")

async def remove_from_dictionary(words, separator):
    await backup_custom_dictionary()
    word_list = words.split(separator)
    for word in word_list:
        with open(custom_dictionary_file, "r", encoding="utf-8") as custom_dictionary:
            custom_dictionary_list = custom_dictionary.readlines()
            custom_dictionary_list = [word.replace("\n", "") for word in custom_dictionary_list]
            try:
                custom_dictionary_list.remove(word)
            except Exception as e:
                return e
        try:
            with open(custom_dictionary_file, "w", encoding="utf-8") as custom_dictionary:
                custom_dictionary.write("\n".join(custom_dictionary_list))
            await compile_dictionary_from_dir()
        except Exception as e:
            return e
        return(f"{words} is removed from dictionary!")
    
async def get_word_index(word):
    with open(custom_dictionary_file, "r", encoding="utf-8") as custom_dictionary:
        custom_dictionary_list = custom_dictionary.readlines()
        custom_dictionary_list = [word.replace("\n", "") for word in custom_dictionary_list]
    try:
        index = custom_dictionary_list.index(word)
        return f"{word} is in line {index} or sth close idk"
    except:
        return f"cant find {word}"

async def get_custom_dictionary():
    with open(custom_dictionary_file, "r", encoding="utf-8") as custom_dictionary:
        custom_dictionary.seek(0)
        custom_dictionary_content = custom_dictionary.read()
        print(custom_dictionary_content)
        return(custom_dictionary_content)
    
async def get_autorespond_channel_id():
    with open(autorespond_channel_file, "r", encoding="utf-8") as autorespond_channels:
        autorespond_channels = autorespond_channels.readlines()
        autorespond_channels_list = [id.replace("\n", "") for id in autorespond_channels]
        return(autorespond_channels_list)
    
async def add_to_autorespond_channels(channel_id:str):
    with open(autorespond_channel_file, "a", encoding="utf-8") as autorespond_channels:
        autorespond_channels.write("\n")
        autorespond_channels.write(channel_id)
    return(f"(`{channel_id}`) is added to autorespond channels!")

async def remove_from_autorespond_channels(channel_id:str):
    with open(autorespond_channel_file, "r", encoding="utf-8") as autorespond_channels:
        autorespond_channels_list = autorespond_channels.readlines()
        autorespond_channels_list = [id.replace("\n", "") for id in autorespond_channels_list]
        try:
            autorespond_channels_list.remove(channel_id)
        except Exception as e:
            return e
    try:
        with open(autorespond_channel_file, "w", encoding="utf-8") as autorespond_channels:
            autorespond_channels.write("\n".join(autorespond_channels_list))
    except Exception as e:
        return e
    return(f"(`{channel_id}`) is removed from autorespond channels!")
# endregion

# region autocorrect commands
@client.hybrid_command(aliases=['ac'], description="autocorrects a list of words from input")
@app_commands.describe(number="an integer from 1-3 inclusive, displays top n results", separator="what separates your different words, defaults to spaces")
async def autocorrect(ctx, query:str="None", number:str="1", *, separator:str=" "):
    try:
        msg = await prettify_autocorrector(query, int(number), separator)
    except ValueError: # if you use text command and dont wrap your input with quotes
        input = f"{query} {number} {separator}" if separator != " " else f"{query} {number}"
        msg = f'if using text command please wrap your input with quotes :D i.e. `"{input}"`'
    await ctx.send(msg)

@client.hybrid_command(description="autocorrects every word in a txt file")
@app_commands.describe(number="an integer from 1-3 inclusive, displays top n results", separator="what separates your different words, defaults to spaces")
async def autocorrect_file(ctx, file: discord.Attachment, number:str="1", *, separator:str=" "):
    await ctx.defer()

    if file.filename.endswith(".txt"):
        uploaded_file = f"text_files/{file.filename}"
        await file.save(uploaded_file)

        try:
            with open(uploaded_file, "r", encoding="utf-8") as input_file:
                query = input_file.read()
                msg = await prettify_autocorrector(query, int(number), separator)
            os.remove(uploaded_file)
        except Exception as e:
            msg = e
    else:
        msg = "please only upload txt files"

    await ctx.send(msg)

@client.hybrid_command(description="compiles every file inside the dictionary directory")
async def compile_dictionary(ctx):
    msg = await compile_dictionary_from_dir()
    await ctx.send(msg)

@client.hybrid_command(description="backups the custom dictionary to the backups directory")
async def backup_dictionary(ctx):
    msg = await backup_custom_dictionary()
    await ctx.send(msg)

@client.hybrid_command(description="adds a word to the custom dictionary")
@app_commands.describe(separator="what separates your different words, defaults to spaces")
async def add_word(ctx, word, separator=" "):
    msg = await add_to_dictionary(word, separator)
    await ctx.send(msg)

@client.hybrid_command(description="removes a word from the custom dictionary")
@app_commands.describe(separator="what separates your different words, defaults to spaces")
async def remove_word(ctx, word, separator=" "):
    msg = await remove_from_dictionary(word, separator)
    await ctx.send(msg)

@client.hybrid_command(description="prints out the custom dictionary")
async def get_dictionary(ctx):
    msg = await get_custom_dictionary()
    await ctx.send(f"""```
{msg}
```""")
    
@client.hybrid_command(description="tries to find a word from the custom dictionary")
async def get_word_location(ctx, word):
    msg = await get_word_index(word)
    await ctx.send(msg)

@client.hybrid_command(description="prints out a list of channel ids currently with autoresponder on")
async def get_autorespond_channels(ctx):
    msg = await get_autorespond_channel_id()
    msg = "\n".join(msg)
    await ctx.send(f"""```
{msg}
```""")
    
@client.hybrid_command(description="adds a channel to autoresponder")
async def add_autorespond_channel(ctx, channel: discord.TextChannel):
    channel_id = str(channel.id)
    msg = await add_to_autorespond_channels(channel_id)
    await ctx.send(f"{channel.name} {msg}")

@client.hybrid_command(description="removes a channel from autoresponder")
async def remove_autorespond_channel(ctx, channel: discord.TextChannel):
    channel_id = str(channel.id)
    msg = await remove_from_autorespond_channels(channel_id)
    await ctx.send(f"{channel.name} {msg}")
# endregion


bot_id_list = [839794863591260182, 944245571714170930, 1396935480284680334, 1334201497470373948, 1414634216292876308]

@client.event
async def on_message(message: discord.Message):
    await client.process_commands(message)
    channel_id_list = await get_autorespond_channel_id()
    msg = []
    if str(message.channel.id) in channel_id_list and message.author.id not in bot_id_list:

        content = message.content
        msg_list = content.split(" ")
        
        if not content.startswith("!"): # dont autocorrect when using commands lol

            # for dyslexicloglog version < 1.2.1

            # for word in msg_list:
            #     ac_query = await autocorrector(word, 1, " ")
            #     if len(word) != 1:
            #         try:
            #             ac_word = ac_query[word][0]
            #         except:
            #             ac_word = word
            #     else:
            #         ac_word = word
            #     msg.append(ac_word)

            ac_query = await autocorrector(content, 1, " ")
            for word in msg_list:
                try:
                    ac_word = ac_query[word][0]
                    if ac_word == '':
                        ac_word = word
                except:
                    ac_word = word
                msg.append(ac_word)

            try:
                await message.channel.send(" ".join(msg))
            except:
                pass
        
@client.event
async def on_command_error(ctx, error):
    channel_id = 1131914463277240361
    channel = client.get_channel(channel_id)
    await channel.send(error)
    await channel.send(error.__traceback__)


keep_alive.keep_alive()
client.run(token)
