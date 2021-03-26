import discord
import json
import embeds


with open("keywords.json", "r") as keywords_file:
    keywords_dictionary = json.loads(keywords_file.read())


async def add(message, keyword, value):
    keywords_dictionary[keyword] = value
    value = " ".join(message.content.split(" ")[3:])
    await message.channel.send(embed = await embeds.embed_successful_action("Keyword added. :white_check_mark:"))

    await save_keywords()

async def remove(message, keyword):
    message_removal = message.content.split(" ")[2]
    keywords_dictionary.pop(message_removal)
    await message.channel.send(embed = await embeds.embed_successful_action("Keyword removed. :white_check_mark:"))

async def list(message, keyword):
    keywords_list = ""
    for keyword in keywords_dictionary:
        keywords_list += f"{keyword} - {keywords_dictionary[keyword]}\n"
    await message.channel.send(f"`{keywords_list}`")


# save keywords to file
async def save_keywords():
    keywords_json = json.dumps(keywords_dictionary)
    with open("keywords.json", "w") as keywords_file:
        keywords_file.write(keywords_json)


async def check_keywords(message):
    for keyword in keywords_dictionary.keys():
            if message.content.__contains__(keyword):
                await message.channel.send(keywords_dictionary[keyword])
                return
