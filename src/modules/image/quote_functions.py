import discord
import random
import io
import os
from PIL import Image, ImageDraw, ImageFont

from data import data
from methods import wrap
import verbose.embeds


class MissingQuoteMessageError(Exception):
    """ raised if user has not specified a message for their quote """


class Quote:
    """ used to initialize all of the quote-related fields, put all the fields together in a BytesIO object (which acts like a file but is stored in memory) and send it on discord """
    def __init__(self, message, image_options, image, font, quote_location_x, quote_location_y, font_colour, max_chars_per_line):
        self.message = message

        try:
            self.quote_message = message.content.split('"')[1]
        except IndexError:
            raise MissingQuoteMessageError("Need to specify a quote message.")

        try:
            self.quote_author = message.content.split('"')[3]
        except IndexError:
            self.quote_author = ""

        self.image_options = image_options
        self.image = image
        self.font = font
        self.quote_location_x = quote_location_x
        self.quote_location_y = quote_location_y
        self.font_colour = font_colour
        self.max_chars_per_line = max_chars_per_line
        self.quote_message_wrap = wrap(
            self.quote_message, self.max_chars_per_line)
        self.image_file = io.BytesIO()
        self.quote_content = self.get_quote_content()

    def get_quote_content(self):
        """ gets the message that will go inside the quote """
        if self.quote_author == "":
            return f'"{self.quote_message_wrap}"'

        return f'"{self.quote_message_wrap}" \n                    - {self.quote_author}'

    async def send_quote(self):
        await self.message.channel.send(file=discord.File(self.image_file, "image.png"))

    async def generate_quote(self):
        """ puts together all the pieces of the quote like the image, content, font etc., puts them together and saves it in a BytesIO object stored in memory. """
        image_with_message = ImageDraw.Draw(self.image)
        image_with_message.text((self.quote_location_x, self.quote_location_y), self.quote_content, (
            self.font_colour, self.font_colour, self.font_colour), font=self.font)
        self.image.save(self.image_file, "PNG")
        self.image_file.seek(0)

        await self.send_quote()


async def execute_quote_command(message):
    try:
        image_type = message.content.split(" ")[2]
    except IndexError:
        await message.channel.send(embed=verbose.embeds.embed_error_message("Incomplete command."))

    if image_type == "colour":
        image_options = os.listdir(f"{data.ROOT_FILE_PATH}/res/quote_images/colourful")
        image = Image.open(
            f"{data.ROOT_FILE_PATH}/res/quote_images/colourful/{image_options[random.randint(0, len(image_options) - 1)]}")
        font = ImageFont.truetype(
            f"{data.ROOT_FILE_PATH}/res/quote_images/fonts/Kiss_Boom.ttf", 130)

        try:
            new_quote = Quote(message, image_options, image, font, 300, 200, 0, 25)
        except MissingQuoteMessageError:
            await message.channel.send(embed=verbose.embeds.embed_error_message("Must specify a quote message."))
            return

        async with message.channel.typing():
            await new_quote.generate_quote()

    elif image_type == "grey":
        image_options = os.listdir(f"{data.ROOT_FILE_PATH}/res/quote_images/greyscale")
        image = Image.open(
            f"{data.ROOT_FILE_PATH}/res/quote_images/greyscale/{image_options[random.randint(0, len(image_options) - 1)]}")
        font = ImageFont.truetype(
            f"{data.ROOT_FILE_PATH}/res/quote_images/fonts/CaviarDreams.ttf", 50)

        try:
            new_quote = Quote(message, image_options, image, font, 800, 200, 180, 20)
        except MissingQuoteMessageError:
            await message.channel.send(embed=verbose.embeds.embed_error_message("Must specify a quote message."))
            return

        async with message.channel.typing():
            await new_quote.generate_quote()

    else:
        await message.channel.send(embed=verbose.embeds.embed_error_message("You must specify a valid image type ('grey' or 'colour')"))

