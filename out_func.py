

# Şaplak atma özelliği için listeden rastgele metin bulma algoritması
def rn():
    global lastrn
    xrn = random.randint(0, len(slaplist) - 1)
    if xrn != lastrn:
        lastrn = xrn
        return lastrn
    return rn()
