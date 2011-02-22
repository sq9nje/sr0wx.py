#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# 
# Copyright 2009-2011 Michal Sadowski (sq6jnx at hamradio dot pl).
#  
# Future versions of this software will probably be licensed under
# some open source license, but this experimental version is not.
# Copying and distribution without the author's explicit permission.
# is not allowed.
# 
# Przyszle wersje tego oprogramowania beda prawdopodobnie udostepniane
# na jednej z open source'owych licencji, jednakze ta, eksperymentalna
# wersja nie jest. Kopiowanie i dystrybuowanie tego oprogramowania bez
# wyraznej zgody autora jest zabronione.
# 
#
# ********
# taf.py
# ********
#

import sys
import lib.taf as pytaf
import datetime
import debug 

from config import taf as config

lang=None

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def translateWindDirections(directions, deg=True, compass=True, short=False):
    global lang
    tmp = ""
    comp = ['N','NNE','NE','ENE','E','ESE','SE','SSE',
            'S','SSW','SW','WSW','W','WNW','NW','NNW']

    if len(directions)==1:
        if directions[0] == "VRB":
            return lang.variableWindDirection
        else:
            return lang.cardinal(directions[0],lang.deg)
    elif len(directions)==3:
        lang.variableWindDirection
        if directions[0]<>"VRB":
            tmp = " ".join( (tmp, comp[int((directions[0]/22.5)%15)]) )
            tmp = " ".join( (tmp, lang.cardinal(directions[0],lang.deg)) )
        tmp = " ".join( (tmp, lang.windVarying) )
        tmp = " ".join( (tmp, comp[int((directions[1]/22.5)%15)]) )
        tmp = " ".join( (tmp, lang.cardinal(directions[1],lang.deg)) )
        tmp = " ".join( (tmp, comp[int((directions[2]/22.5)%15)]) )
        tmp = " ".join( (tmp, lang.cardinal(directions[2],lang.deg)) )
    return tmp

# OK. This function **must** be defined in every module. 
# I think it's quite easy to find out what's happening in here.
def getData(l):
    global lang
    data = {"data":"", "needCTCSS":False, "allOK":True}

    lang = my_import(l+"."+l)

    d=datetime.datetime.utcnow()
    dd,hh,mm = d.strftime("%d %H %M").split()
 
    taf = pytaf.taf(ICAO=config.ICAOAirportCode,at=( int(dd),int(hh)+config.forecastingPeriod,int(mm) ))

    debug.log("TAF", "Raw TAF:\n%s"%taf.rawTAF)
    debug.log("TAF", "Used forecast:%s"%taf.weather)
    
    _weather = " ".join( (lang.forecast, lang.cardinal(3, lang.hrs)) )

    if config.temperatureCelsius and taf.getTemperature() is not None:
        _weather = " ".join( (_weather, lang.temperature,\
		lang.cardinal(taf.getTemperature(), lang.C)) )

    if config.skyConditions and taf.getSkyConditions() is not None:
        _weather = " ".join( (_weather, lang.clouds[taf.getSkyConditions()]) )

    if config.visibilityKilometers and taf.getVisibility() is not None:
        _weather = " ".join( (_weather, lang.visibility,\
		lang.cardinal(int(taf.getVisibility()), lang.km)) ) 

    if config.weather and taf.getWeather() is not None:
        _weather = " ".join( (_weather, taf.getWeather().lower()) ) 
    #else: 
    #    _weather = " ".join( (_weather, "no significant weather?") ) 

    if config.pressureHPa and taf.getPressure() is not None:
        _weather = " ".join( (_weather, lang.pressure,\
		lang.cardinal(taf.getPressure(), lang.hPa)) ) 

    if taf.getWindSpeed() == 0: 
        if config.windSpeedMPS or config.windDirectionDegrees:
            _weather = " ".join( (_weather, lang.noWind) )
    else:
        if config.windSpeedMPS or config.windDirectionDegrees:
            _weather = " ".join( (_weather, lang.windDirection) )
        if config.windDirectionDegrees:
            _weather = " ".join( (_weather, translateWindDirections(taf.getWindDirection())) ) 
        if config.windSpeedMPS:
            _weather = " ".join( (_weather, lang.windStrength, translateWindSpeed(taf.getWindSpeed())) ) 

    data["data"]= lang.removeDiacritics(_weather)
    debug.log("TAF", "finished")
    return data


def translateWindSpeed(speed):
    if len(speed) == 1:
        return lang.cardinal(speed[0], lang.mPs)
    else:
        #return " ".join( (lang.cardinal(speed[0], lang.mPs), lang.windSpeedGusts, 
        #    lang.cardinal(speed[1], lang.mPs)) )
        return " ".join( (lang.cardinal(speed[0], lang.mPs), lang.windSpeedGusts, lang.cardinal(speed[1], lang.mPs)) )


def direction(dir, short=False):
    global lang
    _dir = ""
    if len(dir)==3 and short==True:
        dir = dir[1:3]
    for i in range(0,len(dir)-1):
        _dir = _dir + lang.directions[dir[i]][0]
    _dir = _dir + lang.directions[dir[-1]][1]

    return _dir


