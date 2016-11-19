import discord
from discord.ext import commands
from __main__ import settings
from cogs.utils.helpers import *
from cogs.utils import checks
import asyncio
import string
import random
import re


class AI:
	"""AI Commands
	"""
	def __init__(self, bot):
		self.bot = bot
		self.reactions = read_json(settings.resourcedir + "ai/reactions.json")
		self.questions = read_json(settings.resourcedir + "ai/questions.json")

	async def play_dota_response(self, responsename):
		dotabase = self.bot.get_cog("Dotabase")
		response = await dotabase.get_response(responsename)
		await self.bot.say(response.text)
		await dotabase.play_response(response)

	@commands.command(pass_context=True)
	async def ask(self, ctx, *, question : str=""):
		"""Answers any question you might have"""
		random.seed(question)
		for check in self.questions:
			print(check["regex"])
			if re.search(check["regex"], question):
				await self.play_dota_response(random.choice(check["responses"]))
				return
		print("didnt match anything for ask")


	async def on_message(self, message):
		if (message.author == self.bot.user) or message.content.startswith("?"):
			return

		random.seed(message.content)

		for check in self.reactions:
			if re.search(check["regex"], message.content) and (random.random() < check.get("chance", 1.0)):
				await self.bot.add_reaction(message, random.choice(check["reaction"]))
				break


def setup(bot):
	bot.add_cog(AI(bot))