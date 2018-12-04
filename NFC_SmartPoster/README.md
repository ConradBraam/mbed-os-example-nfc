# NFC SmartPoster controller stop issue repro steps

This is a defect sample repro. app

See original app for notes on compiling installing and running.
We used the following diagram: using the Raspbery Pi explorer (PN512) board, use this pinout mapping diagram to connect the shield to the reference target. In this case a ST NucleoF401RE pinout is shown.
```
          Nucleo F401RE                Explore NFC                 
         (Arduino header)        (pin1 on shield shown with a <|)
     +-------+     +-------+             +--------+                  
     | [NC]  |     | [B8]  |             |[ 2][ 1]|                  
     | [IOREF|     | [B9]  |             |[ 4][ 3]|                  
     | [RST] |     | [AVDD]|             |[ 6][ 5]|                  
1<---+ [3V3] |     | [GND] |             |[ 8][ 7]|                  
     | [5V]  |     | [A5]  +--->23       |[10][ 9]|                  
     | [GND] |     | [A6]  +--->21       |[12][11]|                  
25<--+ [GND] |     | [A7]  +--->19       |[14][13]|                  
     | [VIN] |     | [B6]  +--->3        |[16][15]|                  
     |       |     | [C7]  |             |[18][17]|                  
26<--+ [A0]  |     | [A9]  |             |[20][19]|                  
16<--+ [A1]  |     | [A9]  |             |[22][21]|                  
     | ...   |     |       |             |[24][23]|                  
     |       |     | [A8]  |             |[26][25]|                  
     +-------+     | ...   |             +--------+                  
                   |       |                               
                   |       |                               
                   +-------+                               
                                         
Patch using jumper wires to the             
indicated pins on the Shield.            

The user button is used to enable/disable discovery loop function - press to start discovery.

Requires an NFC reader and the nfcpy libraries on the computer. see original/official docs
Run the python test program and press 5 and enter, to poll for a tag (2 seconds.)