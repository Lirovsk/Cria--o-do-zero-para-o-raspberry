import json
import spidev
import time

#definição dos pinos do raspberry (não necessário por enquanto)
fifoptraddr = 0x00
fifotxbaseaddr = 0x80
#Constantes que representam o modo de operação
SLEEP    = 0x80
STDBY    = 0x81
FSTX     = 0x82
TX       = 0x83
FSRX     = 0x84
RXCONT   = 0x85
RXSINGLE = 0x86
CAD      = 0x87
FSK_STDBY= 0x01
Lora = spidev.SpiDev()
Lora.open(0,0)
Lora.xfer2(0x01 & 0x7F, STDBY)
Lora.xfer2(fifoptraddr & 0x7F, fifotxbaseaddr)
while True:
    dados = {
        "nome": "Joao",
        "idade": 30,
        "cidade": "Sao Paulo"
    }
    dados2 = json.dumps(dados)
    payload = bytes(dados2, 'utf-8')
    payload_length = len(payload)
    Lora.xfer2(payload_length)
    Lora.xfer2(payload)
    Lora.xfer2(0x01 & 0x7F, 0x83)