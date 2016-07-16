import os
import re
import commands
ret = os.system("adb -d wait-for-device")
dev_str = commands.getoutput("adb -d devices")
dev_id = re.findall('\n(\w+)\tdevice\n',dev_str)[0]
print dev_id

header_str_of_adb = "adb -s " + dev_id + " "

prop_str = commands.getoutput(header_str_of_adb + "shell getprop")
#print prop_str
android_ver = re.findall('\n\[ro\.build\.version\.release\]: \[(\d\.\d\.\d)\]',prop_str)[0]
print android_ver


#forward operation

os.system(header_str_of_adb + "forward tcp:7200 tcp:7240")
os.system(header_str_of_adb + "forward tcp:8200 tcp:8240")
os.system(header_str_of_adb + "forward tcp:9200 tcp:9240")
os.system(header_str_of_adb + "forward tcp:9201 tcp:9241")
os.system(header_str_of_adb + "forward tcp:9202 tcp:9242")
os.system(header_str_of_adb + "forward tcp:9300 tcp:9340")


#check carlife exist or not
list_package_str = commands.getoutput(header_str_of_adb + "shell pm list packages")
has_carlife = list_package_str.find('baidu.carlife') != -1

if has_carlife:
    #launch carlife
    temp_str = commands.getoutput(header_str_of_adb + "shell am start -n com.baidu.carlife/.CarlifeActivity")
else:
    print 'there is no carlife in you phone, please download it, thanks.'

