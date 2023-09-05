from machine import Pin,SPI,PWM,Timer, Pin, ADC
from ST7735 import LCD_0inch96
import framebuf
import utime
import math

adc = ADC(Pin(26,mode=Pin.IN))

#color is BGR
RED = 0x00F8
GREEN = 0xE007
BLUE = 0x1F00
WHITE = 0xFFFF
BLACK = 0x0000

lcd = LCD_0inch96()   #Initializing the screen
lcd.fill(BLACK)       #clearing any exsiting diplay

# Configuration et acquisition des données
def get_pulse_rate():
    data = []
    time = []
    start_time = utime.ticks_ms()
    while utime.ticks_diff(utime.ticks_ms(), start_time) < 10000:  # Acquisition des données pendant 10 secondes
        data.append(adc.read_u16())
        time.append(utime.ticks_ms())
        utime.sleep_ms(10)
    
    # Détection des picss
    peaks = []
    threshold=(min(data)+max(data)*5)//6
    for i in range(1, len(data)-1):
        if data[i] > data[i-1] and data[i] > data[i+1] and data[i] > threshold:
            peaks.append(time[i])
    
    # Calcul du rythme cardiaque
    interval_sum = sum(utime.ticks_diff(peaks[i], peaks[i - 1]) for i in range(1, len(peaks)))
    if len(peaks)>1:
        average_interval = interval_sum / (len(peaks) - 1)
        pulse_rate = math.ceil(60 / (average_interval / 1000))  # Conversion en secondes
    
        return pulse_rate
while True:
    pulse_rate = get_pulse_rate()
    print("Rythme cardiaque :", pulse_rate, "bpm")
    lcd.fill(BLACK)
    string = "BPM : " + str(pulse_rate)
    lcd.text(string,55,15,RED)
    lcd.display()
