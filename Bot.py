import discord
from discord.ext import commands
from setting import TOKEN,appid
import requests
import time

intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

            
class SimpleView(discord.ui.View):
        foo : bool = None

        async def disable_all_items(self):
              for item in self.children:
                  item.disabled = True
              await self.message.edit(view=self)
        async def on_timeout(self) -> None:
              await self.message.channel.send("TimeOut")
              await self.disable_all_items()
        
        @discord.ui.button(label="weather now", 
                       style=discord.ButtonStyle.success)
        async def weathernow(self, interaction: discord.Interaction, button: discord.ui.Button):

            # msg = await interaction.response.send_message("https://cdn.discordapp.com/emojis/1138172643867111595.gif?size=96&quality=lossless")
            emojes = {
                "пасмурно": [":cloud:"],
                "ясно": [":sunny:"],
                "облачно с прояснениями": [":white_sun_cloud: "],
                "дождь": [":cloud_rain:"],
                "переменная облачность": [":white_sun_small_cloud: "]

            }
            city_id = 0
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                    params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
            data = res.json()
            cities = ["{} ({})".format(d['name'], d['sys']['country'])
            for d in data['list']]
            print("city:", cities)
            try:
                    city_id = data['list'][0]['id']
                    city_id = city_id
                    print("success")
            except:
                city_id = 524901
                print("fail")

            print('city_id=', city_id)
            res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            
            data = res.json()
            # print(data)
            word = data["weather"][0]['description']
            word = emojes.get(word, [])
            word =  "".join(word)
            if not word:
                print("no")
            
            # await msg.delete()
            print(s_city)
            await interaction.response.send_message(f"температура: {data['main']['temp']}° \n \t \t \t погода: {data['weather'][0]['description']} {word} \n \t \t \t макс.температура: {data['main']['temp_min']}° \n \t \t \t мини.температура: {data['main']['temp_max']}°")
            self.foo = True
            self.stop()
          
        @discord.ui.button(label="weather for 5 days", 
                       style=discord.ButtonStyle.blurple)
        async def weatherfor5days(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("sorry it still in development")
            self.foo = True
            self.stop()
            return
            # msg = await interaction.response.send_message("https://cdn.discordapp.com/emojis/1138172643867111595.gif?size=96&quality=lossless")    
            emojes = {
                "пасмурно": [":cloud:"],
                "ясно": [":sunny:"],
                "облачно с прояснениями": [":white_sun_cloud:"],
                "дождь": [":cloud_rain:"],
                "переменная облачность": [":white_sun_small_cloud:"]        

            }
            city_id = 0
            res = requests.get("http://api.openweathermap.org/data/2.5/find",
                        params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
            data = res.json()
            cities = ["{} ({})".format(d['name'], d['sys']['country'])
            for d in data['list']]
            print("city:", cities)
            try:
                    city_id = data['list'][0]['id']
                    city_id = city_id
                    print("success")
            except:
                city_id = 524901
                print("fail")
                
            print('city_id=', city_id)
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()   
        #     word = data["weather"][0]['description']
        #     word = emojes.get(word, [])
        #     word =  "".join(word)
        #     if not word:
        #         print("no")
            
            # await msg.delete()
            print(s_city)              
            self.foo = True
            self.stop()


@bot.command()
async def weatherfor5days(ctx):
        try:
                city_id = 524901
                res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
                data = res.json()
                print(data['list'])
                for i in data['list']:
                        print( i['dt_txt'], '{0:+3.0f}'.format(i['main']['temp']), i['weather'][0]['description'] )
        except Exception as e:
                print("Exception (forecast):", e)
        pass

@bot.command()
async def weather(ctx, s_city2):
      global s_city
      s_city = s_city2
      view = SimpleView(timeout=15)
#       button = discord.ui.Button(label="Clck me")
#       view.add_item(button)
      message = await ctx.send(view=view)
      view.message = message
      await view.wait()
      await view.disable_all_items()

      if view.foo is None:
            print("timeOut")

      elif view.foo is True:
            print("ok")

      else:
            print("cancell")


@weather.error
async def info_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send('sorry you need to enter city name')
        
bot.run(TOKEN)