# install python 3.6:

yum install gcc bzip2-devel libffi-devel openssl-devel 

./configure --enable-optimizations 
 
# make altinstall is used to prevent replacing the default python binary file /usr/bin/python

make altinstall 

# install pandas:

pip3.6 install MySQL-connector-python numpy mysql-connector psutil xlsxwriter 


