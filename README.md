# Piña Colada ![Build Status](https://travis-ci.org/ecthros/pina-colada.svg?branch=master)

Piña Colada, a powerful and extensible wireless drop box, capable of performing a wide range of remote offensive attacks on a network. It can be controlled via it's command line interface, or connect to it's Command and Control remote server to be controlled remotely, either by web application or Android app.

Please only use Piña Colada with explicit permission - please don't hack without asking.

[Watch some controlled attacks here.](https://www.youtube.com/playlist?list=PL22Ei9kfayhao0qeotVvlkRtfSRSMGoLq)

## General Usage
Piña Colada comes with a number of built-in capabilities, and more can be dynamically added at any time. "Capabilities" are simply modules written to accomplish a task, such as a ARP Spoofing, DNS Poisoning, DOSing a user, etc. Piña Colada can be controlled using a familiar Metasploit like interface ("use" engages a capability, option setting works the same, etc), and is both quick to deploy and easy to use. 

To start Piña Colada, first ensure that you have the required dependencies. [Scapy](http://www.secdev.org/projects/scapy/) is the backbone of the project, so make sure you install it before running. More dependencies may be added as the project is extended, so make sure your installation remains up to date as it's updated. An automatic deployment package is coming soon. 

Launching Piña Colada:
```
$ sudo python cli.py
    ____  _  /\//          ______      __          __        ' .
   / __ \(_)//\/ ____ _   / ____/___  / /___ _____/ /___ _   \~~~/
  / /_/ / / __ \/ __ `/  / /   / __ \/ / __ `/ __  / __ `/    \_/
 / ____/ / / / / /_/ /  / /___/ /_/ / / /_/ / /_/ / /_/ /      Y
/_/   /_/_/ /_/\__,_/   \____/\____/_/\__,_/\__,_/\__,_/      _|_
Welcome to Pina Colada, a powerful Wifi Drop Box. Type "help" to see the list of available commands.
>>
```

## Controlling the Pi (CLI)

Piña Colada has a number of commands that enable to you to control different aspects about the pi and the network. 

**Enabling/disabling Promiscuous Mode:**
```
>> promisc enable
+ Promiscuous Mode enabled for interface eth0.
```

**Controlling operating interface:**
```
>> interface eth0
 + Successfully changed interface to eth0. Using local IP 10.0.0.56.
```

**Enumerating the Network:**
```
>> discover
Begin emission:
Finished to send 256 packets.

Received 0 packets, got 0 answers, remaining 256 packets
ID	IP		MAC			Ports	Last Date
61	10.0.0.1	00:0c:29:5f:e7:50		2016-11-01 15:34:40
62	10.0.0.32	d0:50:99:86:92:1a		2016-11-01 03:23:21
63	10.0.0.34	80:2a:a8:80:b1:82		2016-11-01 15:34:40
...
>> 
```

**Executing Commands:**

Piña Colada also operates as a fall-through shell. For example:
```
>> netstat -plant
 + Executing "netstat -plant"
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      605/sshd
...
>> msfconsole
       =[ metasploit v4.12.32-dev                         ]
+ -- --=[ 1587 exploits - 905 auxiliary - 273 post        ]
+ -- --=[ 457 payloads - 39 encoders - 8 nops             ]
+ -- --=[ Free Metasploit Pro trial: http://r-7.co/trymsp ]

msf > quit
>> 
```

## Capabilities

Out of the box, Piña Colada comes with many, many capabilities, and more can be added dynamically at any time. These capabilities are organized into the following categories:

1. Denial of Service (DOS)
2. ARP
3. Sniffing
4. Exploitation
5. Scanning
6. Auxiliary Attacks

To see a full list of available capabilities, run "list": 

```
>> list
 + Available capabilities:
  + auxiliary
   - reverse_shell
  + dos
   - syn
   - land
   - [tcpkiller](https://github.com/Kkevsterrr/tcpkiller)
  + arp
   - arpSpoof
   - arpDos
  + sniff
   - sniffPack
  + exploitation
   - dnsSpoof2
   - ms08
   - dnsSpoof
  + scan
   - syn
   - nmapScan
   ...
>>
```

To engage a capability for use, simply use the command "use":

```
>> use dos/syn
(Syn Flood) >>
```

Once a capability has been loaded, you can view options using a familiar "show options", and set each option by simply running "set <OPTION> <VALUE>":
```
>> set port 12345 
 + port => 12345
```

#### Persistence

Once loaded, all capabilities are persistent within Piña Colada's interface. This allows for multiple capabilities to be engaged simultaneously, and seamlessly transition between them. 
```
>> use dos/syn
(Syn Flood) >> launch
 + Launching Syn Flood...
Type 'restore' when ready to stop the attack.
(Syn Flood) >> quit
>> use dos/land
(Land Attack) >> launch
 + Launching Land Attack
 Sent 2000 packets.
>> use dos/syn
(Syn Flood) >> restore
 + Restoring target...
```
Even as the land attack is engaged, the syn flood is still operating in the background.

#### Interface

Additionally, Piña Colada supports full autocomplete of all capabilities (including recursively through depth), so you can start typing the following: 
```
>> use rever<tab>
```
immediately autocompletes to: 
```
>> use auxiliary/reverse_shell
```

Making it easy and fast to load arbitrary capapbilities quickly. 

#### Extensibility

More capabilities can be added to Piña Colada at any time, even during runtime. A [template](https://github.com/ecthros/pina-colada/blob/master/capabilities/template.py) capability file is included in the capabilities folder for rapid development - simply copy the file and move it into one of the categories. It is automatically and dynamically available for use in the command line interface or web terminal, and can be deployed at any time. 

## Server Capability

Piña Colada also contains a Command and Control server functionality to allow it be controlled remotely. This drop box functionality is especially useful when Piña Colada is deployed on a Raspberry Pi. To deploy the server on a remote location, run the following:

```
$ python server.py
[*] Starting web sever...
[*] PinaColada startup successful - listening on 0.0.0.0:9999
[*] Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

The server is now listening for connections and it's web server is accessible. In order to use the functionality of the command and control server, the pi must be connected. On the pi, run: 

```
$ sudo python client.py
Initializing Network DB...
[*] Attempting to connect to server
[*] Successfully connected.
```

The server will also acknoledge a succesful connection: 
```
[*] Pina Colada has connected.
```

The web server runs on port 5000, so going to the IP address of the server <IP>:5000 gives you a drop web terminal into the pi. This works by tunneling commands to the client into the command line interface. The CnC server also allows for the android app to connect to the pi for control. All of this communication is encrypted to prevent from eavesdropping or MITM attacks against the pi. 

### Encryption

All communication to and from the pi are encrypted using AES/CBC/PKCS#5 encryption. Keys are negotiated via the Diffie-Hellman protocol upon connection to the pi. All tunneling through the CnC server is also encrypted for protection and prevention of a MITM attack. 

## Contributing
Piña Colada is still very much in its infancy! Feel free to contribute to the project - simply fork it, make your changes, and issue a pull request. Have an idea for a killer capability, or something we could improve? Make an issue and we'll add it ASAP!

If you wish to add your own capability, follow the directions given in the pina-colada/capabilities/template.py file.
