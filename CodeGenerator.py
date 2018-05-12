arduinoCode = []
variables = {}
wheels = []
animations = []


def createVariable(command):
    variables[command[1]] = command[2]
    print("New variable name: " + command[1])
    print("Variable value: " + variables[command[1]])
    print("Current variables:")
    print(variables)


def animate(command):
    # Step 1: Default code
    createInitialCode()

    # Step 2: Check for variables
    animation = ""
    color = ""
    colorRGB = ()
    time = 0

    # a) Animation
    if command[1] not in variables:
        animation = command[1]
    else:
        animation = variables[command[1]]

    # b) Color
    if command[2] not in variables:
        if isinstance(command[2], tuple):
            colorRGB = command[2]
        else:
            color = command[2]
    elif isinstance(variables[command[2]], tuple):
        colorRGB = variables[command[2]]
    else:
        color = variables[command[2]]

    # c) Time
    if command[3] not in variables:
        time = command[3]
    else:
        time = variables[command[3]]

    print("Animation: " + animation)
    print("Color: " + color)
    print("ColorRGB: ")
    print(colorRGB)
    print("Time: ")
    print(time)

    # Step 3: Animation code
    if animation == "RAINBOW":
        createRainbowAnimation(colorRGB, time)
    elif animation == "RAINBOW_CYCLE":
        createRainbowCycleAnimation(colorRGB, time)
    elif animation == "THEATER_CHASE_RAINBOW":
        createTheaterChaseRainbowAnimation(colorRGB, time)
    elif animation == "COLOR_WIPE":
        colorRGB = returnRGB(color)
        print("The RGB is: ")
        print(colorRGB)
        createColorWipeAnimation(colorRGB, time)
    elif animation == "THEATER_CHASE":
        colorRGB = returnRGB(color)
        # print("The RGB is: ")
        # print(colorRGB)
        createColorWipeAnimation(colorRGB, time)


# Pass rgb tuple for wheel creation and time delay
#Missing definition code
def createRainbowAnimation(colorRGB, time):
    createColorWheel(colorRGB)
    arduinoLine = "rainbow(" + time + ")\n"
    animations.append(arduinoLine)

#Missing definition code
def createRainbowCycleAnimation(colorRGB, time):
    createColorWheel(colorRGB)
    arduinoLine = "rainbowCycle(" + time + ")\n"
    animations.append(arduinoLine)

#Missing definition code
def createTheaterChaseRainbowAnimation(colorRGB, time):
    createColorWheel(colorRGB)
    arduinoLine = "theaterChaseRainbow(" + time + ")\n"
    animations.append(arduinoLine)


# Pass color to be used and time delay
def createColorWipeAnimation(colorRGB, time):
    arduinoLine = "colorWipe(" + colorRGB + ", " + time + ")\n"
    animations.append(arduinoLine)


def createTheaterChaseAnimation(colorRGB, time):
    arduinoLine = "theaterChase(" + colorRGB + ", " + time + ")\n"
    animations.append(arduinoLine)


#Work in progress
def createColorWheel(colorRGB):
    arduinoBlock = "uint32_t Wheel(byte WheelPos) {\n" \
                   "   WheelPos = 255 - WheelPos;\n" \
                   "   if (WheelPos < 85)\n" \
                   "       {\n" \
                   "       return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);\n" \
                   "       }" \
                   "   if (WheelPos < 170) {\n" \
                   "       WheelPos -= 85;\n" \
                   "       return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);\n" \
                   "   }\n" \
                   "   WheelPos -= 170;\n" \
                   "   return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);\n" \
                   "}"
    wheels.append(arduinoBlock)


def returnRGB(color):
    if color == 'RED':
        return (255, 0, 0)
    if color == 'BLUE':
        return (0, 0, 255)
    if color == 'GREEN':
        return (0, 255, 0)
    if color == 'YELLOW':
        return (255, 255, 0)
    if color == 'ORANGE':
        return (255, 165, 0)
    if color == 'PURPLE':
        return (128, 0, 128)
    if color == 'WHITE':
        return (255, 255, 255)


# Generates the default Arduino code
def createInitialCode():
    defaultCode = "#include <Adafruit_NeoPixel.h> \n" \
                  "#ifdef __AVR__ \n" \
                  "  #include <avr/power.h> \n" \
                  "#endif \n" \
                  " \n" \
                  "#define PIN 6 \n" \
                  "    \n" \
                  "Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_GRB + NEO_KHZ800); \n" \
                  "   \n" \
                  "void setup() { \n" \
                  "  #if defined (__AVR_ATtiny85__) \n" \
                  "    if (F_CPU == 16000000) clock_prescale_set(clock_div_1); \n" \
                  "  #endif \n" \
                  "  // End of trinket special code \n" \
                  "\n" \
                  "  strip.begin(); \n" \
                  "  strip.show(); // Initialize all pixels to 'off' \n" \
                  "} \n" \
                  "\n" \
                  "// Fill the dots one after the other with a color \n" \
                  "void colorWipe(uint32_t c, uint8_t wait) { \n" \
                  "  for(uint16_t i=0; i<strip.numPixels(); i++) { \n" \
                  "   strip.setPixelColor(i, c); \n" \
                  "    strip.show(); \n" \
                  "    delay(wait); \n" \
                  "  } \n" \
                  "} \n" \
                  "           \n" \
                  "void theaterChase(uint32_t c, uint8_t wait) { \n" \
                  "  for (int j=0; j<10; j++) {  //do 10 cycles of chasing \n" \
                  "    for (int q=0; q < 3; q++) { \n" \
                  "      for (uint16_t i=0; i < strip.numPixels(); i=i+3) { \n" \
                  "        strip.setPixelColor(i+q, c); \n" \
                  "      } \n" \
                  "      strip.show(); \n" \
                  "            \n" \
                  "      delay(wait); \n" \
                  "            \n" \
                  "      for (uint16_t i=0; i < strip.numPixels(); i=i+3) { \n" \
                  "        strip.setPixelColor(i+q, 0); \n" \
                  "     } \n" \
                  "    } \n" \
                  "  } \n" \
                  "}"
    arduinoCode.append(defaultCode)
    # filePath = "test.ino"
    # test = open(filePath, 'w')
    # test.write(defaultCode)
    # test.close()
