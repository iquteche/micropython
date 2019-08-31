<h1> burn esp8266 firmware</h1><br>
-esptool.py --chip esp8266 erase_flash<br>
-esptool.py --chip esp8266 --port <serial_port> write_flash --flash_mode dio --flash_size detect 0x0 <esp8266-X.bin><br>
<br>
<h1> burn esp32 firmware</h1><br>
-esptool.py --chip esp8266 erase_flash<br>
-esptool.py --chip esp32 --port <serial_port> write_flash -z 0x1000 <esp32-X.bin><br>
