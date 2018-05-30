# But : trouver un port aléatoire disponible afin de modifier le port par défaut de postgres (5432)

## Lister les ports utilisés et le service associé

`sudo netstat -natup | sed -nr 's#^[^:]*:([[:digit:]]+)[^/]*/(.+)$#\1 \2#p'`

>	139 smbd
>	54321 postgres
>	53 dnsmasq
>	22 sshd
>	445 smbd
>	43406 firefox
>	49340 firefox
>	139 smbd
>	37672 firefox
>	39316 firefox
>	49274 firefox
>	49342 firefox
>	48824 firefox
>	35032 firefox
>	56121 dnsmasq
>	5353 avahi-daemon: r
>	50445 postgres
>	42408 avahi-daemon: r
>	53 dnsmasq
>	68 dhclient
>	137 nmbd
>	137 nmbd
>	137 nmbd
>	138 nmbd
>	138 nmbd
>	138 nmbd
>	631 cups-browsed

## Simulation d'un scan externe des ports (qui pourrait être malicieux !)

`sudo nmap -T4 127.0.0.1 -p 5432,54321`

Ici 54321 est le port par défaut pour postgres et 54321 le port (arbitrairement choisi) sur lequel il est réellement lancé.
5432 est un un port standard. Il fait partie des "well-know ports". On peut les trouver dans `/etc/services`. Le découpage est décrit dans la [RFC 6335, section _"6.  Port Number Ranges"_](https://www.rfc-editor.org/rfc/rfc6335.txt)). `nmap` donne donc "postgres".
Cependant `nmap` constate que le port 54321 est ouvert mais ne parvient pas à déterminer le service derrière celui-ci .

>	Starting Nmap 7.01 ( https://nmap.org ) at 2017-04-12 14:12 CEST
>	Nmap scan report for localhost (127.0.0.1)
>	Host is up (0.000052s latency).
>	PORT      STATE  SERVICE
>	5432/tcp  closed postgresql
>	54321/tcp open   unknown
>
>	Nmap done: 1 IP address (1 host up) scanned in 0.28 seconds

## Tableau comparatif : Y a-t-il un intérêt à changer le port par défaut de postgres ?

Pour | Contre
-|-
cf ci-dessus : rend d'éventuelles intrusions plus difficiles | la base n'est pas destinée à un usage public, une sécurité "forte" n'est donc pas nécessaire
| | les données manipulées n'ont pas un aspect sensible particulier
| | les configurations par défaut des programmes en interaction avec postgres sont à modifier

Modifier le port par défaut présente un trop faible intérêt comparé à l'apport en sécurité. Ce n'est pas un système manipulant des données sensibles, et un changement de port requiert de modifier les configurations par défaut des outils amenés se connecter à la base. Enfin, étant un "well-know port", si postgres n'est pas déjà installé, par convention ce port ne court pas le risque d'être déjà utilisé par un quelconque autre service.

**Décision prise :** Conservation du port **5432** (non modifié).
