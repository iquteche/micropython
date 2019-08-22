<h1>ESP_32 Micropython</h1>
- go to this page http://micropython.org/download <br>
- download firmware esp32spiram-20190125-v1.10.bin <br>
- esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32--bluetooth.bin
