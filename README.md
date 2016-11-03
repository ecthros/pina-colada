# Piña Colada ![Build Status](https://travis-ci.org/ecthros/pina-colada.svg?branch=master)

Piña Colada, a powerful and extensible wireless pineapple, capable of performing a wide range of remote offensive attacks on a network. It can currently be controlled only via a command line interface, but a Command and Control remote server functionality is coming soon. An Android app will allow you to control the Piña Colada via the Command and Control server (Under Construction).

Please only use Piña Colada with explicit permission - please don't hack without asking.

## Usage
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
Welcome to Pina Colada, a powerful Wifi Pinapple. Type "help" to see the list of available commands.
>>
```

## Capabilities

Out of the box, Piña Colada comes with many, many capabilities, and more can be added at any time. These capabilities are organized into categories. Currently, the following attacks are supported: 

1. Packet Sniffing - Passively sniffs the network and logs all traffic recorded
2. Scanning - standard scanning types are implemented, and Piña Colada often out performs nmap for the same scan type
3. TCP Hangups (from [tcpkiller](https://github.com/Kkevsterrr/tcpkiller))
4. ARP Spoofing and Man In The Middle Attacks
5. MS08 Exploitation
6. Many, many, many more coming soon!

To see a full list of available capabilities, run "list": 

```
>> list
 + Available capabilities:
  + dos
   - land
   - syn
   - tcpkiller
  + arp
   - arpDos
   - arpSpoof
  + sniff
   - sniffPack
  + exploitation
   - dnsSpoof
   - ms08
  + scan
   - nmapScan
   - syn
   ...
>>
```

To engage a capability for use, simply use the command "use":

```
>> use dos/syn
(Syn Scan) >>
```

Once a capability has been loaded, you can view options using a familiar "show options", and set each option by simply running "set <OPTION> <VALUE>":
```
>> set port 12345 
 + port => 12345
```

## Contributing
Piña Colada is still very much in its infancy! Feel free to contribute to the project - simply fork it, make your changes, and issue a pull request. Have an idea for a killer capability, or something we could improve? Make an issue and we'll add it ASAP!

If you wish to add your own capability, follow the directions given in the pina-colada/capabilities/template.py file.
