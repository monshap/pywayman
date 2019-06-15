#! /usr/bin/env python

"""
Get Windows backgrounds and copy them to PicAttempts folder
"""

import os
import re
from shutil import copy, copy2
import cv2


class fileobj(object):

	def __init__(self, directory, name):
		"""Gets properties of file with specified directory and name.
		
		Args
		----
		directory : str
			directory of file
		name : str
			name of file	
		"""
		super(fileobj, self).__init__()
		self.dir = directory
		self.name = name

		path = os.path.join(self.dir, self.name)
		size = os.path.getsize(path)
		mdate = os.path.getmtime(path)
		tdate = os.path.getctime(path)
		self.path = path
		self.size = size*1e-3
		self.date = mdate
		self.tdate = tdate

	def dim_check(self, w=1920, h=1080):
		"""Check if file has correct dimensions.
		
		Keywords
		--------
		w : int, optional
			display width (px), by default 1920
		h : int, optional
			display height (px), by default 1080
		
		Returns
		-------
		boolean
			returns True if image dimensions match, else returns false
		"""
		im = cv2.imread(self.path)
		imdims = (im.shape[1], im.shape[0])
		dims = (w, h)
		if imdims == dims:
			return True
		else:
			return False


def pull_all(directory, smin=0, smax=1600):
	"""Pull files within specified size range.
	
	Args
	----
	directory : str
		directory to search in
	
	Keywords
	--------
	smin : int, optional
		minimum file size (in KB), by default 0
	smax : int, optional
		maximum file size (in KB), by default 1600
	
	Returns
	-------
	dict
		dictionary with filenames as keys and fileobjs as values
	"""
	names = os.listdir(directory)
	files = {}
	for name in names:
		file = fileobj(directory, name)
		if (file.size < smin) or (file.size > smax):
			pass
		else:
			files[name] = file
	return files


def newest_tstamp(files):
	"""Get timestamp of most recently added file."""
	tmax = [files[name].date for name in files]
	if tmax:
		return max(tmax)
	else:
		return 0


def copy_picture(file, destdir):
	"""Copy file to desired location and convert to JPEG file"""
	srcpath = file.path
	destpath = os.path.join(destdir, file.name) + '.jpg'
	_ = copy2(srcpath, destpath)
	tmpfile = fileobj(destdir, file.name + '.jpg')
	if tmpfile.dim_check():
		pass
	else:
		os.remove(destpath)


def pylfer(usrpath=None):
	"""Main function to copy files from Windows location to user-defined
	   location.
	
	Keywords
	--------
	usrpath : str, optional
		path location to copy images to, by default None
		if None, will open a prompt to locate directory
	"""
	import tkinter as tk
	from tkinter import filedialog

	packdir = os.path.expandvars("%LOCALAPPDATA%\Packages")
	dirs = os.listdir(packdir)
	regex = re.compile("Microsoft\.Windows\.ContentDeliveryManager_\w*")
	try:
		for f in dirs:
			if regex.match(f):
				winpath = os.path.join(packdir, f, "LocalState", "Assets")
			else:
				pass
		if usrpath:
			pass
		else:
			root = tk.Tk()
			usrpath = filedialog.askdirectory()
			root.withdraw()
		usrfiles = pull_all(usrpath)
		winfiles = pull_all(winpath)
		t_win = newest_tstamp(winfiles)
		t_usr = newest_tstamp(usrfiles)
		if t_win > t_usr:
			for name in winfiles.keys():
				if winfiles[name].date > t_usr:
					copy_picture(winfiles[name], usrpath)
				else:
					pass
		else:
			print("Most recent pictures have already been copied!")
			print("They can be found at '%s'" % (usrpath))
	except Exception as e:
		print(e)
		print("Windows content delivery folder not found.")
		print("Please check that lockscreen photos are enabled!")


if __name__ == '__main__':
	pylfer()
