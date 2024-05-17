import requests
import discord
from discord import app_commands
from discord.ext import commands

valid_categories = ["Programming", "Misc", "Dark", "Any"]

def get_jokes(bot: commands.Bot):
    @bot.tree.command(name="joke")
    @app_commands.describe(category="Choose a joke category (optional)")
    @app_commands.choices(category=[
        app_commands.Choice(name="Programming", value="Programming"),
        app_commands.Choice(name="Misc", value="Misc"),
        app_commands.Choice(name="Dark", value="Dark"),
        app_commands.Choice(name="Any", value="Any")
    ])
    async def joke(interaction: discord.Interaction, category: str = "Any"):
        # Fetch joke from the API
        try:
            response = requests.get(f'https://v2.jokeapi.dev/joke/{category}')
            response.raise_for_status()  # Will raise an HTTPError for bad responses
            joke = response.json()
            if joke['type'] == 'single':
                joke_message = joke['joke']
            else:
                joke_message = f"{joke['setup']} - {joke['delivery']}"
        except requests.RequestException as e:
            joke_message = "Failed to retrieve joke. Please try again later."

        await interaction.response.send_message(joke_message)
