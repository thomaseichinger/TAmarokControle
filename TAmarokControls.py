#! /usr/bin/python
# -*- coding: utf-8 -*-
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor,
#    Boston, MA  02110-1301, USA.
#
#    ---
#    Copyright (C) 2009, Thomas Eichinger <thomas.eichinger1@gmail.com>

#
# http://wiki.xmms2.xmms.se/wiki/MPRIS
#

import dbus

class TAmarokControls( ):
  def __init__( self ):
    bus = dbus.SessionBus()
    try:
      app_proxy = bus.get_object( 'org.kde.amarok', '/' )
      self.app = dbus.Interface( app_proxy, 'org.freedesktop.MediaPlayer' )
      player_proxy = bus.get_object( 'org.kde.amarok', '/Player' )
      self.player = dbus.Interface( player_proxy, 'org.freedesktop.MediaPlayer' )
      tList_proxy = bus.get_object( 'org.kde.amarok', '/TrackList')
      self.trackList = dbus.Interface( tList_proxy, 'org.freedesktop.MediaPlayer' )
    except dbus.exceptions.DBusException:
      import sys
      from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
      from PyKDE4.kdeui import KMainWindow, KMessageBox, KApplication

      about = KAboutData("msgbox", "msgbox", ki18n ("TAmarok"), "0.1", ki18n(""), KAboutData.License_GPL,
                          ki18n ( "(c) 2009 Thomas Eichinger" ), ki18n(""), "", "")
      KCmdLineArgs.init(sys.argv, about)
      app = KApplication()
      win = KMainWindow()
      if KMessageBox.warningYesNo(win, "Oops, found no Amarok instance.\n Start Amarok now?" ) == 3 :
        import subprocess
        self.out = ""
        subprocess.Popen("amarok")
        import time
        time.sleep(3)
        app_proxy = bus.get_object( 'org.kde.amarok', '/' )
        self.app = dbus.Interface( app_proxy, 'org.freedesktop.MediaPlayer' )
        player_proxy = bus.get_object( 'org.kde.amarok', '/Player' )
        self.player = dbus.Interface( player_proxy, 'org.freedesktop.MediaPlayer' )
        tList_proxy = bus.get_object( 'org.kde.amarok', '/TrackList')
        self.trackList = dbus.Interface( tList_proxy, 'org.freedesktop.MediaPlayer' )
      else:
        print "*E* Sorry no Amarok running"
        quit()

  def getPlayerIdentity( self ):
    self.app.Identity()
    
  def quit( self ):
    self.app.Quit()

##################################
##		Player manipulation		##
##################################
  def triggerPlay( self ):
    self.player.Play()

  def triggerStop( self ):
    self.player.Stop()

  def triggerNext( self ):
    self.player.Next()
    
  def triggerPrevious( self ):
    self.player.Prev()

  def togglePlayPause( self ):
    status = self.player.GetStatus()
    if int(status[0]) is 1:
      self.player.Play()
    elif int(status[0]) is 0:
      self.player.Pause()

  def increaseVol( self, i=5 ):
    now = self.player.VolumeGet()
    self.setVolume( int(now)+i )
 
  def decreaseVol( self, i=5 ):
    self.setVolume( int(self.player.VolumeGet())-i )

  def setVolume( self, i ):
    self.player.VolumeSet( int(i) )

	# The unit for position manipulation is ms
	# example:
	# amarok.increasePos( 1000 )			=> forward for 1 sec
	# amarok.decreasePos( 10000 )			=> rewind for 10 sec
	# amarok.setPosition( 1000*60*3.5 )		=> position is 3min30sec ;)
  def increasePos( self, p=5 ):
    self.setPosition( int(self.player.PositionGet())+p )

  def decreasePos( self, p=5 ):
    self.setPosition( int(self.player.PositionGet())-p )

  def setPosition( self, p ):
    self.player.PositionSet( p )

  def toggleTrackRepeat( self ):
    status = self.player.GetStatus()
    now = bool(status[2])
    self.player.Repeat( not now )

  def getMetaData( self, key='all' ):
    data = self.player.GetMetadata()
    if key is 'all':
      return data
    if key is 'album':
      return data['album']
    if key is 'artist':
      return data['artist']


######################################
##		TrackList manipulation		##
######################################




def main():
  amarok = TAmarokControls()
  ## an example usage
  amarok.increaseVol()

if __name__ == "__main__":
  main()