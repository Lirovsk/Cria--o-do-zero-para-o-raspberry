import time
import spidev
import json
import RPi.GPIO as GPIO
#definição das constanstes a sertem usadas
class LORA:
    FIFO               = 0x00
    OP_MODE            = 0x01
    FR_MSB             = 0x06
    FR_MID             = 0x07
    FR_LSB             = 0x08
    PA_CONFIG          = 0x09
    PA_RAMP            = 0x0A
    OCP                = 0x0B
    LNA                = 0x0C
    FIFO_ADDR_PTR      = 0x0D
    FIFO_TX_BASE_ADDR  = 0x0E
    FIFO_RX_BASE_ADDR  = 0x0F
    FIFO_RX_CURR_ADDR  = 0x10
    IRQ_FLAGS_MASK     = 0x11
    IRQ_FLAGS          = 0x12
    RX_NB_BYTES        = 0x13
    RX_HEADER_CNT_MSB  = 0x14
    RX_PACKET_CNT_MSB  = 0x16
    MODEM_STAT         = 0x18
    PKT_SNR_VALUE      = 0x19
    PKT_RSSI_VALUE     = 0x1A
    RSSI_VALUE         = 0x1B
    HOP_CHANNEL        = 0x1C
    MODEM_CONFIG_1     = 0x1D
    MODEM_CONFIG_2     = 0x1E
    SYMB_TIMEOUT_LSB   = 0x1F
    PREAMBLE_MSB       = 0x20
    PAYLOAD_LENGTH     = 0x22
    MAX_PAYLOAD_LENGTH = 0x23
    HOP_PERIOD         = 0x24
    FIFO_RX_BYTE_ADDR  = 0x25
    MODEM_CONFIG_3     = 0x26
    PPM_CORRECTION     = 0x27
    FEI_MSB            = 0x28
    DETECT_OPTIMIZE    = 0X31
    INVERT_IQ          = 0x33
    DETECTION_THRESH   = 0X37
    SYNC_WORD          = 0X39
    DIO_MAPPING_1      = 0x40
    DIO_MAPPING_2      = 0x41
    VERSION            = 0x42
    TCXO               = 0x4B
    PA_DAC             = 0x4D
    AGC_REF            = 0x61
    AGC_THRESH_1       = 0x62
    AGC_THRESH_2       = 0x63
    AGC_THRESH_3       = 0x64
    PLL                = 0x70
    
#Inicio do módulo spi
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 500000

#escrita do registro FIFO
spi.xfer2([LORA.FIFO_TX_BASE_ADDR | 0x80, 0x00])

#Tratamento da mensagem
dados = {
        "nome": "Joao",
        "idade": 30,
        "cidade": "Sao Paulo"
    }

dados2 = json.dumps(dados)
payload = bytes(dados2, 'utf-8')
payload_length = [len(payload)]

#Escrita do payload no FIFO
while True:
    spi.xfer2([LORA.FIFO_ADDR_PTR | 0x80, 0x00])
    spi.xfer2([LORA.PAYLOAD_LENGTH | 0x80, payload_length[0]])
    spi.xfer2([LORA.FIFO | 0x80, ] + payload)
    print("Mensagem enviada")