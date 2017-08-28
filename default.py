#
#  Skin by: Tron Wizard for Kodi
#  YouPorn Code by Echo Coder
#
#  Copyright (C) 2016 
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import os
import sys
import urllib
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import time
import base64
import requests
import re
import xbmcvfs
import urllib2,urllib

DIALOG          = xbmcgui.Dialog()
DP              = xbmcgui.DialogProgress()
HOME            = xbmc.translatePath('special://home/')
ADDONS          = os.path.join(HOME,     'addons')
USERDATA        = os.path.join(HOME,     'userdata')
ADDON           = xbmcaddon.Addon()
ADDONID         = ADDON.getAddonInfo('id')
ADDONVERSION    = ADDON.getAddonInfo('version')
CWD             = ADDON.getAddonInfo('path').decode('utf-8')
ACTION_PREVIOUS_MENU = 10
ACTION_SELECT_ITEM = 7

AddonTitle = 'You Porn'
#Default veriables

NEW_VIDS        = 'http://www.youporn.com/'
TOP_VIDS        = 'http://www.youporn.com/top_rated/'
MOST_FAV        = 'http://www.youporn.com/most_favorited/'
MOST_VIEW       = 'http://www.youporn.com/most_viewed/'
MOST_DIS        = 'http://www.youporn.com/most_discussed/'

class WindowXML(xbmcgui.WindowXML):
    def onInit(self):
        #Put list populating code/GUI startup things here
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        self.list_control = self.window.getControl(401)
        self.pornvids = self.window.getControl(402)
        self.categories()
        self.GET_CONTENT(NEW_VIDS,self.pornvids)

    def categories(self):
        result = requests.get('http://www.youporn.com/categories')
        match = re.compile("id='categoryList'>(.+?)<div class='title-bar sixteen-column'>",re.DOTALL).findall(result.content)
        string = str(match)
        match2 = sorted(re.compile("<a h(.+?)</p>",re.DOTALL).findall(string))
        fail = 0
        videos = 0
        for item in match2:
            url=re.compile('ref="(.+?)"').findall(item)[0]
            title=re.compile('alt="(.+?)"').findall(item)[0]
            icon_cat=re.compile('original="(.+?)"').findall(item)[0]
            a = str(icon_cat)
            icon_cat = a.replace(' ','%20')
            if "http" not in str(icon_cat):
                icon_cat = icon
            number=re.compile('<span>(.+?)</span>').findall(item)[0]
            b = str(number)
            c = b.replace(',','').replace(' Videos','')
            videos = videos + int(float(c))
            url3 = url
            url4 = url3.replace('\\','')
            url = "http://www.youporn.com" + url4
            name = "[COLOR rose][B]" + title + " - " + number + "[/B][/COLOR]"
            self.list_control.addItem(xbmcgui.ListItem(name, label2=url, iconImage=icon_cat, thumbnailImage=icon_cat))

    def GET_CONTENT(self,url,currentlist):
        global souperback
        global souperbad
        checker = url
        result = requests.get(url)
        match = re.compile('video-box four-column(.+?)<div class="video-box-title">',re.DOTALL).findall(result.content)
        for item in match:
            try:
                title=re.compile("alt=(.+?)'").findall(item)[0]
                url=re.compile('<a href="(.+?)"').findall(item)[0]
                iconimage=re.compile('<img src="(.+?)"').findall(item)[0]
                if "icon-hd-text" in item:
                    name = "[B][COLOR orangered]HD[/COLOR][COLOR rose] - " + title + "[/COLOR][/B]"
                    name = name.replace("'",'')
                    currentlist.addItem(xbmcgui.ListItem(name, label2=url, iconImage=iconimage, thumbnailImage=iconimage))
                else:
                    name = "[B][COLOR yellow]SD[/COLOR][COLOR rose] - " + title + "[/COLOR][/B]"
                #name = name.replace("'",'')
                #xbmc.log(url)
                #currentlist.addItem(xbmcgui.ListItem(name, label2=url, iconImage=iconimage, thumbnailImage=iconimage))
            except: pass
#       try:
        np=re.compile('<li class="current"(.+?)<div id="next">',re.DOTALL).findall(result.content)
        for item in np:
            current=re.compile('<div class="currentPage" data-page-number=".+?">(.+?)</div>').findall(item)[0]
            url2=re.compile('<a href="(.+?)=').findall(item)[0]
            next1 = int(float(current)) + 1
            url = "http://youporn.com" + str(url2) + "=" + str(next1)
            souperbad = url
            if next1 != 2:
                back1 = int(float(current)) - 1
                souperback = "http://youporn.com" + str(url2) + "=" + str(back1)
            else:
                souperback = "http://youporn.com" + str(url2) + "=" + str(1)
    def SEARCH(self):
        string =''
        keyboard = xbmc.Keyboard(string, 'Enter Search Term')
        keyboard.doModal()
        if keyboard.isConfirmed():
            string = keyboard.getText().replace(' ','').capitalize()
            if len(string)>1:
                url = "http://www.youporn.com/search/?query=" + string + "&page="
                xbmc.log(url)
                self.GET_CONTENT(url,self.pornvids)
            else: quit()
    def open_url(self, url,output=None):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
        response = urllib2.urlopen(req)
        if output == 'headers':
            result = response.headers
            response.close()
            return result
        else: 
            link = response.read()
            return link
    def PLAY_URL(self,name,url,iconimage):
        xbmc.executebuiltin("ActivateWindow(busydialog)")
        url = "http://www.youporn.com" + url
        r = self.open_url(url)
        s = re.findall('\w*\s*:\s*\"([^\"]*)', r) + re.findall('\w*\s*:\s*\'([^\']*)', r)
        s = [i for i in s if (urlparse.urlparse(i).path).strip('/').split('/')[-1].split('.')[-1] in ['mp4', 'flv', 'm3u8']]
        self.u = []; threads = []
        def sort_link(i):
            try:
                c = self.open_url(i, output='headers')
                checks = ['video','mpegurl','html']
                if any(f for f in checks if f in c['Content-Type']): self.u.append((i, int(c['Content-Length'])))
            except:
                pass
        for i in s: threads.append(Thread(sort_link, i))
        [i.start() for i in threads] ; [i.join() for i in threads]
        
        try:
            u = sorted(self.u, key=lambda x: x[1])[::-1]
            url_play = u[0][0]
        except: 
            xbmc.executebuiltin("Dialog.Close(busydialog)")
            quit()
        xbmc.executebuiltin("Dialog.Close(busydialog)")
        liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        xbmc.Player ().play(url_play, liz, False)     
    def onAction(self, action):
        if action == ACTION_PREVIOUS_MENU:
            self.close()
    def onClick(self,controlID):
        if controlID == 402:
            name = xbmc.getInfoLabel('Container(402).Listitem.Label')
            url = xbmc.getInfoLabel('Container(402).Listitem.Label2')
            icon = xbmc.getInfoLabel('Container(402).Listitem.Icon')
            self.PLAY_URL(name,url,icon)
        if controlID == 401:
            name = xbmc.getInfoLabel('Container(402).Listitem.Label')
            url = xbmc.getInfoLabel('Container(401).Listitem.Label2')
            try:
                while name:
                    self.pornvids.removeItem(0)
            except:
                self.GET_CONTENT(url,self.pornvids)
                xbmc.log(self.soup)
        if controlID == 502:
            name = xbmc.getInfoLabel('Container(402).Listitem.Label')
            try:
                while name:
                    self.pornvids.removeItem(0)
            except:
                xbmc.log(souperbad)
                self.GET_CONTENT(souperbad,self.pornvids)
        if controlID == 501:
            name = xbmc.getInfoLabel('Container(402).Listitem.Label')
            try:
                while name:
                    self.pornvids.removeItem(0)
            except:
                self.GET_CONTENT(souperback,self.pornvids)
                xbmc.log(souperback)
        if controlID == 503:
            self.close()
        if controlID == 504:
            name = xbmc.getInfoLabel('Container(402).Listitem.Label')
            try:
                while name:
                    self.pornvids.removeItem(0)
            except:
                self.SEARCH()
    def onFocus(self,controlID):
        pass
import threading
class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        self._target(*self._args)
if __name__ == "__main__":
    scriptDir = xbmcaddon.Addon('plugin.video.youporn').getAddonInfo('path')
    sys.path.insert(0, os.path.join(scriptDir, 'resources', 'src'))
    w = WindowXML("home.xml", scriptDir)
    w.doModal()
    del w