# -*- coding: utf-8 -*-

from telegram.ext import *
from telegram import *
import logging,os,random,string,json,base64,urllib,sys,re

"""
	İşletim sistemine özel özellikler için
	işletim sistemi bilgisini kontrol et
"""
linux = os.name == 'posix'

# Botun bazı elemanlarını Python 2 ve Python 3 ile uyumlu hale getir
req = 0
quo = 0
py3 = sys.version_info[0] >= 3

if py3:
	import urllib.request,urllib.parse
	req = urllib.request
	quo = urllib.parse
else:
	import urllib2
	req = urllib2
	quo = req

# Yandex Translate API Key (örnek: trnsl.1.1.20190224T015610Z.47h8eba1d2c35f6g.59a2b3030eaae8611751e6a68c231cc83d597c07)
transkey = ""

# Yandex SpeechKit API Key (örnek: 4bcd3fgh-1jkl-mn0p-qr5t-uvwxyz123456)
ttskey = u""

# Telegram Bot API Token (örnek: 123456789:aBCdeFGHiJKLmn_pQrsTUv128qKUm9yGlNBg)
TOKEN = ""

def start(bot, update):
    update.message.reply_text('HOSGELDIN DOSTUM!')

# Botta oluşan sorunları ekrana çıktılar
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

# Yandex Translate API için dil listesi
langlist = ["az","sq","am","en","ar","hy","af","eu","ba","be","bn",
"my","bg","bs","cy","hu","vi","ht","gl","nl","mrj","el","ka","gu","da",
"he","yi","id","ga","it","is","es","kk","kn","ca","ky","zh","ko","xh",
"km","lo","la","lv","lt","lb","mg","ms","ml","mt","mk","mi","mr","mhr",
"mn","de","ne","no","pa","pap","fa","pl","pt","ro","ru","ceb","sr","si",
"sk","sl","sw","su","tg","th","tl","ta","tt","te","tr","udm","uz","uk",
"ur","fi","fr","hi","hr","cs","sv","gd","et","eo","jv","ja"]

# Şaplak atma özelliği için gösterilecek mesajlar listesi
slaplist = [u"{}, {} üzerine tüplü TV fırlattı!", u"{}, {}'ye osmanlı tokadı attı!",
u"{}, {} ADAMIN SiKTI!", u"{}, {} üzerine iPhone3GS fırlattı!",
u"{}, {}'nin RTX 2080Ti'sini kırdı!",u"{}, {}'nin kalbini kırdı!", 
u"{}, {} üzerine kahve döktü!", u"{}, {}'nin yüzüne pasta fırlattı!",
u"{}, {} için aldığı hediyeyi Sikti!"]

lastrn = -1

# Sohbet odasında mesajlara verilecek tepkiler

def conv(bot, update):
	res=""
	txt=gettxt(update)
	global tx
	send=True
	try:
		tx=txt.replace("\n"," ").split(" ")
	except:
		return
	else:
		cmd=tx[0]
		if len(cmd) < 1:
			send=False
			return
		if args():
			txt=txt[len(cmd)+1:]
			# komut @ işareti içeriyorsa hangi bota komut verildiğini kontrol eder
			if "@" in cmd:
				t = cmd.split("@")
				if bot.username == t[1]:
					cmd=t[0]
				else:
					send=False
					return
			cmd=cmd[1:].lower()
			if "hello" == cmd:
				res = "Merhaba dünya!"
			elif "link" == cmd:
				res = u"Grup linki: "
				if bool(update.message.chat.username):
					res = res + "https://t.me/" + update.message.chat.username
				elif adminctrl(bot,update,bot.id):
					if bool(update.message.chat.invite_link):
						res = res + update.message.chat.invite_link
					else:
						res = res + bot.exportChatInviteLink(update.message.chat.id)
			elif "tekrarla" == cmd:
				if len(txt) > 0:
					res = txt
				else:
					res = "Bu özelliği kullanmak için bir metin yazmalısınız\nKullanım şekli:\n/tekrarla <metin>"
			elif "id" == cmd:
				type = update.message.chat.type
				res = u"Konuşma tipi: "+type+"\n"+u"Konuşma numarası: "+str(update.message.chat.id)
				if "group" in type:
					res = res + "\n"+u"Kişi numarası: "+str(update.message.from_user.id)
					res = res + "\n"+u"Yöneticiler: "
					for i in bot.get_chat_administrators(update.message.chat.id):
						if bool(i.user.username):
							user = i.user.username
						else:
							user = i.user.full_name
						res = res + "\n" + user + "\n" + i.status + "\n\n"
			elif cmd in [u"duck",u"google",u"stackoverflow",u"wiki"]:
				res = arama(cmd,txt)
			elif cmd in [u"cevir",u"çevir"]:
				if len(txt) > 0:
					if tx[1][0] == "-" and tx[1][1:] in langlist:
						lang = tx[1][1:]
						txt = txt.replace(tx[1],"")
					else:
						lang = "tr"
					res = cevir(lang,txt)
				else:
					res = update.message.reply_to_message
					if res:
						if tx[1][0] == "-" and tx[1][1:] in langlist:
							lang = tx[1][1:]
						else:
							lang = "tr"
						txt = res.text
						if not txt:
							txt = res.caption
						res = cevir(lang,txt)
					else:
						res = u"Bu özelliği kullanmak için bir metin yazmalısınız\nKullanım şekli:\n/cevir <metin> veya /cevir -dil <metin>"
			elif "beniat" == cmd:
				if "group" in update.message.chat.type:
					id = update.message.from_user.id
					if not adminctrl(bot,update,id):
						user = update.message.from_user.username
						if not bool(user):
							user = update.message.from_user.full_name
						else:
							user = u"@"+user
						
						if adminctrl(bot,update,bot.id):
							try:
								bot.kickChatMember(chat_id=update.message.chat.id,user_id=id)
								bot.unbanChatMember(chat_id=update.message.chat.id,user_id=id)
							except:
								if adminctrl(bot,update,id):
									res = user + u" yönetici olduğundan dolayı seni atamadım, çok çıkmak istiyorsan kendin çıkabilirsin"
								else:
									res = user + u" kendisini gruptan attırmak istedi, ancak bir sorunla karşılaştığımdan dolayı bunu yapamadım"
							else:
								res = user + u" kendisini gruptan attırdı"
						else:
							res = u"Yönetici izinlerine sahip olmadığımdan seni atamıyorum"
					else:
						res = u"Sen bir yöneticisin, seni engelleyemem"
				else:
					res = u"Bu komut sadece grupta çalışır"
			elif "hesapla" == cmd:
				if not linux:
					res = u"Bot sahibi bu botu GNU/Linux kurulu olmayan bir makine üzerinde açmış gibi görünüyor, dolayısıyla bu özelliği kullanamazsınız"
				else:
					if len(tx) < 2:
						res = u"Bu özelliği kullanmak için bir metin yazmalısınız\nKullanım şekli:\n/hesapla <metin>"
					else:
						if re.search('\d+', txt):
							res = os.popen("echo " + replacer(txt.replace("(","\(").replace(")","\)").replace(" ",""). replace("&","").replace(";","").replace(":","").replace("`","").replace("$","").replace("!","").lower()) + " | bc 2> /dev/null").read()
							res = res.replace("\\\n","")
						else:
							res = ""
						if not bool(res) or not re.search('\d+', txt):
							res = u"Eksik veya hatalı giriş yaptınız, doğru bir şekilde yazıp tekrar deneyin"
			elif "sil" == cmd:
				try:
					if "group" in update.message.chat.type:
						if adminctrl(bot,update,update.message.from_user.id):
							a = update.message.reply_to_message
							if a:
								a.delete()
								id = update.message.chat.id
								update.message.delete()
								res = "Mesaj silindi"
								bot.sendMessage(chat_id=id,text=res)
								return
							else:
								res = u"İşlem yapmak için bir kişinin mesajına cevap vermelisiniz"
						else:
							res = u"Yönetici olmadığın için bu yazdığını umursamıyorum"
					else:
						res = u"Bu komut sadece grupta çalışır"
				except:
					res = u"Yönetici izinlerine sahip olmadığımdan veya başka bir sorun oluştuğundan dolayı bu işlemi yapamıyorum"
			elif cmd in [u"tekmele",u"engelle",u"ekaldir"]:
				try:
					if "group" in update.message.chat.type:
						if adminctrl(bot,update,update.message.from_user.id):
							if len(tx) == 1:
								a = update.message.reply_to_message
								if bool(a):
									if a.from_user.id != bot.id:
										if cmd != "ekaldir":
											bot.kickChatMember(chat_id=update.message.chat.id,user_id=a.from_user.id)
										if cmd == "engelle":
											res = u"Kişi gruptan atıldı ve engellendi"
										else:
											bot.unbanChatMember(chat_id=update.message.chat.id,user_id=a.from_user.id)
											if cmd == "tekmele":
												res = u"Kişi gruptan atıldı"
											else:
												res = u"Kişinin engeli kaldırıldı"
									else:
										if cmd != "ekaldir":
											res = u"Kendimi nasıl gruptan atabilirim?"
										else:
											res = u"Ben zaten gruptayım, engellenmedim"
								else:
									res = u"Şu anlık işlem yapmak için bir kişinin mesajına cevap vermelisiniz"
							else:
								res = u"Şu anlık işlem yapmak için bir kişinin mesajına cevap vermelisiniz"
						else:
							res = u"Yönetici olmadığın için bu yazdığını umursamıyorum"
					else:
						res = u"Bu komut sadece grupta çalışır"
				except:
					res = u"Yönetici izinlerine sahip olmadığımdan veya başka bir sorun oluştuğundan dolayı bu işlemi yapamıyorum"
			elif "hava" == cmd:
				res = hava(txt)
			elif "ses" == cmd:
				if len(tx) > 1:
					tts(update,txt)
					send = False
				else:
					res = u"Bu özelliği kullanmak için metin yazmalısınız\nKullanım şekli:\n/ses <metin>"
			elif "slap" == cmd:
				user = update.message.from_user.username
				us2 = ""
				if not bool(user):
					user = update.message.from_user.full_name
				else:
					user = u"@" + user
				if len(tx) == 1:
					a = update.message.reply_to_message
					if not bool(a):
						us2 = user
						user = u"@"+bot.username
					else:
						b = a.from_user
						if not bool(b.username):
							us2 = b.full_name
						else:
							us2 = "@"+b.username
						send = False
				else:
					us2 = tx[1]
				res = slaplist[rn()].format(user,us2)
				if not send:
					update.message.reply_to_message.reply_text(res)
			else:
				send = False
		else:
			# Botla normal sohbet kurma algoritması
			if bot.first_name.lower() == tx[0].lower():
				send = True
				if len(tx) == 1:
					res = u"Kes!"
				else:
					res = txt[len(tx[0])+1:].lower()
					tx = res.split(" ")
					if u"defol" in tx or bot.first_name.lower() in tx:
						res = u"Kes!"
					elif u"nasılsın" in tx or u"naber" in tx:
						res = u"Bilemiyorum "+update.message.from_user.first_name.split(" ")[0]+u" ..."
					elif u"ne yapıyorsun" in res or u"napıyon" in tx:
						res = u"Yuvarlanıp gidiyoruz işte, sen ne yapıyorsun?"
					elif u"ağla" in tx:
						res = u"Kudur 😜"
					elif u"öl" in tx or u"geber" in tx:
						res = u"Zaten yaşamıyorum ki 😏" 
					elif u"ölmek istiyorum" in res:
						res = u"ŞeReFSiZLeRe iNaT YaŞa"
					elif u"seri" in tx:
						res = u"Köz getir kardşm"
					elif u"hey" in tx or u"hi" in tx or u"merhaba" in tx:
						res = u"Merhaba"
					elif u"atatürk" in tx:
						res = u"🇹🇷🇹🇷🇹🇷🇹🇷 ATAM 🇹🇷🇹🇷🇹🇷🇹🇷"
					else:
						res = u"¯\_(ツ)_/¯"
					
		if send:
				if cmd in [u"hava",u"duck",u"google",u"stackoverflow",u"wiki"]:
					update.message.reply_markdown(res)
				else:
					update.message.reply_text(res)


def replacer(text):
	rep = {u"ç": u"c", u"ğ": u"g", u"ı": u"i", u"ö": u"o",u"ş": u"s", u"ü": u"u"}
	if py3:
		rep = rep.items()
	else:
		rep = rep.iteritems()
	rep = dict((re.escape(k), v) for k, v in rep)
	pattern = re.compile("|".join(rep.keys()))
	text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
	return text

# Komut girilip girilmediğini kontrol eder
def args():
	return tx[0][0] in ["/","!","\\","|"]

tx = []

# Inline modda mesajlara verilecek tepkiler
def inline(bot, update):
	query = update.inline_query.query
	if len(query) > 2:
		global tx
		tx = query.split(" ")
		sres = []
		if args():
			temp=query[len(tx[0])+1:]
			cmd=tx[0][1:]
			desc = ""
			if "tekrarla" == cmd:
				desc="Metni tekrarla: "+temp
				if len(tx) < 2:
					desc="Bu özelliği kullanmak için bir metin yazmalısınız\nKullanım şekli:\n/tekrarla <metin>"
					temp=desc
				sres.append(InlineQueryResultArticle(
						id = ''.join(random.choice(string.ascii_lowercase + string.digits))[:8],
						title = bot.first_name,
						description=desc,
						input_message_content = InputTextMessageContent(temp)
					)
				)
			elif cmd in [u"duck",u"google",u"stackoverflow",u"wiki"]:
				desc = u"🔍 " + arasite(cmd) + ": " + temp
				temp = arama(cmd,temp)
				sres.append(InlineQueryResultArticle(
						id = ''.join(random.choice(string.ascii_lowercase + string.digits))[:8],
						title = bot.first_name,
						description=desc,
						input_message_content = InputTextMessageContent(temp,parse_mode=ParseMode.MARKDOWN)
					)
				)
			elif "hava" == cmd:
				if len(tx) < 2:
					desc="Bu özelliği kullanmak için bir metin yazmalısınız\nKullanım şekli:\n/hava <şehir>"
					temp=desc
				else:
					desc = u"Hava durumu: "+temp
					temp = hava(temp)
				sres.append(InlineQueryResultArticle(
						id = ''.join(random.choice(string.ascii_lowercase + string.digits))[:8],
						title = bot.first_name,
						description=desc,
						input_message_content = InputTextMessageContent(temp,parse_mode=ParseMode.MARKDOWN)
					)
				)
			elif cmd in [u"cevir",u"çevir"]:
				desc=u"Çevir: "+temp
				if len(tx) < 2:
					desc="Bu özelliği kullanmak için bir metin yazmalısınız\nKullanım şekli:\n/cevir <metin> veya /cevir -dil metin"
					temp=desc
				else:
					if tx[1][0] == "-" and tx[1][1:] in langlist:
						lang = tx[1][1:]
						temp = ''.join(temp).replace(tx[1],"")
						desc = ''.join(desc).replace(tx[1],"") + " -> " + lang
					else:
						desc = desc + " -> " + lang
						lang = "tr"
					temp = cevir(lang,temp)
					desc = desc + "\n" + u"Önizleme: " + temp
				sres.append(InlineQueryResultArticle(
						id = ''.join(random.choice(string.ascii_lowercase + string.digits))[:8],
						title = bot.first_name,
						description=desc,
						input_message_content = InputTextMessageContent(temp)
					)
				)
			else:
				return
			update.inline_query.answer(sres)
		else:
			return
	else:
		return

# Gruba yeni giren kişileri karşıla (beta)
def welcome(bot, update):
	update.message.reply_markdown(update.message.chat.title+u" grubuna hoş geldin")
	
# Gruptan çıkan kişileri uğurla (beta)
def goodbye(bot, update):
	update.message.reply_text("Hoşçakal")
	
"""
def build_menu(buttons,n_cols=1,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu
"""

# Sobet numarası belirtilen kişinin yönetici olup olmadığını bulur
def adminctrl(bot,update,id):
	for i in bot.get_chat_administrators(update.message.chat.id):
		if id == i.user.id:
			return True
	return False

# Şaplak atma özelliği için listeden rastgele metin bulma algoritması
def rn():
	global lastrn
	xrn = random.randint(0,len(slaplist)-1)
	if xrn != lastrn:
		lastrn = xrn
		return lastrn
	return rn()

# Hava durumunu bir web sağlayıcısından çeker
def hava(sehir):
	if not bool(sehir):
		return u"Lütfen bir şehir adı girin"
	sehir = arafiltre(str(sehir))
	sehir = sehir.replace('"','').replace(":","").split("+")[0].split(",")[0]
	if len(sehir) < 1:
		return u"Bu özellik şu anda çalışmıyor veya hatalı giriş yaptınız"
	sehir = sehir.replace(sehir[0],sehir[0].upper(),1)
	txt = quo.quote(sehir.encode("utf8"))
	txt = conn("http://wttr.in/"+txt+"?qmT0").read()
	if not bool(txt) or b"===" in txt:
		return u"Bu özellik şu anda çalışmıyor veya hatalı giriş yaptınız"
	txtx = txt.replace(txt.split(b"\n")[0],b"",1)
	txtx = b"```%s```" % txtx
	txtx = txt.split(b"\n")[0] + b"\n" + txtx
	return txtx.decode('utf-8')

# Girilen metne göre çeviri yapar
def cevir(dil,cumle):
	temp = quo.quote(cumle.encode("utf8"))
	temp = ''.join(temp).replace("?","%3F")
	temp = "https://translate.yandex.net/api/v1.5/tr.json/translate?key="+transkey+"&lang="+dil+"&text="+temp
	temp = conn(temp).read()
	temp = json.loads(temp.decode("utf8")).get('text')[0]
	return temp

# Arama motorları için arama linki oluşturur
def arama(cmd,cumle):
	res = cumle
	txt = cumle
	if not bool(res):
		res = u"Lütfen aramak için bir metin yazın"
	else:	
		res = quo.quote(res.encode("utf8"))
		if cmd == "duck":
			res = "https://duckduckgo.com/?q="+res
		elif cmd == "stackoverflow":
			res = "https://stackoverflow.com/search?q="+res
		elif cmd == "wiki":
			res = base64.b64encode((u"https://tr.wikipedia.org/w/index.php?search="+res).encode("utf8"))
			res = "http://www.wikizeroo.net/index.php?q="+res.decode("utf8")
		else:
			res ="https://www.google.com.tr/search?q="+res
		txt = "[%s]" % arafiltre(txt)
		res = "(%s)" % arafiltre(res)
		res = u"🔍 " + ("*%s*" % arasite(cmd) + ": ") + txt + res
	return res

def arasite(cmd):
	if cmd == "duck":
		return "DuckDuckGo"
	elif cmd == "stackoverflow":
		return "Stack Overflow"
	elif cmd == "wiki":
		return "Wikizero"
	else:
		return "Google"

"""
	Bazı istenmeyen karakterleri arama sonucundan ve
	diğer yerlerden filtreler
"""
def arafiltre(txt):
	return txt.replace("[","").replace("]","").replace("(","").replace(")","").replace("{","").replace("}","");

# Metinden ses üretir
def tts(update,txt):
	f = quo.quote(txt.replace("&","ve").encode("utf8"))
	s = u"oksana" # Konuşan ses
	f = conn(u"https://tts.voicetech.yandex.net/generate?key="+ttskey+u"&text="+txt+u"&format=opus&lang=tr-TR&speaker="+spk+u"&speed=0.8")
	update.message.reply_voice(voice=f)
	f.close()

"""
	Belirtilen linklere bağlanmak için gerekli başlıkları
	ayarlar ve sonucu gerekli yere geri dönüş olarak verir
"""
def conn(url):
	return req.urlopen(req.Request(url, headers={'User-Agent':'curl/7.63', 'Accept-Language':'tr'}))

# Mesaj metinlerini yakalamak için algoritma
def gettxt(update):
	txt=update.message.text
	if not bool(txt):
		txt=update.message.caption
	return txt	

"""
	Botun can damarı, ana fonksiyon
	Yazılan anahtarla bota bağlanmaya çalışır
	Ayrıca sohbet filteleri de burada belirtilir
"""
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.status_update.left_chat_member, goodbye))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(InlineQueryHandler(inline))
    dp.add_handler(MessageHandler(Filters.all, conv))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
