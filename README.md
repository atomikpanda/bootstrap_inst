# bootstrap_inst

install a zip with a boostrap folder into /bootstrap on a jailbroken device (Electra)

Usage: ./bootstrap_inst.py --ip <ip_addr> --port <device_port> --file <path_to_archive> [--theos]


Example: ./bootstrap_inst.py --ip 127.0.0.1 --port 2222 --file tweak.zip
Theos Example: ./bootstrap_inst.py --file tweak.zip --theos


To create your own zip to install simply make a folder somewhere on your Mac, then make a bootstrap folder inside of that.


	mypackage

	└── bootstrap

   		 └── lol.txt
    
   		 └── Library
    
    
then zip mypackage to mypackage.zip

whatever files are placed in the boostrap dir will be copied to your device.
