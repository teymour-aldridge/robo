import discord


async def embed_error_message(embed_description):
    return discord.Embed(
        title = "ERROR:",
        colour = discord.Colour.dark_red(),
        description = embed_description,
    )

async def embed_successful_action(embed_description):
    return discord.Embed(
        title = "Success!",
        colour = discord.Colour.green(),
        description = embed_description,
    )

async def embed_response(embed_title, embed_description):
    return discord.Embed(
        title = embed_title,
        colour = discord.Colour(0x9dacc4),
        description = embed_description,
    )

