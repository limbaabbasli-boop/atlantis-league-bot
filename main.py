import os
import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)
bot.remove_command('help')

user_levels = {} 

SAHIB_ID = 153887690437529761 
QEYDIYYATSIZ_ROL_ID = 1567404022795600024
QEYDIYYATLI_ROL_ID = 1567403934186733580
SABIT_KANAL_ID = 1567220696319266967

SHIP_KART_RESIM = "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1000&auto=format&fit=crop"
LEVEL_UP_RESIM = "https://images.unsplash.com/photo-1534447677768-be436bb09401?q=80&w=1000&auto=format&fit=crop"

@bot.event
async def on_ready():
    print(f'Deltac Bot tam gücü ilə işə düşdü!')
    try:
        synced = await bot.tree.sync()
        print(f"Slash komutlar sinxronizasiya olundu: {len(synced)} komut.")
    except Exception as e:
        print(f"Xəta: {e}")
    await bot.change_presence(activity=discord.Game(name="Deltac | /yardim"))

@bot.event
async def on_member_join(member):
    rol = member.guild.get_role(QEYDIYYATSIZ_ROL_ID)
    if rol:
        try:
            await member.add_roles(rol)
        except:
            pass

    kanal = member.guild.get_channel(SABIT_KANAL_ID)
    if kanal:
        embed = discord.Embed(
            title="Ailəmizə xoş gəldin!",
            description=f"<a:hosgeldin:1567411922012348447> **{member.mention}**!\n\nServerimizə qoşulduğun üçün çox sevindik!",
            color=0x151515
        )
        embed.set_image(url=SHIP_KART_RESIM)
        embed.add_field(name="İstifadəçi", value=f"{member.name} (`{member.id}`)", inline=False)
        await kanal.send(embed=embed)

@bot.event
async def on_member_remove(member):
    kanal = member.guild.get_channel(SABIT_KANAL_ID)
    if kanal:
        embed = discord.Embed(
            title="Üzv Ayrıldı",
            description=f"<a:uzgun:1567412245892169800> **{member.name}** serverdən ayrıldı. Güle güle...",
            color=0x992d22
        )
        embed.set_image(url=SHIP_KART_RESIM)
        embed.add_field(name="İstifadəçi", value=f"{member.name}", inline=False)
        await kanal.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    uid = message.author.id
    if uid not in user_levels:
        user_levels[uid] = [0, 1] 
    
    user_levels[uid][0] += 1
    mesaj_sayisi = user_levels[uid][0]
    gercek_level = user_levels[uid][1]

    yeni_level = mesaj_sayisi // 10 + 1
    if yeni_level > gercek_level:
        user_levels[uid][1] = yeni_level
        rank_kanal = discord.utils.get(message.guild.text_channels, name="rank-up")
        if rank_kanal:
            embed = discord.Embed(
                description=f"**{message.author.display_name}** Yeni səviyyəyə çatdı! Səviyyə **{yeni_level}**", 
                color=0x111111
            )
            embed.set_image(url=LEVEL_UP_RESIM)
            await rank_kanal.send(embed=embed)

    mesaj = message.content.lower()
    if "külbaş" in mesaj or bot.user.mentioned_in(message):
        sert_laflar = [
            "Ağzına soxsam boğularsane, heç danışma gecə-gecə.",
            "O sözü özünə saxla, balacalar sənə girir daha çox o gün gördük sizi.",
            "A kişi, sənə söz deyənə qədər adam özünə çay qoyub içər, kəs səsin."
        ]
        await message.channel.send(random.choice(sert_laflar))

    elif "salam" in mesaj:
        await message.channel.send("Aleykum salam, nə var nə yox?")

    await bot.process_commands(message)

@bot.command(name="level", aliases=["lvl"])
async def level_komut(ctx, member: discord.Member = None):
    target = member or ctx.author
    data = user_levels.get(target.id, [0, 1])
    embed = discord.Embed(title="Deltac Səviyyə Sistemi", description=f"👤 **{target.display_name}**\n📊 Səviyyə: **{data[1]}**\n💬 Mesaj Sayı: **{data[0]}**", color=0x111111)
    embed.set_image(url=LEVEL_UP_RESIM)
    await ctx.send(embed=embed)

@bot.tree.command(name="level", description="İstifadəçinin səviyyəsinə baxır")
async def slash_level(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    data = user_levels.get(target.id, [0, 1])
    embed = discord.Embed(title="Deltac Səviyyə Sistemi", description=f"👤 **{target.display_name}**\n📊 Səviyyə: **{data[1]}**\n💬 Mesaj Sayı: **{data[0]}**", color=0x111111)
    embed.set_image(url=LEVEL_UP_RESIM)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="levelqur", description="Yalnız sahib tərəfindən səviyyə tənzimləyir")
async def slash_levelqur(interaction: discord.Interaction, hedef: discord.Member, yeni_level: int):
    if interaction.user.id != SAHIB_ID:
        await interaction.response.send_message("A kişi, bu komutu yalnız server sahibi işlədə bilər!", ephemeral=True)
        return
    
    if hedef.id not in user_levels:
        user_levels[hedef.id] = [0, yeni_level]
    else:
        user_levels[hedef.id][1] = yeni_level
        
    embed = discord.Embed(title="Deltac Səviyyə Tənzimləndi", description=f"⚙️ **{hedef.display_name}** adlı istifadəçinin səviyyəsi **{yeni_level}** olaraq dəyişdirildi.", color=0x111111)
    embed.set_image(url=LEVEL_UP_RESIM)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="yardim", description="Deltac Komut siyahısı")
async def slash_yardim(interaction: discord.Interaction):
    embed = discord.Embed(title="Deltac - Komutlar", color=0x111111)
    embed.description = "• `/qeydiyyat` / `.qeydiyyat`\n• `/qver` / `.qver`\n• `/ban` / `.ban`\n• `/mute` / `.mute`\n• `/level` / `.level`\n• `/levelqur` (Sahib)\n• `/ship`\n• `/mafia`\n• `/temizle`"
    embed.set_image(url=SHIP_KART_RESIM)
    await interaction.response.send_message(embed=embed)

@bot.command(name="yardim", aliases=["help"])
async def yardim(ctx):
    embed = discord.Embed(title="Deltac - Komutlar", color=0x111111)
    embed.description = "• `.qeydiyyat`\n• `.qver`\n• `.ban`\n• `.mute`\n• `.level`\n• `.ship`\n• `.mafia`\n• `.temizle [sayı]`"
    embed.set_image(url=SHIP_KART_RESIM)
    await ctx.send(embed=embed)

@bot.command(name="qeydiyyat", aliases=["qeq"])
@commands.has_permissions(manage_roles=True)
async def qeydiyyat(ctx, member: discord.Member, *, isim: str):
    q_rol = ctx.guild.get_role(QEYDIYYATLI_ROL_ID)
    sz_rol = ctx.guild.get_role(QEYDIYYATSIZ_ROL_ID)
    if q_rol: await member.add_roles(q_rol)
    if sz_rol and sz_rol in member.roles: await member.remove_roles(sz_rol)
    
    embed = discord.Embed(title="Qeydiyyat Uğurlu", description=f"✅ **{member.display_name}** -> **{isim}** olaraq qeydiyyatdan keçdi.", color=0x111111)
    embed.set_image(url=SHIP_KART_RESIM)
    await ctx.send(embed=embed)

@bot.tree.command(name="qeydiyyat", description="İstifadəçini qeydiyyatdan keçirir")
async def slash_qeydiyyat(interaction: discord.Interaction, member: discord.Member, isim: str):
    q_rol = interaction.guild.get_role(QEYDIYYATLI_ROL_ID)
    sz_rol = interaction.guild.get_role(QEYDIYYATSIZ_ROL_ID)
    if q_rol: await member.add_roles(q_rol)
    if sz_rol and sz_rol in member.roles: await member.remove_roles(sz_rol)
    
    embed = discord.Embed(title="Qeydiyyat Uğurlu", description=f"✅ **{member.display_name}** -> **{isim}** olaraq qeydiyyatdan keçdi.", color=0x111111)
    embed.set_image(url=SHIP_KART_RESIM)
    await interaction.response.send_message(embed=embed)

@bot.command(name="qver")
@commands.has_permissions(manage_roles=True)
async def qver(ctx, member: discord.Member):
    sz_rol = ctx.guild.get_role(QEYDIYYATSIZ_ROL_ID)
    if sz_rol: await member.add_roles(sz_rol)
    
    embed = discord.Embed(title="Rol Verildi", description=f"✨ **{member.display_name}** adlı istifadəçiyə Qeydiyyatsız rolu verildi.", color=0x111111)
    embed.set_image(url=SHIP_KART_RESIM)
    await ctx.send(embed=embed)

@bot.tree.command(name="qver", description="İstifadəçiyə qeydiyyatsız rolu verir")
async def slash_qver(interaction: discord.Interaction, member: discord.Member):
    sz_rol = interaction.guild.get_role(QEYDIYYATSIZ_ROL_ID)
    if sz_rol: await member.add_roles(sz_rol)
    
    embed = discord.Embed(title="Rol Verildi", description=f"✨ **{member.display_name}** adlı istifadəçiyə Qeydiyyatsız rolu verildi.", color=0x111111)
    embed.set_image(url=SHIP_KART_RESIM)
    await interaction.response.send_message(embed=embed)

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, sebep="Göstərilməyib"):
    await member.ban(reason=sebep)
    embed = discord.Embed(title="İstifadəçi Edam Olundu (Ban)", description=f"🔨 **{member.display_name}** serverdən qovuldu.\nSəbəb: {sebep}", color=0x992d22)
    embed.set_image(url=SHIP_KART_RESIM)
    await ctx.send(embed=embed)

@bot.tree.command(name="ban", description="İstifadəçini ban edir")
async def slash_ban(interaction: discord.Interaction, member: discord.Member, sebep: str = "Göstərilməyib"):
    await member.ban(reason=sebep)
    embed = discord.Embed(title="İstifadəçi Edam Olundu (Ban)", description=f"🔨 **{member.display_name}** serverdən qovuldu.\nSəbəb: {sebep}", color=0x992d22)
    embed.set_image(url=SHIP_KART_RESIM)
    await interaction.response.send_message(embed=embed)

@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, sebep="Göstərilməyib"):
    embed = discord.Embed(title="Səssizə Alındı (Mute)", description=f"🔇 **{member.display_name}** zindana atıldı.\nSəbəb: {sebep}", color=0xfee75c)
    embed.set_image(url=SHIP_KART_RESIM)
    await ctx.send(embed=embed)

@bot.tree.command(name="mute", description="İstifadəçini mute edir")
async def slash_mute(interaction: discord.Interaction, member: discord.Member, sebep: str = "Göstərilməyib"):
    embed = discord.Embed(title="Səssizə Alındı (Mute)", description=f"🔇 **{member.display_name}** zindana atıldı.\nSəbəb: {sebep}", color=0xfee75c)
    embed.set_image(url=SHIP_KART_RESIM)
    await interaction.response.send_message(embed=embed)

# --- SHIP SİSTEMİ ---
class ShipView(discord.ui.View):
    def __init__(self, author, target):
        super().__init__(timeout=30)
        self.author = author
        self.target = target

    @discord.ui.button(label="Sənə uyğun değil", style=discord.ButtonStyle.danger)
    async def uygun_deyil(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message("Bu düymə sənə aid deyil qardaş.", ephemeral=True)
            return
        await interaction.response.send_message(f"{self.author.display_name} bu ship işinə nöqtə qoydu, uyğun gəlmədi.", ephemeral=True)

    @discord.ui.button(label="Şarkınız", style=discord.ButtonStyle.secondary)
    async def sarkiniz(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message("Bu düymə sənə aid deyil qardaş.", ephemeral=True)
            return
        sarkiler = ["Qara Gözlüm", "Sevgi Delilikdir", "Köhnə Məhəllə", "Gecənin Səsi"]
        await interaction.response.send_message(f"🎶 Sizin ortaq mahnınız: **{random.choice(sarkiler)}**", ephemeral=True)

    @discord.ui.button(label="Yenidən ship", style=discord.ButtonStyle.blurple)
    async def yeniden(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user != self.author:
            await interaction.response.send_message("Bu düymə sənə aid deyil qardaş.", ephemeral=True)
            return
        faiz = random.randint(1, 100)
        
        if 0 <= faiz <= 30:
            emoji = "<a:uzgun:1567412245892169800>"
        elif 31 <= faiz <= 60:
            emoji = "<a:ship:1567413599159459944>"
        else:
            emoji = "<a:senicokseviyorum:1567413691500990548>"

        metin = f"## {emoji} {self.author.display_name} <a:ship:1567413599159459944> {self.target.display_name}\n> Uyğunluq: **%{faiz}**\n\n"
        if faiz < 50:
            metin += f"{emoji} Hələ ki bir-birlərinə salam belə verməyiblər, deyəsən bu sevgi \"ghost\" rejimində başlayır.\n-# 50%-dən aşağı uyğunluqda evlənmək mümkün deyil."
        else:
            metin += f"{emoji} Alovlu sevgi başladı! Deyəsən bu işin sonu toydu."
        
        embed = discord.Embed(color=0x111111, description=metin)
        embed.set_image(url=SHIP_KART_RESIM)
        await interaction.response.edit_message(content=None, embed=embed, view=self)

@bot.command(name="ship")
async def ship(ctx, member: discord.Member = None):
    if not member:
        await ctx.send("Kiminlə ship eləmək istəyirsən? Məsələn: `.ship @İstifadəçi` yaz.")
        return
    if member == ctx.author:
        await ctx.send("Öz-özünlə ship eləyə bilməzsən qardaş.")
        return

    faiz = random.randint(1, 100)
    
    if 0 <= faiz <= 30:
        emoji = "<a:uzgun:1567412245892169800>"
    elif 31 <= faiz <= 60:
        emoji = "<a:ship:1567413599159459944>"
    else:
        emoji = "<a:senicokseviyorum:1567413691500990548>"

    metin = f"## {emoji} {ctx.author.display_name} <a:ship:1567413599159459944> {member.display_name}\n> Uyğunluq: **%{faiz}**\n\n"
    if faiz < 50:
        metin += f"{emoji} Hələ ki bir-birlərinə salam belə verməyiblər, deyəsən bu sevgi \"ghost\" rejimində başlayır.\n-# 50%-dən aşağı uyğunluqda evlənmək mümkün deyil."
    else:
        metin += f"{emoji} Alovlu sevgi başladı! Deyəsən bu işin sonu toydu."

    embed = discord.Embed(color=0x111111, description=metin)
    embed.set_image(url=SHIP_KART_RESIM)
    
    view = ShipView(ctx.author, member)
    await ctx.send(embed=embed, view=view)

@bot.command(name="mafia")
async def mafia(ctx):
    roller = ["Mafiya başçısı", "Polis", "Həkim", "Sadə vətəndaş", "Killer", "Oğraş"]
    secilen = random.choice(roller)
    await ctx.send(f"Mafiya oyununda sənə düşən rol: {secilen}")

@bot.tree.command(name="mafia", description="Mafya oyunundaki rolünüzü belirler")
async def slash_mafia(interaction: discord.Interaction):
    roller = ["Mafiya başçısı", "Polis", "Həkim", "Sadə vətəndaş", "Killer", "Oğraş"]
    secilen = random.choice(roller)
    await interaction.response.send_message(f"Mafiya oyununda sənə düşən rol: **{secilen}**")

@bot.command(name="temizle")
@commands.has_permissions(manage_messages=True)
async def temizle(ctx, limit: int = 10):
    if limit > 100: limit = 100
    await ctx.message.delete()
    silinen = await ctx.channel.purge(limit=limit)
    msg = await ctx.send(f"🧹 Uğurla {len(silinen)} mesaj təmizləndi.")
    await msg.delete(delay=4)

@bot.tree.command(name="temizle", description="Belirtilen sayıda mesajı siler")
async def slash_temizle(interaction: discord.Interaction, limit: int = 10):
    if not interaction.user.guild_permissions.manage_messages:
        await interaction.response.send_message("Bu komut için mesajları yönet yetkisi lazım!", ephemeral=True)
        return
    if limit > 100: limit = 100
    await interaction.response.defer(ephemeral=True)
    silinen = await interaction.channel.purge(limit=limit)
    await interaction.followup.send(f"🧹 Uğurla {len(silinen)} mesaj təmizləndi.")

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)

        
