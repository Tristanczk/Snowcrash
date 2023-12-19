In level09, we also have an executable level09 and a token file
This time, we can read the token file, but the content contains non displayable characters

```bash
level09@SnowCrash:~$ cat token
f4kmm6p|=�p�n��DB�Du{��
```

and when we execute the program level09

```bash
level09@SnowCrash:~$ ./level09
You need to provied only one arg.
level09@SnowCrash:~$ ./level09 token
tpmhr
```
note, when we use token, it doesn't get the content of the file but rather the word token as if we do this
```bash
level09@SnowCrash:~$ ./level09 /home/user/level09/token
/iqpi4{zm{9wq�s{@JA���{�
```
we don't have the same result

when looking at the program with `strings -d level09`, we have the following text

```
You should not reverse this
LD_PRELOAD
Injection Linked lib detected exit..
/etc/ld.so.preload
/proc/self/maps
/proc/self/maps is unaccessible, probably a LD_PRELOAD attempt exit..
libc
You need to provied only one arg.
00000000 00:00 0
LD_PRELOAD detected through memory maps exit ..
```

which might correspond to some protection against custom code injection

and when looking at `nm level09`, we see a function called isLib which might check if the function corresponds to the actual library function.
As LD_PRELOAD is an environment variable used to specify a list of additional libraries  that should be loaded before all other libraries when a program is executed,
allowing to override functions with your own custom functions

We also see a function called afterSubstr which might return the text after a given subchain

It seems that the token file contains the password after going through the program, so we need to identify what the program is doing in order to revert it

Doing some test with the program

```bash
level09@SnowCrash:~$ ./level09 ca
cb
level09@SnowCrash:~$ ./level09 cba
ccc
level09@SnowCrash:~$ ./level09 cbaz
ccc}
level09@SnowCrash:~$ ./level09 dcba
dddd
level09@SnowCrash:~$ ./level09 edcba
eeeee
```

we can see that most likely, it just display the current character + i (i being the charather position in the string)
We can copy the token file into our machine, then, using a simple python script to decode it, we get the following password: f3iji1ju5yuevaus41q1afiuq
It works, we can now log into the flag09 user and get the flag.
And with that ends the mandatory part
