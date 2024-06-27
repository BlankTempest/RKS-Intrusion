# RKS-Intrusion
Remote Keying System Simulation and Intrusion

### Introduction
Remote Keying System (RKS) is an electronic lock that controls access to a building or vehicle by using an electronic remote control such as garage doors and vehicle doors. Widely used in automobiles, an RKS performs the functions of a standard car key without physical contact.

Before you start,
Install tkinter and pillow using pip.

![image](https://github.com/BlankTempest/RKS-Intrusion/assets/61834898/d6fcf6c5-7084-43ea-8f12-b3d974c5b412)


In this project, we simulate different types of RKS implementations.

### 1. Fixed Code 

Implementation: In a fixed code system, the transmitter and receiver use a pre-programmed code that remains the same every time the remote is used. The code is typically hardcoded into both the transmitter (key fob) and the receiver (car). When the button on the remote is pressed, the transmitter sends the fixed code to the receiver, which then validates it. If the code matches, the receiver performs the desired action (e.g., unlocking the door). 

Vulnerability: Fixed code systems are highly vulnerable to replay attacks. Since the code remains constant, an attacker can easily intercept and record the transmitted code. They can then replay this code to gain unauthorized access to the vehicle. They are also vulnerable to brute force attacks where different permutations of the key can be applied to gain access to the car.

Simulation: We simulate a fixed code system by creating a simple program that sends and receives fixed codes between a transmitter and a receiver. We demonstrate how an attacker can intercept and replay the fixed code to unlock the door.
To break fixed code systems, we can brute force different permutations and feed them in intervals.

Demonstration:

Step 1) Run relay.py, car_fixed.py, programmed_fob.py using python

Step 2) Look at the programmed_fob.py window. This is hardcoded with the key. Click on the image of the fob to transmit the signals. The car should change from locked to unlocked upon transmission of the key.

Step 3) Close programmed_fob.py and run fixed_fob.py using python. Input the key “00110011” into the text box and click on the image of the fob to transmit the signals. The car should change from locked to unlocked upon transmission of the key.

Step 4) Copy the 8-bit permutation string from List.txt that is padded with spaces. Paste the string into the text box. Click on the image of the fob to transmit the signals. The brute force attempt should start and the state of the car will change.


### 2. Shift Register

Implementation: In a shift register system, the code is not discarded after its attempt at validation. Instead it chucks the first bit and attempts to validate the next 8 bits. This algorithm typically involves shifting the bits of the input.

Vulnerability: Shift register systems are much easier to brute force since the permutations can be fed in without any breaks. With the use of de-bruijn sequences, the input permutation strings can be reduced to be much smaller.

Simulation: We simulate a shift register system by creating a program that implements a simple shift register algorithm. We demonstrate how an attacker can use de-bruijn sequences to unlock the door.

A de Bruijn sequence of order n on a size-k alphabet A is a cyclic sequence in which every possible length-n string on A occurs exactly once as a substring

Demonstration: 

Step 1) Run relay.py, fob.py and car_sr.py using python. 

Step 2)  Input the key “00110011” into the text box and click on the image of the fob to transmit the signals. The car should change from locked to unlocked upon transmission of the key.

Step 3) Copy the 8-bit de bruijn sequence from List.txt. Paste the string into the text box. Click on the image of the fob to transmit the signals. The brute force attempt should start and the state of the car will change.


### 3. Rolling Code

Implementation: In a rolling code system, also known as hopping code or hopping encryption, each time the remote is used, both the transmitter and the receiver generate a new code based on a pseudo random number generation algorithm. The code "rolls" or changes with each use, making it extremely difficult for attackers to predict or intercept the next code . The receiver stores a list of valid codes and accepts the next expected code in the sequence. This works by having the same seeded PRNG algorithm in both the transmitter and the receiver.

Vulnerability: While rolling code systems are highly secure, they are still susceptible to attacks such as jamming. Jamming attacks involve disrupting the communication between the transmitter and receiver, preventing the valid code from being received. This intercepted code is relayed back and since the code is still in the window, it will allow access.

Simulation: We simulate a rolling code system by creating a program that implements a PRNG algorithm(Mersenne twister) to generate and validate rolling codes. We demonstrate the robust security of rolling codes compared to fixed code and shift register systems and its fall to a jamming attack.

Demonstration:

Step 1) Run car_rc.py, relay.py and fob_rc.py using python.

Step 2) Click on the image in the fob_rc tkinter window to change the state of the car.

Step 3) Feed Ctrl+C into relay.py window. Press on the fob window once. The relay.py should terminate.

Step 4) Launch jammer.py. Click on the fob_rc window to send the transmission. The key will be intercepted by the jammer. Copy the intercepted key.

Step 5) Feed Ctrl+C into the jammer.py. Press once on the image in the fob window. The jammer.py will terminate. 

Step 6)Run relay.py using python. Close fob_rc.py and start fob.py using python. Paste the key into the text box and click on the image to send the transmission. The state of the car will change once for the transmission sent. With this, you have replayed the code successfully.


### Extra. Shift Register with GUI for the Jammer

Step 1)
Run the following files (each in a new terminal)
car_lock_unlock_gui.py
relayjammer.py
fob_g.py

Step 2)
In the fob gui, enter the key 00110011

Step 3)
With the jammer as inactive, we can lock and unlock the car by clicking on the lock icon on the fob gui 
