#!/usr/bin/env python
import zipfile
import sys
import tempfile
import shutil
import os

device_ip = None
device_port = "22"

def find_bootstrap_dir(base_dir):
	for root, dirs, files in os.walk(base_dir):
		path = root.split(os.sep)
		for adir in dirs:
			if adir == "bootstrap":
				current_bootsrap = os.sep.join(path)+os.sep+adir
				# print "found bootstrap dir at " + current_bootsrap
				return current_bootsrap
	return None


def install_zip(path, device_ip, device_port):
	print("installing on "+device_ip+" port "+device_port)
	tmpdir = tempfile.mkdtemp()

	with zipfile.ZipFile(path,"r") as zip_ref:
		zip_ref.extractall(tmpdir)

	shutil.rmtree(tmpdir+"/__MACOSX")
	local_bootstrap_dir = find_bootstrap_dir(tmpdir)
	if local_bootstrap_dir == None:
		print "Failed to find bootstrap directory in zip contents."
		exit(1)

	scp_cmd = "scp -r -P "+device_port+" "+local_bootstrap_dir+" root@"+device_ip+":/bootstrap"
	print scp_cmd
	# exit(0)
	os.system(scp_cmd)

	# os.system("open "+tmpdir)
	# clean up tmp dir
	shutil.rmtree(tmpdir)
	pass

def main():
	global device_ip
	global device_port

	if os.environ.has_key("THEOS_DEVICE_IP") == True:
		device_ip = os.environ["THEOS_DEVICE_IP"]

	if os.environ.has_key("THEOS_DEVICE_PORT") == True:
		device_port = os.environ["THEOS_DEVICE_PORT"]

	
	if device_ip == None:
		print "Device IP cannot be nothing. Try changing THEOS_DEVICE_IP to the IP address of your iOS device."
		exit(1)

	
	install_zip(sys.argv[1], device_ip, device_port)
	pass


main()