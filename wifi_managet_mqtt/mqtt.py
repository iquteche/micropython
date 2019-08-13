import network
import socket
from umqttsimple import MQTTClient
from machine import Pin,Timer,RTC
import ubinascii
import machine
import time
import net
# from localtime import Rtc
import time
port=800
wlan=None
s=None
wlan=network.WLAN(network.AP_IF)
wlan.active(True)
station=network.WLAN(network.STA_IF)
station.active(True)
class Wifi(object):
    # rtc=Rtc()
    c=None
    ssid=""
    password=""
    server=""
    led = Pin(2, Pin.OUT, value=1)
    button=Pin(0,Pin.IN)
    clients = ubinascii.hexlify(machine.unique_id())
    client=clients.decode()
    topic = b"kembang"
    state = ""
    timer=Timer(0)
    timer2=Timer(1)
    status=0
    nyala_pada_1=""
    nyala_pada_2=""
    nyala_pada_3=""
    nyala_pada_4=""
    mati_pada_1=""
    mati_pada_2=""
    mati_pada_3=""
    mati_pada_4=""
    waktu=""
    
    
    # menit=0
    def __init__(self,*args,**kwargs):
        super(Wifi,self).__init__(*args,**kwargs)
        self.button.irq(trigger=Pin.IRQ_RISING,handler=self.func)
        self.start_ap()
        self.start_mqtt()
    def tim2(self,dt):
        pass
    def func(self,dt):
        self.ap()
    def start_ap(self):
        print("menunggu....")
        time.sleep(5)
        if station.isconnected()==True:
            print("sudah konek")
            return
        self.ap()
    def ap(self):
        self.timer.deinit()
        station.disconnect()
        while(wlan.ifconfig()[0]=='0.0.0.0'):
            time.sleep(1)
        print(wlan.ifconfig())
        try:
            print("tcp sedang menuggu")
            ip=wlan.ifconfig()[0]     
            s = socket.socket()     
            s.bind(("192.168.4.1",800))    
            s.listen(1)          
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
            station.disconnect()
            while True:
                if self.status==1:
                    break
                print("acepting....")
                conn,addr = s.accept()     
                print(addr,"connected")
                while True:
                    data = conn.recv(1024)              
                    if(len(data) == 0):
                        print("close socket")
                        conn.close()                
                        break
                    print(data)
                    str_data=data.decode()
                    print(str_data)
                    if "connect" in str_data:
                        print("conceting AP")
                        paket=str_data.split("-")
                        print(paket)
                        t=("ssid=\"{}\"".format(paket[1]),"pwd=\"{}\"".format(paket[2]),"server=\"{}\"".format(paket[3]))
                        print(t)
                        f=open("net.py","w")
                        f.write("\n".join(t))
                        f.close()
                        self.server=paket[3]
                        print(self.server)
                        station.connect(paket[1],paket[2])
                        conn.send("data diterima") 
                    if str_data=="scan":
                        lis=[]
                        nets=station.scan()
                        for nt in nets:
                            name = str(nt[0], 'utf8')
                            lis.append(name)
                            print(lis)
                        conn.send(str(lis))
                    if str_data=="exit":
                        self.status=1
                        break
                    if str_data=="tanya":
                        print(station.isconnected())
                        if station.isconnected()==True:
                            conn.send("terhubung")
                            return self.start_mqtt()
                            self.status=1
                            break
                        else:
                            conn.send("belum terhubung")
        except:
            print("gagal cok")
            if(s):
                s.close()
            wlan.active(False)
    def start_mqtt(self):
        try:
            self.c = MQTTClient(self.clients, net.server)   
            self.c.connect()
        except:
            self.c = MQTTClient(self.clients, self.server) 
            self.c.connect()
        try:
            print("mulai mqtt")
            self.c.set_callback(self.sub_cb)
            self.c.subscribe(self.topic)
            self.c.subscribe(b"waktu")
            
            self.c.subscribe(b"nyala_pada_1")
            self.c.subscribe(b"nyala_pada_2")
            self.c.subscribe(b"nyala_pada_3")
            self.c.subscribe(b"nyala_pada_4")

            self.c.subscribe(b"mati_pada_1")
            self.c.subscribe(b"mati_pada_2")
            self.c.subscribe(b"mati_pada_3")
            self.c.subscribe(b"mati_pada_4")

            
            
            
            print("Connected to %s, subscribed to %s topic" % (self.server,self.topic))
            while 1:
                self.timer.deinit()
                self.state="terhubung"
                self.c.wait_msg()
        except:
            print("pedot")
            self.state="terputus"
            self.timer.init(period=1000,callback=self.tim)
    def sub_cb(self,topic, msg):
        strtopic=topic.decode()
        message=msg.decode()



        if "waktu" in strtopic:
            self.waktu=message
        elif self.client+"add" in strtopic:
            self.c.publish(self.clients+b"lampu",b"[lampu,on,off]")


        elif self.client+"nyala_pada_1" in strtopic:
            self.nyala_pada_1=message
        elif self.client+"nyala_pada_2" in strtopic:
            self.nyala_pada_2=message
        elif self.client+"nyala_pada_3" in strtopic:
            self.nyala_pada_3=message
        elif self.client+"nyala_pada_4" in strtopic:
            self.nyala_pada_4=message
        elif self.client+"mati_pada_1" in strtopic:
            self.mati_pada_1=message
        elif self.client+"mati_pada_2" in strtopic:
            self.mati_pada_2=message
        elif self.client+"mati_pada_3" in strtopic:
            self.mati_pada_3=message
        elif self.client+"mati_pada_4" in strtopic:
            self.mati_pada_4=message
        elif self.waktu==self.nyala_pada_1:
            self.led.value(0)
        elif self.waktu==self.nyala_pada_2:
            self.led.value(0)
        elif self.waktu==self.nyala_pada_3:
            self.led.value(0)
        elif self.waktu==self.nyala_pada_4:
            self.led.value(0)
        elif self.waktu==self.mati_pada_1:
            self.led.value(1)
        elif self.waktu==self.mati_pada_2:
            self.led.value(1)
        elif self.waktu==self.mati_pada_3:
            self.led.value(1)
        elif self.waktu==self.mati_pada_4:
            self.led.value(1)

        
        
        
    
        elif msg == b"on":
            self.led.value(0)
            # self.c.publish(self.client,b"saya client")
        elif msg == b"off":
            self.led.value(1)
        print(self.waktu)
        print(self.client)
        print(self.nyala_pada_1)
    def tim(self,dt):
        print(station.isconnected())
        if self.state=="terputus":
            self.start_mqtt()
        else:
            self.timer.deinit()
Wifi()
