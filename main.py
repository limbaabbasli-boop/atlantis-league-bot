import os
import discord
from discord.ext import commands
from discord.ui import Button, View, Select
import random

# Bot Kurulumu
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

# Sahte Veritabanı (Oyuncu Bakiyeleri & Mülkleri)
user_balances = {}

def get_user_data(user_id):
    if user_id not in user_balances:
        user_balances[user_id] = {
            "cuzdan": 0,
            "banka": 0,
            "deger": 0,
            "takim": "Serbest Oyuncu",
            "arabalar": [],
            "evler": []
        }
    return user_balances[user_id]

# ---------------------------------------------------------
# UI BİLEŞENLERİ (BUTONLAR VE SEÇİM MENÜLERİ)
# ---------------------------------------------------------

class HelpView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="RP Sistemleri", style=discord.ButtonStyle.primary, emoji="⚽")
    async def rp_help(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="⚽ Atlantis League Sistemleri Yardım",
            description="Sunucudaki temel RP ve Ekonomi komutları:",
            color=discord.Color.blue()
        )
        embed.add_field(name=".bal", value="Cüzdan, banka ve değer durumunuzu gösterir.", inline=False)
        embed.add_field(name=".pay @Kullanıcı [Miktar]", value="Başka bir oyuncuya para gönderir.", inline=False)
        embed.add_field(name=".kap @Oyuncu [Takım]", value="Oyuncuyu kulübünüze transfer eder (Kapar).", inline=False)
        embed.add_field(name=".galeri", value="Araba satın alım galerisini açar.", inline=False)
        embed.add_field(name=".emlak", value="Ev/Mülk satın alım ofisini açar.", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Yönetici Komutları", style=discord.ButtonStyle.danger, emoji="👑")
    async def admin_help(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="👑 Yönetici Sistemleri",
            description="Yetkililerin kullanabileceği özel komutlar:",
            color=discord.Color.red()
        )
        embed.add_field(name=".bal-ekle @Kullanıcı [Miktar]", value="Teknik Direktör/Başkan için bakiye ekler.", inline=False)
        embed.add_field(name=".deger-ver @Kullanıcı [Değer] [Sebep]", value="Oyuncunun değerini günceller.", inline=False)
        embed.add_field(name=".kapa (veya .kanal-kilitle)", value="Bulunduğunuz kanalı üyelere kapatır.", inline=False)
        embed.add_field(name=".ac (veya .kanal-ac)", value="Kilitlenen kanalı tekrar açar.", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class CarSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Porsche 911 Turbo S", description="21M Bal • +11M Değer", emoji="🏎️"),
            discord.SelectOption(label="Range Rover SV", description="27M Bal • +18M Değer", emoji="🚘"),
            discord.SelectOption(label="Ferrari 12Cilindri", description="35M Bal • +25M Değer", emoji="🏎️"),
            discord.SelectOption(label="Lamborghini Revuelto", description="40M Bal • +30M Değer", emoji="🏎️"),
            discord.SelectOption(label="Bugatti Tourbillon", description="50M Bal • +40M Değer", emoji="🏎️"),
        ]
        super().__init__(placeholder="Satın almak istediğin aracı seç...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        data = get_user_data(interaction.user.id)
        selected_car = self.values[0]
        data["arabalar"].append(selected_car)
        await interaction.response.send_message(
            f"🎉 Tebrikler! **{selected_car}** başarıyla satın alındı ve garajınıza eklendi!", 
            ephemeral=True
        )


class CarGalleryView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(CarSelect())


class HouseSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Şehir Manzaralı 2+1 Daire", description="9M Bal • +4M Değer", emoji="🏢"),
            discord.SelectOption(label="Akıllı Ev Sistemli 3+1 Daire", description="14M Bal • +7M Değer", emoji="🏠"),
            discord.SelectOption(label="Deniz Manzaralı Lüks Rezidans", description="20M Bal • +12M Değer", emoji="🏙️"),
            discord.SelectOption(label="Özel Bahçeli Müstakil Villa", description="38M Bal • +19M Değer", emoji="🏡"),
            discord.SelectOption(label="Atlantis Kraliyet Malikanesi", description="45M Bal • +29M Değer", emoji="🏰"),
        ]
        super().__init__(placeholder="Satın almak istediğin evi seç...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        data = get_user_data(interaction.user.id)
        selected_house = self.values[0]
        data["evler"].append(selected_house)
        await interaction.response.send_message(
            f"🏡 Tebrikler! **{selected_house}** tapusu üzerinize geçirildi!", 
            ephemeral=True
        )


class HouseGalleryView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HouseSelect())


# ---------------------------------------------------------
# BOT ETKİNLİKLERİ VE KOMUTLAR
# ---------------------------------------------------------

@bot.event
async def on_ready():
    print(f"[{bot.user}] Atlantis League Botu Aktif!")
    await bot.change_presence(activity=discord.Game(name="Atlantis League | .help"))


@bot.command(name="help")
async def help_command(ctx):
    """Gelişmiş Atlantis League Yardım Menüsü"""
    embed = discord.Embed(
        title="✨ Atlantis League - Yardım Paneli",
        description="Aşağıdaki butonları kullanarak RP komutlarını ve yetkili menülerini inceleyebilirsiniz.",
        color=discord.Color.purple()
    )
    if ctx.guild and ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
    embed.add_field(name="❓ Nasıl Başlanır?", value="📜 `.baslangic` yazarak rehber mesajını alabilirsiniz.", inline=False)
    
    view = HelpView()
    await ctx.send(embed=embed, view=view)


# --- EKONOMİ VE TRANSFER KOMUTLARI ---

@bot.command(aliases=["bakiye", "cuzdan"])
async def bal(ctx, member: discord.Member = None):
    """Kullanıcının Bakiyesini ve Mülklerini Gösterir"""
    target = member or ctx.author
    data = get_user_data(target.id)

    embed = discord.Embed(
        title=f"💳 {target.display_name} - Oyuncu Profili",
        color=discord.Color.green()
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="🛡️ Takımı", value=f"**{data['takim']}**", inline=False)
    embed.add_field(name="👛 Cüzdan", value=f"{data['cuzdan']:,} Bal", inline=True)
    embed.add_field(name="🏦 Banka", value=f"{data['banka']:,} Bal", inline=True)
    embed.add_field(name="⭐ Oyuncu Değeri", value=f"{data['deger']:,} Bal", inline=True)
    embed.add_field(name="🏎️ Arabalar", value=f"{len(data['arabalar'])} Adet", inline=True)
    embed.add_field(name="🏡 Evler", value=f"{len(data['evler'])} Adet", inline=True)

    await ctx.send(embed=embed)


@bot.command()
async def pay(ctx, member: discord.Member, miktar: int):
    """Başka Bir Oyuncuya Para Gönderir"""
    if member.id == ctx.author.id:
        return await ctx.send("❌ Kendine para gönderemezsin!")
    if miktar <= 0:
        return await ctx.send("❌ Geçerli bir miktar girmelisin!")

    sender_data = get_user_data(ctx.author.id)

    if sender_data["cuzdan"] < miktar:
        return await ctx.send("❌ Cüzdanında yeterli miktarda Bal yok!")

    receiver_data = get_user_data(member.id)
    sender_data["cuzdan"] -= miktar
    receiver_data["cuzdan"] += miktar

    embed = discord.Embed(
        title="💸 Para Transferi",
        description=f"{ctx.author.mention}, {member.mention} kullanıcısına **{miktar:,} Bal** gönderdi!",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


@bot.command()
async def kap(ctx, oyucu: discord.Member, *, takim_adi: str):
    """Oyuncuyu Takıma Katma / Kapma Komutu"""
    data = get_user_data(oyucu.id)
    eski_takim = data["takim"]
    data["takim"] = takim_adi

    embed = discord.Embed(
        title="🔥 BOMBA TRANSFER! OYUNCU KAPILDI!",
        description=f"{oyucu.mention} isimli oyuncu başarıyla kapıldı ve kadroya katıldı!",
        color=discord.Color.gold()
    )
    embed.set_thumbnail(url=oyucu.display_avatar.url)
    embed.add_field(name="👤 Transfer Edilen Oyuncu", value=oyucu.mention, inline=True)
    embed.add_field(name="🛡️ Yeni Takımı", value=f"**{takim_adi}**", inline=True)
    embed.add_field(name="🔄 Eski Takımı", value=eski_takim, inline=True)
    embed.add_field(name="✍️ İşlemi Yapan Menajer/Yetkili", value=ctx.author.mention, inline=False)
    embed.set_footer(text="Atlantis League Transfer Pazarı")

    await ctx.send(embed=embed)


# --- YETKİLİ BAKIYE EKLEME KOMUTU (.bal-ekle) ---

@bot.command(name="bal-ekle")
@commands.has_permissions(administrator=True)
async def bal_ekle(ctx, member: discord.Member, miktar: int = 100000000):
    """Teknik Direktör ve Başkanlar İçin Bakiye Ekler (Varsayılan 100M)"""
    data = get_user_data(member.id)
    data["cuzdan"] += miktar

    embed = discord.Embed(
        title="🏦 Kulüp Kasasından Bakiye Eklendi",
        description=f"👑 Yetkili {ctx.author.mention}, **{member.mention}** adlı kullanıcının cüzdanına **{miktar:,} Bal** ekledi!",
        color=discord.Color.gold()
    )
    embed.add_field(name="💰 Güncel Cüzdan", value=f"{data['cuzdan']:,} Bal", inline=False)
    embed.set_footer(text="Atlantis League Finans Departmanı")
    
    await ctx.send(embed=embed)


# --- YETKİLİ KANAL KİLİTLEME KOMUTLARI ---

@bot.command(aliases=["kapa"])
@commands.has_permissions(manage_channels=True)
async def kanal_kilitle(ctx):
    """Bulunulan Kanalı Yazışmaya Kapatır"""
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Bu kanal yetkili tarafından üyelerin yazışmasına kapatıldı!")

@bot.command(aliases=["ac"])
@commands.has_permissions(manage_channels=True)
async def kanal_ac(ctx):
    """Kilitlenen Kanalı Tekrar Açar"""
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Bu kanal tekrar üyelerin yazışmasına açıldı!")


# --- RP PANELERİ VE MAĞAZALAR ---

@bot.command()
async def baslangic(ctx):
    """Atlantis League Başlangıç Rehberi Panelini Açar"""
    embed = discord.Embed(
        title="💫 Atlantis League Başlangıç Rehberi",
        description="**Atlantis League'e hoş geldin.**\nKaydını tamamla, oyuncunu geliştir ve ilk takımını bul.",
        color=discord.Color.gold()
    )
    embed.add_field(name="📝 İlk Gün Planım", value="1. Kayıt Ol\n2. Antrenman Yap\n3. Takım Bul", inline=False)
    
    view = View()
    view.add_item(Button(label="Kayıt Ol", style=discord.ButtonStyle.primary, emoji="👤"))
    view.add_item(Button(label="Değer Kazan", style=discord.ButtonStyle.success, emoji="💶"))
    view.add_item(Button(label="Takım Bul", style=discord.ButtonStyle.secondary, emoji="🛡️"))
    
    await ctx.send(embed=embed, view=view)


@bot.command()
async def galeri(ctx):
    """Araba Satın Alım Menüsü"""
    embed = discord.Embed(
        title="🚘 Atlantis League Araç Galerisi",
        description="2026 model seçkin araçları incelemek ve satın almak için aşağıdaki menüyü kullanın.\n\n"
                    "• Satın alma işlemi onay ekranından sonra tamamlanır.\n"
                    "• Her araç yalnızca bir kez alınabilir.",
        color=discord.Color.dark_gray()
    )
    await ctx.send(embed=embed, view=CarGalleryView())


@bot.command()
async def emlak(ctx):
    """Ev Satın Alım Menüsü"""
    embed = discord.Embed(
        title="🏡 Atlantis League Emlak Ofisi",
        description="Modern dairelerden kraliyet malikanelerine kadar mülkleri incelemek için aşağıdaki menüyü kullanın.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, view=HouseGalleryView())


@bot.command(name="deger-ver")
@commands.has_permissions(administrator=True)
async def deger_ver(ctx, uye: discord.Member, yeni_deger: str, *, sebep: str = "Açıklama belirtilmedi"):
    """Yöneticilerin Değer Logu Geçmesini Sağlar"""
    embed = discord.Embed(
        title="🟡 Değer Verildi",
        color=discord.Color.gold()
    )
    embed.add_field(name="👤 Üye", value=uye.mention, inline=False)
    embed.add_field(name="📈 Yeni Değer", value=yeni_deger, inline=False)
    embed.add_field(name="📌 Sebep", value=sebep, inline=False)
    embed.add_field(name="👑 Yetkili", value=ctx.author.mention, inline=False)
    embed.set_footer(text=f"Zaman › {ctx.message.created_at.strftime('%d %B %Y %H:%M')}")
    
    await ctx.send(embed=embed)


bot.run(os.environ.get("DISCORD_TOKEN"))
