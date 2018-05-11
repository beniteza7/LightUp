#include <Adafruit_NeoPixel.h> 
#ifdef __AVR__ 
#include <avr/power.h> 
#endif 
#define PIN 6 Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_GRB + NEO_KHZ800); 
void setup() 
{ 
#if defined (__AVR_ATtiny85__) 
if (F_CPU == 16000000) clock_prescale_set(clock_div_1); 
#endif 
// End of trinket special code 
strip.begin(); 
strip.show(); 
// Initialize all pixels to 'off' 
} 
// Fill the dots one after the other with a color 
void colorWipe(uint32_t c, uint8_t wait) 
{ 
for(uint16_t i=0; i<strip.numPixels(); i++) { 
strip.setPixelColor(i, c); strip.show(); 
delay(wait); 
} 
} 
void rainbow(uint8_t wait) 
{ 
uint16_t i, j; 
for(j=0; j<256; j++) { 
for(i=0; i<strip.numPixels(); i++) { 
strip.setPixelColor(i, Wheel((i+j) & 255)); 
} 
strip.show(); 
delay(wait); 
} 
} 
void theaterChase(uint32_t c, uint8_t wait) 
{ 
for (int j=0; j<10; j++) { 
//do 10 cycles of chasing 
for (int q=0; q < 3; q++) { 
for (uint16_t i=0; i < strip.numPixels(); i=i+3) { 
strip.setPixelColor(i+q, c); 
} 
strip.show(); 
delay(wait); 
for (uint16_t i=0; i < strip.numPixels(); i=i+3) { 
strip.setPixelColor(i+q, 0); 
} 
} 
} 
}