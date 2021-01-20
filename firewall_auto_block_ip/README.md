# Config log iptables:
vi /etc/rsyslog.d/iptables.conf
kern.warning    /logs/iptables/iptables.log
:msg,contains,"[netfilter] " /logs/iptables/iptables.log

systemctl restart rsyslog

# Add rule iptables connlimit:
iptables -A INPUT -i em2 -p tcp --syn -m state --state NEW -m connlimit --connlimit-above 15 -m multiport --dports 80,443 -j LOG --log-level 5 --log-prefix "[netfilter] CONLIMIT_15: "
