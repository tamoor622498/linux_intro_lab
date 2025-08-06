import subprocess
import time

LEDS = 0x41200000
SWO = 0x41200008
RGB0 = 0x41210000
RGB1 = 0x41210008

R = 0b001
G = 0b010
B = 0b100

#Read at addr and return as int
def readMem(addr=0x41200008):
    result = subprocess.run(f"devmem {hex(addr)} w", shell=True, capture_output=True, text=True)
    return int(result.stdout.strip(), 0)

def writeMem(addr=0x41200000, val=0):
    result = subprocess.run(f"devmem {hex(addr)} w {hex(val)}", shell=True, capture_output=True, text=True)

#Bits to array
def int_to_bit_array(value, width=4):
    return list(reversed([(value >> i) & 1 for i in range(width)]))

def main():
    ledVal = 0b0000
    while True:
        if (ledVal == 0b1111):
            ledVal = 0b0000
        else:
            ledVal+=1
        
        writeMem(LEDS, ledVal)
        
        switches = readMem()
        
        if (switches == 0b000):
            writeMem(RGB0, 0)
            writeMem(RGB1, 0)
        
        if (switches == 0b001):
            writeMem(RGB0, R)
            writeMem(RGB1, R)
        
        if(switches == 0b010):
            writeMem(RGB0, G)
            writeMem(RGB1, G)
            
        if(switches == 0b100):
            writeMem(RGB0, B)
            writeMem(RGB1, B)
        
        if(switches == 0b011):
            writeMem(RGB0, R+G)
            writeMem(RGB1, R+G)
            
        if(switches == 0b101):
            writeMem(RGB0, R+B)
            writeMem(RGB1, R+B)
            
        if(switches == 0b110):
            writeMem(RGB0, R+G)
            writeMem(RGB1, R+G)
            
        if(switches == 0b111):
            writeMem(RGB0, R+B+G)
            writeMem(RGB1, R+B+G)
        
        time.sleep(0.5)
    
if __name__=="__main__":
    main()