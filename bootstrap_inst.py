#!/usr/bin/env python
import zipfile
import sys
import tempfile
import shutil
import os
import getopt

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

	MACOSX_DIR = tmpdir+"/__MACOSX"

	if os.path.isdir(MACOSX_DIR) == True:
		shutil.rmtree(MACOSX_DIR)

	local_bootstrap_dir = find_bootstrap_dir(tmpdir)
	if local_bootstrap_dir == None:
		print "Failed to find bootstrap directory in zip contents."
		exit(1)

	scp_cmd = "scp -r -P "+device_port+" "+local_bootstrap_dir+" root@"+device_ip+":/"
	# print scp_cmd # useful for debugging the scp command
	# exit(0)
	os.system(scp_cmd)

	# clean up tmp dir
	shutil.rmtree(tmpdir)
	pass

def usage(exit_code):
	print "\nUsage: ./bootstrap_inst.py --ip <ip_addr> --port <device_port> --file <path_to_archive> [--theos]\n"
	print "Example: ./bootstrap_inst.py --ip 127.0.0.1 --port 2222 --file tweak.zip"
	print "Theos Example: ./bootstrap_inst.py --file tweak.zip --theos"
	exit(exit_code)
	pass

def theos_mode():
	global device_ip
	global device_port

	if os.environ.has_key("THEOS_DEVICE_IP") == True:
		device_ip = os.environ["THEOS_DEVICE_IP"]

	if os.environ.has_key("THEOS_DEVICE_PORT") == True:
		device_port = os.environ["THEOS_DEVICE_PORT"]

	if device_ip == None:
		print "Device IP cannot be nothing. Try changing THEOS_DEVICE_IP to the IP address of your iOS device."
		usage(1)

	pass

def main():
	global device_ip
	global device_port
	input_file = None
	use_theos = False

	try:
		opts, args = getopt.getopt(sys.argv[1:], 'i:p:hf:t', ['ip=', 'port=', 'help', 'file=', 'theos'])
	except getopt.GetoptError:
		usage(2)

	for opt, arg in opts:
		if opt in ('-h', '--help'):
			usage(2)
		elif opt in ('-i', '--ip'):
			device_ip = arg
		elif opt in ('-p', '--port'):
			device_port = arg
		elif opt in ('-f', '--file'):
			input_file = arg
		elif opt in ('-t', '--theos'):
			use_theos = True
		else:
			usage(2)

	if input_file == None:
		print "No input file -f or --file not specified."
		usage(1)

	if use_theos == True:
		theos_mode()
	
	if device_ip == None:
		print "Device IP cannot be nothing. Try specifying --ip or --theos."
		usage(1)

	install_zip(input_file, device_ip, device_port)

	return 0


exit(main())