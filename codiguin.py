import json
import spidev
import time

#definição dos pinos do raspberry (não necessário por enquanto)
fifoptraddr = 0x00
fifotxbaseaddr = 0x80
Lora = spidev.SpiDev()
Lora.open(0,0)
while True:
    Lora.spi.xfer2(fifoptraddr & 0x7F, fifotxbaseaddr)
    dados = {
        "nome": "Joao",
        "idade": 30,
        "cidade": "Sao Paulo"
    }
    dados2 = json.dumps(dados)
    payload = bytes(dados2, 'utf-8')
    Lora.xfer2(payload)