import spidev
import time

# SPI configuration
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000

# LoRa parameters
FREQUENCY = 915e6  # Set your frequency here
SPREADING_FACTOR = 7  # Spreading factor (7 to 12)
TX_POWER = 14  # Power level from 2 to 20

# Message to send
message = "Hello, LoRa!"

# LoRa register addresses
REG_FIFO = 0x00
REG_OP_MODE = 0x01
REG_FR_MSB = 0x06
REG_FR_MID = 0x07
REG_FR_LSB = 0x08
REG_PA_CONFIG = 0x09
REG_FIFO_TX_BASE_ADDR = 0x0E
REG_FIFO_ADDR_PTR = 0x0D
REG_PAYLOAD_LENGTH = 0x22
REG_IRQ_FLAGS = 0x12
REG_MODEM_CONFIG1 = 0x1D
REG_MODEM_CONFIG2 = 0x1E

# Initialize LoRa module
def lora_reset():
    pass  # Implement your reset logic here

def set_mode(mode):
    spi.xfer2([REG_OP_MODE | 0x80, mode])

def write_register(address, value):
    spi.xfer2([address | 0x80, value])

# Reset LoRa module
lora_reset()
time.sleep(0.01)

# Configure LoRa module
set_mode(0x81)  # Sleep mode
write_register(REG_PA_CONFIG, 0x8F)  # Set power output to maximum
write_register(REG_FR_MSB, int((FREQUENCY / 32e6) * 524288))  # Frequency setting
write_register(REG_FR_MID, int(((FREQUENCY & 0xFF) * 16777216) / 32e6))  # Frequency setting
write_register(REG_FR_LSB, int(((FREQUENCY & 0xFFFFFF) * 256) / 32e6))  # Frequency setting
write_register(REG_MODEM_CONFIG1, 0x72)  # Bandwidth and coding rate
write_register(REG_MODEM_CONFIG2, (SPREADING_FACTOR << 4) | 0x04)  # Spreading factor and CRC enabled
write_register(REG_OP_MODE, 0x81)  # Standby mode

# Send a message
set_mode(0x81)  # Standby mode
write_register(REG_FIFO_TX_BASE_ADDR, 0x00)  # Set FIFO pointer
write_register(REG_FIFO_ADDR_PTR, 0x00)  # Set FIFO pointer
for char in message:
    write_register(REG_FIFO, ord(char))  # Write data to FIFO
write_register(REG_PAYLOAD_LENGTH, len(message))  # Set payload length
set_mode(0x83)  # Transmit mode

# Wait for transmission to complete
while True:
    irq_flags = write_register(REG_IRQ_FLAGS, 0xFF)  # Read IRQ flags
    if (irq_flags & 0x08) != 0:  # TxDone flag
        break
    time.sleep(0.1)

# Close SPI connection
spi.close()