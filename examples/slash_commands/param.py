import disnake
from disnake.ext import commands
from disnake.ext.commands import Param

bot = commands.Bot("!")

# disnake can use a fastapi-like option syntax.
# That means instead of using the options keyword you will be
# setting the default of your parameters.
# It should allow you to create more readable commands and make the more complicated
# features easier to use.
# Not only that but using Param even adds support for a ton of other features.

# We create a new command with two options: required (a requistring) and optional (an integer).
# Param takes care of parsing the annotation and adding a description for it.
# If you want to provide a default value and make the option optional simply provide it as the first argument.
# "description" may be shortened to "desc" if you so choose.
@bot.slash_command()
async def simple(
    inter: disnake.ApplicationCommandInteraction,
    required: str = Param(description="The required argument"),
    optional: int = Param(0, desc="The optional argument"),
):
    ...


# To make an option required don't provide a default or set it to "..."
# Callable defaults are allowed too, in this case it defaults to the author.
@bot.slash_command()
async def defaults(
    inter: disnake.ApplicationCommandInteraction,
    required: str = Param(desc="a"),
    also_required: str = Param(..., desc="b"),
    member: str = Param(lambda inter: inter.author),
):
    ...


# Names are automatically discerned from the parameter name ("_" are changed to "-")
# However you may want to provide your own name in some cases.
@bot.slash_command()
async def names(
    inter: disnake.ApplicationCommandInteraction, 
    class_: str = Param(name="class", desc="Your class")
):
    ...


# Not all types are currently supported by discord, you may use converters in these cases.
# Both old command converters using annotations and converters using functions are supported.
# However converters which are not consistent with the actual type are not allowed.
# That means no Converter classes and no fuckery like clean_content may be used in an annotation.
@bot.slash_command()
async def converters(
    inter: disnake.ApplicationCommandInteraction,
    emoji: disnake.Emoji = Param(desc="An emoji"),
    content: str = Param(desc="Clean content", converter=lambda inter, arg: arg.replace("@", "\\@")),
):
    ...


# converters may also dictate the type of the option
# (In case no annotation is present the code falls back to the normal annotation)
def get_username(inter, user: disnake.User) -> str:
    return user.name + '#' + user.discriminator # str(user) is better here but shhhh

@bot.slash_command()
async def advanced_converters(
    inter: disnake.ApplicationCommandInteraction,
    username: str = Param(name="user", desc="A user", conv=get_username)
):
    ...

# Enumeration (choices) is allowed using enum.Enum, commands.option_enum or Literal
# The user will see the enum member name or the dict key and the bot will receive the value.
from enum import Enum
from typing import Literal


class Color(int, Enum):
    red = 0xe74c3c
    green = 0x2ecc71
    blue = 0x3498db
    yellow = 0xfee75c



Gender = commands.option_enum(["Male", "Female", "Other", "Prefer Not To Say"])
Language = commands.option_enum({"English": "en", "French": "fr", "Spanish": "es"})


@bot.slash_command()
async def enumeration(
    inter: disnake.ApplicationCommandInteraction,
    color: Color = Param(desc="Your favorite color"),
    gender: Gender = Param(desc="Your gender"),
    language: Language = Param(desc="Your language"),
    mode: Literal[1, 2, 3] = Param(desc="Mode of your choosing"),
):
    ...


# Specific types may be required of the user.
# If they provide the wrong one a BadArgument exception is raised.
@bot.slash_command()
async def verify(
    inter: disnake.ApplicationCommandInteraction, 
    channel: disnake.TextChannel = Param(desc="a TEXT channel")
):
    ...


@verify.error
async def on_verify_errror(inter, exception):
    if isinstance(exception, commands.ChannelNotFound):
        await inter.response.send_message("The channel must be a text channel")
        return
    ...
