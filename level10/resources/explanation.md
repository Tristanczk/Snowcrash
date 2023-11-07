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