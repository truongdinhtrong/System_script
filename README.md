# install python 3.6:

yum install gcc bzip2-devel libffi-devel openssl-devel 

./configure --enable-optimizations 
 
# make altinstall is used to prevent replacing the default python binary file /usr/bin/python

make altinstall 

# install pandas:

pip3.6 install MySQL-connector-python numpy mysql-connector psutil xlsxwriter 

# Config log iptables:
vi /etc/rsyslog.d/iptables.conf
kern.warning    /logs/iptables/iptables.log
:msg,contains,"[netfilter] " /logs/iptables/iptables.log

# Add rule iptables connlimit:
-A INPUT -i em2 -p tcp --syn -m state --state NEW -m connlimit --connlimit-above 15 -m multiport --dports 80,443 -j LOG --log-level 5 --log-prefix "[netfilter] CONLIMIT_15: "

