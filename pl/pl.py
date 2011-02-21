# -*- coding: utf-8 -*-
# *********
# pl/pl.py
# *********
#
# This file defines language dependent functions and variables. Probably
# this is the most important file in whole package.
#
# ============
# Requirements
# ============
#
# This package *may* import some other packages, it is up to you (and your
# needs).
#
# BUT: this packahe **must** define the following functions:
# * ``direction()`` which "translates" direction given by letters into
#    its word representation
# * ``removeDiacritics()`` which removes diacritics
# * ``readISODT()`` "translates" date and time into its word representation
# * ``cardinal()``  which changes numbers into words (1 -> one)
#
# As you probably can see all of these functions are language-dependant.
#
# ======================
# Implementation example
# ======================
#
# Here is implementation example for Polish language. Polish is interresting
# because it uses diacritics and 7 (seven) gramatical cases[#]_ (among many
# other features ;)
#
# .. [*] http://pl.wikipedia.org/wiki/Przypadek#Przypadki_w_j.C4.99zyku_polskim
#
# There *may* be some issues with diacritics because there are many
# implementations [#]. For example, Windows uses its own coding system while
# Linux uses UTF-8 (I think). And, when moving files (which are named with
# diacritics) from one platform to another results may (will) be
# unexpectable.
#
# .. [#] http://pl.wikipedia.org/wiki/Kodowanie_polskich_znak%C3%B3w
#
# =====================
# Polish dictionary
# =====================
#
# Concept: to make things clear, easy to debug and to
# internationalize. Program *doesn't use words* but *filenames*.
# So, if somewhere in programme variable's value or function returnes 
# ie. *windy* it should be regarded as a *filename*, ``windy.ogg``.
#
# Beware too short words, it will be like machine gun rapid fire or
# will sound like a cyborg from old, cheap sci-fi movie. IMO the good way
# is to record longer phrases, like *"the temperature is"*, save it as
# ``the_temperature_is.ogg`` and use it's filename (``the_temperature_is``)
# as a return value.
#
# This dictionary is used by all SR0WX modules.

# * *"weather report for ... "* (ie. 4 may 2009)
weatherDate   =  "stan_pogody_z_dnia"

# * *"forecast for next ... hours"
forecast = "prognoza_na_nastepne"
hrs = ["","godziny","godzin"]

# * *"pressure ... hectopascals"*
pressure      = "cisnienie"
hPa = ["hektopaskal", "hektopaskale", "hektopaskali"]

# * *"humidity ... percent"*
humidity      = "wilgotnosc"
percent = [u"procent",u"procent",u"procent"]

# * *"wind speed ... meters per second / no wind"*
windSpeed     = "predkosc_wiatru"
windSpeedGusts = "w_porywach"
mPs    = ["metr_na_sekunde", "metry_na_sekunde", "metrow_na_sekunde"]
noWind = "bezwietrznie"
wind   = "wiatr"

# * *"wind strength ... Beaufort wind force scale"*
windStrength  = "sila_wiatru"
B   = ["stopien_w_skali_beauforta", "stopnie_w_skali_beauforta", \
    "stopni_w_skali_beauforta"]

# * *"wind direction ... degrees / variable wind direction"*
windDirection = "kierunek_wiatru"
deg = [u"stopien","stopnie","stopni"]
variableWindDirection = "zmienny"
windVarying = "skrajne_kierunki_wiatru"

# * *"temperarture ... centigrades"*
# * *"dew point ... centigrades"*
temperature = "temperatura"
dewPoint    = "punkt_rosy"
C   = ["stopien_celsjusza", "stopnie_celsjusza", "stopni_celsjusza"]

# * *"visibility ... kilometers"*
visibility = "widocznosc"
km  = ["kilometr", "kilometry", u"kilometrow"]


# * *"cloud cover" ... "sky clear"
cloudCover = "zachmurzenie"
clouds = {'SKC': 'bezchmurnie', 'FEW':'lekkie_zachmurzenie', 'SCT': 'zachmurzenie_umiarkowane',
        'BKN': 'silne_zachmurzenie', 'OVC':'zachmurzenie_calkowite', 'NSC':""}


# We need also local names for directions to convert two- or three letters
# long wind direction into words (first is used as prefix, second as suffix):
directions = { "N": ("północno ",   "północny"),
               "E": ("wschodnio ",  "wschodni"),
               "W": ("zachodnio ",  "zachodni"),
               "S": ("południowo ", "południowy") }

# These dictionaries are used by meteoalarm module.
meteoalarmAwarenesses = ["brak_zagrozen","silny_wiatr","snieg_lub_oblodzenie","burze","mgly",
    "wysokie_temperatury","niskie_temperatury","zjawiska_strefy_brzegowej",
    "pozary_lasow","lawiny","intensywne_opady deszczu","inne_zagrozenia"]
meteoalarmAwarenessLvl = ["nieokreslony","","niski","sredni","wysoki"]
meteoalarmAwarenessLevel = "poziom_zagrozenia"
meteoalarmRegions = {483: "łódzkiego", 479:"śląskiego", 482:"świętokrzyskiego",
    477:"dolnoslaskiego", 485:"kujawsko_pomorskiego", 487:"lubelskiego",
    474:"lubuskiego", 480:"malopolskiego", 489:"mazowieckiego", 478:"opolskiego",
    481:"podkarpackiego", 488:"podlaskiego",476:"pomorskiego", 
    486:"warminsko_mazurskiego", 484:"wielkopolskiego", 475:"zachodniopomorskiego" }
meteoalarmAwareness   = "zagrozenia_meteorologiczne dla_wojewodztwa"
meteoalarmNoAwareness = "brak_zagrozen_meteorologicznych dla_wojewodztwa"
today    = "dzis"
tomorrow = "jutro"



# ----------------
# common functions
# ----------------
#
# Some of functions below were taken from dowgird[#]_ implementation, I've
# made some changes.
#
# .. [#] http://code.google.com/p/pyliczba/ by dowgird
#
# dowgird's implementation uses some variables as dictionaries (not in Python
# meaning). I don't like these variables, but functions are working very well
# and this is most important.
#

jednostkiM = [u""] + u"jeden dwa trzy cztery pięć sześć siedem osiem dziewięć".split()
jednostkiF = [u""] + u"jedną dwie trzy cztery pięć sześć siedem osiem dziewięć".split()
dziesiatki = [u""] + u"""dziesięć dwadzieścia  trzydzieści czterdzieści
     pięćdziesiąt sześćdziesiąt siedemdziesiąt osiemdziesiąt dziewięćdziesiąt""".split()
nastki = u"""dziesięć jedenaście dwanaście trzynaście czternaście piętnaście
        szesnaście siedemnaście osiemnaście dziewiętnaście""".split()
setki = [u""]+ u"""sto dwieście trzysta czterysta pięćset sześćset siedemset osiemset
              dziewięćset""".split()

ws=u"""x x x
   tysiąc tysiące tysięcy
   milion miliony milionów
   miliard miliardy miliardów
   bilion biliony bilionów"""
wielkie = [ l.split() for l in ws.split('\n') ]

##zlotowki=u"""złoty złote złotych""".split()
##grosze=u"""grosz grosze groszy""".split()

# There are also some functions, by dowgird, so I haven't even looked into
# them.

def _slownie3cyfry(liczba, plec='M'):
    if plec=='M':
        jednostki = jednostkiM
    else:
        jednostki = jednostkiF

    je = liczba % 10
    dz = (liczba//10) % 10
    se = (liczba//100) % 10
    slowa=[]

    if se>0:
        slowa.append(setki[se])
    if dz==1:
        slowa.append(nastki[je])
    else:
        if dz>0:
            slowa.append(dziesiatki[dz])
        if je>0:
            slowa.append(jednostki[je])
    retval = " ".join(slowa)
    return retval

def _przypadek(liczba):
    je = liczba % 10
    dz = (liczba//10)  % 10

    if liczba == 1:
        typ = 0       #jeden tysiąc"
    elif dz==1 and je>1:  # naście tysięcy
        typ = 2
    elif  2<=je<=4:
        typ = 1       # [k-dziesiąt/set] [dwa/trzy/czery] tysiące
    else:
        typ = 2       # x tysięcy

    return typ

def lslownie(liczba, plec='M'):
    """Liczba całkowita słownie"""
    trojki = []
    if liczba==0:
        return u'zero'
    while liczba>0:
        trojki.append(liczba % 1000)
        liczba = liczba // 1000
    slowa = []
    for i,n in enumerate(trojki):
        if n>0:
            if i>0:
                p = _przypadek(n)
                w = wielkie[i][p]
                slowa.append(_slownie3cyfry(n, plec)+u" "+w)
            else:
                slowa.append(_slownie3cyfry(n, plec))
    slowa.reverse()
    return ' '.join(slowa)

def cosslownie(liczba,cos, plec='M'):
    """Słownie "ileś cosiów"

    liczba - int
    cos - tablica przypadków [coś, cosie, cosiów]"""
    #print liczba
    #print cos[_przypadek(liczba)]
    return lslownie(liczba, plec)+" " + cos[_przypadek(liczba)]

##def kwotaslownie(liczba, format = 0):
##    """Słownie złotych, groszy.
##
##    liczba - float, liczba złotych z groszami po przecinku
##    format - jesli 0, to grosze w postaci xx/100, słownie w p. przypadku
##    """
##    lzlotych = int(liczba)
##    lgroszy = int (liczba * 100 + 0.5 ) % 100
##    if format!=0:
##        groszslownie = cosslownie(lgroszy, grosze)
##    else:
##        groszslownie = '%d/100' % lgroszy
##    return cosslownie(lzlotych, przypzl) + u" " +  groszslownie
##

# As you remember, ``cardinal()`` must be defined, this is the function which
# will be used by SR0WX modules. This functions was also written by dowgrid,
# modified by me. (Is function's name proper?)
def cardinal(no, units=[u"",u"",u""], gender='M'):
    """Zamienia liczbę zapisaną cyframi na zapis słowny, opcjonalnie z jednostkami
w odpowiednim przypadku. Obsługuje liczby ujemne."""
    if no<0:
        return (u"minus " + cosslownie(-no, units, plec=gender)).replace(u"jeden tysiąc", u"tysiąc",1).encode("utf-8")
    else:
        return cosslownie(no, units, plec=gender).replace(u"jeden tysiąc", u"tysiąc",1).encode("utf-8")

# This one tiny simply removes diactrics (lower case only). This function
# must be defined even if your language doesn't use diactrics (like English),
# for example as a simple ``return text``.
def removeDiacritics(text):
    return text.replace("ą","a").replace("ć","c").replace("ę","e").\
        replace("ł","l").replace("ń","n").replace("ó","o").replace("ś","s").\
        replace("ź","z").replace("ż","z")

# The last one changes ISO structured date time into word representation.
# It doesn't return year value.
def readISODT(ISODT):
    _rv=() # return value
    y,m,d,hh,mm,ss= ( int(ISODT[0:4]),   int(ISODT[5:7]),   int(ISODT[8:10]),
                      int(ISODT[11:13]), int(ISODT[14:16]), int(ISODT[17:19]) )

    # miesiąc
    _M = ["","stycznia","lutego","marca","kwietnia","maja","czerwca","lipca",
         "sierpnia","września","października","listopada","grudnia"]
    Mslownie = _M[m]
    # dzień
    _j = ["","pierwszego","drugiego","trzeciego","czwartego","piątego","szóstego",
        "siódmego","ósmego","dziewiątego","dziesiątego","jedenastego",
        "dwunastego","trzynastego","czternastego","piętnastego","szesnastego",
        "siedemnastego","osiemnastego","dziewiętnastego"]
    _d = ["","","dwudziestego","trzydziestego"]

    if d<20: Dslownie = _j[d]
    else: Dslownie = " ".join( (_d[d/10], _j[d%10]) )

    _j = ["zero","pierwsza","druga","trzecia","czwarta","piąta","szósta",
          "siódma","ósma","dziewiąta","dziesiąta","jedenasta","dwunasta",
          "trzynasta","czternasta","piętnasta","szesnasta","siedemnasta",
          "osiemnasta","dziewiętnasta"]

    if hh<20: HHslownie = _j[hh]
    elif hh==20: HHslownie="dwudziesta"
    else: HHslownie = " ".join( ("dwudziesta", _j[hh%10]) )

    MMslownie = cardinal(mm).replace("zero","zero_zero")

    return " ".join( (Dslownie, Mslownie, "godzina", HHslownie, MMslownie) )

def readISODate(ISODate):
    _rv=() # return value
    y,m,d,hh,mm,ss= ( int(ISODate[0:4]),   int(ISODate[5:7]),   int(ISODate[8:10]),
                      int(ISODate[11:13]), int(ISODate[14:16]), int(ISODate[17:19]) )

    # miesiąc
    _M = ["","stycznia","lutego","marca","kwietnia","maja","czerwca","lipca",
         "sierpnia","września","października","listopada","grudnia"]
    Mslownie = _M[m]
    # dzień
    _j = ["","pierwszego","drugiego","trzeciego","czwartego","piątego","szóstego",
        "siódmego","ósmego","dziewiątego","dziesiątego","jedenastego",
        "dwunastego","trzynastego","czternastego","piętnastego","szesnastego",
        "siedemnastego","osiemnastego","dziewiętnastego"]
    _d = ["","","dwudziestego","trzydziestego"]

    if d<20: Dslownie = _j[d]
    else: Dslownie = " ".join( (_d[d/10], _j[d%10]) )

    return " ".join( (Dslownie, Mslownie) )

sunrise = "wschod_slonca"
sunset  = "zachod_slonca"
dayLength = "dlugosc_dnia"

mns = ["minuta","minuty","minut"]

def readHour(dt):
    return removeDiacritics(readISODT('0000-00-00 '+str(dt.hour).rjust(2, '0')+':'+str(dt.minute).rjust(2, '0')+':00'))

def readHourLen(hour):
    ss = hour.seconds
    hh = ss/3600
    mm = (ss-hh*3600)/60
    return removeDiacritics(" ".join( (cardinal(hh, hrs, gender='F'), cardinal(mm, mns, gender='F')) ))


gopr_region = ["", "w_karkonoszach obowiazuje", "", "w_regionie_babiej_gory obowiazuje", "w_pieninach obowiazuje", "w_bieszczadach obowiazuje"]
avalancheLevel = ['']+[i+' stopien_zagrozenia_lawinowego' for i in ['pierwszy', 'drugi', 'trzeci', 'czwarty', 'piaty najwyzszy'] ]
gopr_tendention = ['', '', 'tendencja_spadkowa', 'tendencja_wzrostowa']
info_at = 'komunikat_z_dnia'

hscr_welcome= "komunikat czeskiej_sluzby_ratownictwa_gorskiego"
hscr_region = {"K": "w_karkonoszach obowiazuje", "J": "w_jesionikach_i_masywie_snieznika obowiazuje"}
hscr_tendention = ['', '', 'tendencja_spadkowa', 'tendencja_wzrostowa']
