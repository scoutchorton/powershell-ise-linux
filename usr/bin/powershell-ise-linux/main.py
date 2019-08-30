#!/usr/bin/env python

#
#	Imports
#
import os
import sys
import gi
import re
from gi.repository import GLib
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte

global builder, pwsh

cwd = __file__.split('main.py')[0]

#
#	Functions
#
def parseText(text):
	#Remove blank lines
	textArr = text.split('\n')
	while textArr.count(''):
		textArr.pop(textArr.index(''))
	#Remove comments
	#Finish
	return '\n'.join(textArr)


def runCommands(evt):
	#print 'Running program...'
	buffer = builder.get_object('buffer-program-editor')
	text = parseText(buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), True)) + '\r'
	pwsh.feed_child(text, len(text))
	#print text



#
#	GTK/Glade
#
pwsh = Vte.Terminal()
pwsh.spawn_sync(Vte.PtyFlags.DEFAULT, os.environ['HOME'], ['/snap/bin/pwsh'], [], GLib.SpawnFlags.DO_NOT_REAP_CHILD, None, None)

builder = Gtk.Builder()
builder.add_from_file(cwd + 'powershell.glade')

terminalWrapper = builder.get_object('main-editor-box')
terminalWrapper.add(pwsh)

handlers = {
	'function-run': runCommands,
	'function-quit': Gtk.main_quit
}
builder.connect_signals(handlers)

window = builder.get_object('window-main')
window.show_all()

Gtk.main()
