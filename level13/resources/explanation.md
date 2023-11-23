in level13, we are back to having a good old binary file that we likely will have to exploit in some way

```bash
level13@SnowCrash:~$ ./level13 
UID 2013 started us but we we expect 4242
```

the issue is that the program is expecting another user ID to launch the process (most likely the flag13 user). After inspection of the /etc/passwd file, the id of flag13 is 3013 so it is another user that doesn't exist

```bash
level13@SnowCrash:~$ strings -d level13 
/lib/ld-linux.so.2
__gmon_start__
libc.so.6
_IO_stdin_used
exit
strdup
printf
getuid
__libc_start_main
GLIBC_2.0
PTRh`
UWVS
[^_]
0123456
UID %d started us but we we expect %d
boe]!ai0FB@.:|L6l@A?>qJ}I
your token is %s
;*2$"$
```

when looking at strings -d, it seems that the program will display the token only if it is launched by the right user. We also notice a strange line 'boe]!ai0FB@.:|L6l@A?>qJ}I'

if we look at the program with gdb :
```bash
(gdb) break main
Breakpoint 1 at 0x804858f
(gdb) run
Starting program: /home/user/level13/level13 

Breakpoint 1, 0x0804858f in main ()
(gdb) disassemble
Dump of assembler code for function main:
   0x0804858c <+0>:	push   %ebp
   0x0804858d <+1>:	mov    %esp,%ebp
=> 0x0804858f <+3>:	and    $0xfffffff0,%esp
   0x08048592 <+6>:	sub    $0x10,%esp
   0x08048595 <+9>:	call   0x8048380 <getuid@plt>
   0x0804859a <+14>:	cmp    $0x1092,%eax
   0x0804859f <+19>:	je     0x80485cb <main+63>
   0x080485a1 <+21>:	call   0x8048380 <getuid@plt>
   0x080485a6 <+26>:	mov    $0x80486c8,%edx
   0x080485ab <+31>:	movl   $0x1092,0x8(%esp)
   0x080485b3 <+39>:	mov    %eax,0x4(%esp)
   0x080485b7 <+43>:	mov    %edx,(%esp)
   0x080485ba <+46>:	call   0x8048360 <printf@plt>
   0x080485bf <+51>:	movl   $0x1,(%esp)
   0x080485c6 <+58>:	call   0x80483a0 <exit@plt>
   0x080485cb <+63>:	movl   $0x80486ef,(%esp)
   0x080485d2 <+70>:	call   0x8048474 <ft_des>
   0x080485d7 <+75>:	mov    $0x8048709,%edx
   0x080485dc <+80>:	mov    %eax,0x4(%esp)
   0x080485e0 <+84>:	mov    %edx,(%esp)
   0x080485e3 <+87>:	call   0x8048360 <printf@plt>
   0x080485e8 <+92>:	leave  
   0x080485e9 <+93>:	ret    
End of assembler dump.
```

we see that the function will call getuid, then compare the result in eax to 0x1092 which is 4242 in hexadecimal
If the comparison it equals, it will jump to 0x080485cb, where it will call the ft_des function and then later print the token. The only issue is that the comparison needs to be equal while the getuid will return 2013.
For this we can just go to the instruction at 0x0804859a (for instance with ni operations) and modify the value of the eax register with:

```bash
set $eax = 0x1092
```
We then can just continue the program execution with ni, and at the end, it will print the token

```bash
your token is 2A31L79asukciNyi8uppkEuSx
```
