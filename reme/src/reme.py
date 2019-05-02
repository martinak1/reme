"""
reme.py
Discord bot.
"""

import discord
import entry

class Reme(discord.client):
    async def on_ready(self):
        print('Reme has connected to the server as: {}'.format(self.user))

    async def on_message(self, message):
        user = message.auther
        user.send(
            content="Reme received: {}".format(message.content)
        )

        entry = Entry()
        entry.from_message(message)


        user.send(
            content="""
                Reme found:
                    Content: {}
                    Users: {}
                    Created: {}
                    Executed: {}
            """.format(
                entry.content(),
                entry.users(),
                entry.created(),
                entry.executed()
            )
        )
