# -*- coding: utf-8 -*-

import vmdetect
if vmdetect.checkVMware():
	print "Sandbox Detected !!"
else:
	print "We are OK"
