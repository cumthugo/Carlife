import os
import re
import commands
import time
import socket
import carlife_pb2 as pb

header_str_of_adb = ''
def start_send_msg_cmd_to_phone():
    s = socket.socket()
    host = "127.0.0.1"
    port = 7200
    print 'host',host
    s.connect((host,port))
    print host,'connected'
    data = '\x00\x04\x00\x00\x00\x01\x80\x01'

    version = pb.CarLifeProtocolVersion()
    version.majorVersion = 2
    version.minorVersion = 0
    data += version.SerializeToString()
    s.send(data)
    print 'data:',data
    print s.recv(1024)
    
def start_connect():
    global header_str_of_adb
    print 'wait for phone injection...'
    errorno = os.system("adb -d wait-for-device")
    dev_str = commands.getoutput("adb -d devices")
    dev_id = re.findall('\n(\w+)\tdevice\n',dev_str)[0]
    print dev_id, ' inserted.'

    header_str_of_adb = "adb -s " + dev_id + " "

    prop_str = commands.getoutput(header_str_of_adb + "shell getprop")
    #print prop_str
    android_ver = re.findall('\n\[ro\.build\.version\.release\]: \[(\d\.\d\.\d)\]',prop_str)[0]
    print 'android version:', android_ver


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
        print 'start launch carlife...'
        temp_str = commands.getoutput(header_str_of_adb + "shell am start -n com.baidu.carlife/.CarlifeActivity")
        start_send_msg_cmd_to_phone()
    else:
        print 'there is no carlife in you phone, please download it, thanks.'


if __name__ == '__main__':
    while 1:
        start_connect()
        while 1:
            error_no,output_str = commands.getstatusoutput(header_str_of_adb + "shell ls")
            if error_no:
                print 'phone has pulg out, end.\n\n\n'
                break
            time.sleep(0.2)
