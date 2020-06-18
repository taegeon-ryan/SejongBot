import os
import discord
from hanspell import spell_checker
from dotenv import load_dotenv

bot = discord.Client()

@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.online, activity=discord.Game("알파 테스트"))
  print(f'{bot.user.name} - {bot.user.id}로 로그인!')

@bot.event
async def on_message(msg):
  # 메시지를 보낸 유저가 봇인 경우 무시함
  if msg.author.bot:
    return
  
  if '마춤뻡 고쳐줘' in msg.content or '맞춤법 고쳐줘' in msg.content:
    sentence = msg.content.replace('마춤뻡 고쳐줘', '').replace('맞춤법 고쳐줘', '').strip()

    try:    
      result = spell_checker.check(sentence)
      print(f'입력한 문장: {result.original}')
      print(f'교정한 문장: {result.checked}')

      if result.errors > 0:
        marked_sentence = ''
        for key, value in result.words.items():
          # <span class='violet_text'> 태그가 뜨는 오류
          if 'span' in key:
            continue

          if 'class' in key:
            i = key.find('>')
            marked_sentence += key[i+1:]
            marked_sentence += ' '
            continue

          if value > 0:
            marked_sentence += '**__' + key + '__**'
          else:
            marked_sentence += key

          marked_sentence += ' '
        print()

        # 임베드 생성
        embed = discord.Embed(title="마춤뻡", description=f'틀린 맞춤법을 {result.errors}개 확인했어요!', color=0xED2323)
        embed.add_field(name="입력한 문장", value=result.original, inline=False)
        embed.add_field(name="교정한 문장", value=marked_sentence, inline=False)
      else:
        # 공백이 입력된 경우
        if result.original == '':
          raise Exception('공백 입력')

        embed = discord.Embed(title="마춤뻡", description='틀린 맞춤법을 발견하지 못했어요!', color=0xED2323)
        embed.add_field(name="입력한 문장", value=result.original, inline=False)

    except Exception as ex:
      embed = discord.Embed(title="마춤뻡", description='명령어 처리 과정에서 오류가 발생했어요!', color=0xED2323)
      print('\033[93m' + '오류: ' + str(ex) + '\033[0m' + '\n')
    
    await msg.channel.send(embed=embed)

  if '마춤뻡 도움' in msg.content or '맞춤법 도움' in msg.content:
    embed = discord.Embed(title="마춤뻡", color=0xED2323)
    embed.add_field(name="사용법", value='맞춤법 검사를 할 문장을 입력하고 `마춤뻡 고쳐줘` 혹은 `맞춤법 고쳐줘`를 입력해 주세요.', inline=False)
    embed.add_field(name="문의", value='사용 중 버그가 발생하거나, 궁금한 사항이 있을 경우 <@242160154664108032> 에게 DM을 보내주세요.', inline=False)
    await msg.channel.send(embed=embed)

load_dotenv(verbose=True)
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)