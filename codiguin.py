import json
import spidev
import time

#definição dos pinos do raspberry (não necessário por enquanto)
fifoptraddr = 0x00
fifotxbaseaddr = 0x80

#defina a função de setar a frequencia do Lora
def set_freq(self, f):
        i = int(f * 16384.)    # choose floor
        msb = i // 65536
        i -= msb * 65536
        mid = i // 256
        i -= mid * 256
        lsb = i
        return self.spi.xfer([REG.LORA.FR_MSB | 0x80, msb, mid, lsb])
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
Lora.xfer2([((0x01)& 0x7F | STDBY)])
Lora.xfer2([(fifoptraddr) & 0x7F | fifotxbaseaddr])
Lora.set_freq(915.0)
while True:
    #dados = {
    #    "nome": "Joao",
    #    "idade": 30,
    #    "cidade": "Sao Paulo"
    #}
    dados = "oi, esp32"
    dados2 = json.dumps(dados)
    payload = bytes(dados2, 'utf-8')
    payload_length = [len(payload)]
    Lora.xfer2(payload_length)
    Lora.xfer2(payload)
    Lora.xfer2([(0x01)&0x7F | 0x83])
    print("Enviando...\n")
    time.sleep(2)