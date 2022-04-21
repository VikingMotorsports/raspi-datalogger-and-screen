from smbus2 import SMBus, i2c_msg

with SMBus(1) as bus:
    # Read 64 bytes from address 0x69
    msg = i2c_msg.read(0x69, 2)
    bus.i2c_rdwr(msg)

    # Write a single byte to address 0x69
    msg = i2c_msg.write(0x69, "Poggers")
    bus.i2c_rdwr(msg)

