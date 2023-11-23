In level 14, we have no file available and when we check all files for the users level14 or flag14 with find / -user, we don't find anything.

Maybe we can exploit the very thing that allows us to get a flag, the getflag comment. The only weird thing is that it is something that we could have done for every other levels

when we look at strings :
```bash
level14@SnowCrash:~$ strings -d /bin/getflag
/lib/ld-linux.so.2
__gmon_start__
libc.so.6
_IO_stdin_used
__stack_chk_fail
strdup
stdout
fputc
fputs
getenv
stderr
getuid
ptrace
fwrite
open
__libc_start_main
GLIBC_2.4
GLIBC_2.0
PTRh@
QVhF
UWVS
[^_]
0123456
You should not reverse this
LD_PRELOAD
Injection Linked lib detected exit..
/etc/ld.so.preload
/proc/self/maps
/proc/self/maps is unaccessible, probably a LD_PRELOAD attempt exit..
libc
Check flag.Here is your token : 
You are root are you that dumb ?
I`fA>_88eEd:=`85h0D8HE>,D
7`4Ci4=^d=J,?>i;6,7d416,7
<>B16\AD<C6,G_<1>^7ci>l4B
B8b:6,3fj7:,;bh>D@>8i:6@D
?4d@:,C>8C60G>8:h:Gb4?l,A
G8H.6,=4k5J0<cd/D@>>B:>:4
H8B8h_20B4J43><8>\ED<;j@3
78H:J4<4<9i_I4k0J^5>B1j`9
bci`mC{)jxkn<"uD~6%g7FK`7
Dc6m~;}f8Cj#xFkel;#&ycfbK
74H9D^3ed7k05445J0E4e;Da4
70hCi,E44Df[A4B/J@3f<=:`D
8_Dw"4#?+3i]q&;p6 gtw88EC
boe]!ai0FB@.:|L6l@A?>qJ}I
g <t61:|4_|!@IF.-62FH&G~DCK/Ekrvvdwz?v|
Nope there is no token here for you sorry. Try again :)
00000000 00:00 0
LD_PRELOAD detected through memory maps exit ..
;*2$"$
```

we see numerous weird strings with especially one string that catches my eye : boe]!ai0FB@.:|L6l@A?>qJ}I, which is the same string that we saw in the level13 program.
The getflag command could just use the same ft_des function to get the token

```bash
level14@SnowCrash:~$ nm /bin/getflag
0804af28 d _DYNAMIC
0804aff4 d _GLOBAL_OFFSET_TABLE_
08048f9c R _IO_stdin_used
         w _Jv_RegisterClasses
0804af18 d __CTOR_END__
0804af14 d __CTOR_LIST__
0804af20 D __DTOR_END__
0804af1c d __DTOR_LIST__
080494a8 r __FRAME_END__
0804af24 d __JCR_END__
0804af24 d __JCR_LIST__
0804b03c A __bss_start
0804b030 D __data_start
08048f50 t __do_global_ctors_aux
08048580 t __do_global_dtors_aux
0804b034 D __dso_handle
         w __gmon_start__
08048f42 T __i686.get_pc_thunk.bx
0804af14 d __init_array_end
0804af14 d __init_array_start
08048f40 T __libc_csu_fini
08048ed0 T __libc_csu_init
         U __libc_start_main@@GLIBC_2.0
         U __stack_chk_fail@@GLIBC_2.4
0804b03c A _edata
0804b06c A _end
08048f7c T _fini
08048f98 R _fp_hw
08048444 T _init
08048550 T _start
080487be T afterSubstr
0804b064 b completed.6159
0804b030 W data_start
0804b068 b dtor_idx.6161
0804b038 d end.3187
         U fputc@@GLIBC_2.0
         U fputs@@GLIBC_2.0
080485e0 t frame_dummy
08048604 T ft_des
         U fwrite@@GLIBC_2.0
         U getenv@@GLIBC_2.0
         U getuid@@GLIBC_2.0
08048843 T isLib
08048946 T main
         U open@@GLIBC_2.0
         U ptrace@@GLIBC_2.0
         U puts@@GLIBC_2.0
0804b040 B stderr@@GLIBC_2.0
0804b060 B stdout@@GLIBC_2.0
         U strdup@@GLIBC_2.0
0804874c T syscall_gets
0804871c T syscall_open
```

and sure enough, ft_des is among the used function.
We have many options :
 - we could reuse the program of level13 by using gdb to pass the string for level14 which should be this one 'g <t61:|4_|!@IF.-62FH&G~DCK/Ekrvvdwz?v|'
 - or we could just understand how the getflag program checks that we are the right user and just bypass this check

when we look with gdb, we can see that the getflag program has the same logic :
```bash
0x08048afd <+439>:	call   0x80484b0 <getuid@plt>
   0x08048b02 <+444>:	mov    %eax,0x18(%esp)
   0x08048b06 <+448>:	mov    0x18(%esp),%eax
   0x08048b0a <+452>:	cmp    $0xbbe,%eax
   0x08048b0f <+457>:	je     0x8048ccb <main+901>
   0x08048b15 <+463>:	cmp    $0xbbe,%eax
   0x08048b1a <+468>:	ja     0x8048b68 <main+546>
   0x08048b1c <+470>:	cmp    $0xbba,%eax
   0x08048b21 <+475>:	je     0x8048c3b <main+757>
   0x08048b27 <+481>:	cmp    $0xbba,%eax
   0x08048b2c <+486>:	ja     0x8048b4d <main+519>
   0x08048b2e <+488>:	cmp    $0xbb8,%eax
   0x08048b33 <+493>:	je     0x8048bf3 <main+685>
   0x08048b39 <+499>:	cmp    $0xbb8,%eax
   0x08048b3e <+504>:	ja     0x8048c17 <main+721>
   0x08048b44 <+510>:	test   %eax,%eax
   0x08048b46 <+512>:	je     0x8048bc6 <main+640>
   0x08048b48 <+514>:	jmp    0x8048e06 <main+1216>
   0x08048b4d <+519>:	cmp    $0xbbc,%eax
   0x08048b52 <+524>:	je     0x8048c83 <main+829>
   0x08048b58 <+530>:	cmp    $0xbbc,%eax
   0x08048b5d <+535>:	ja     0x8048ca7 <main+865>
   0x08048b63 <+541>:	jmp    0x8048c5f <main+793>
   0x08048b68 <+546>:	cmp    $0xbc2,%eax
   0x08048b6d <+551>:	je     0x8048d5b <main+1045>
   0x08048b73 <+557>:	cmp    $0xbc2,%eax
   0x08048b78 <+562>:	ja     0x8048b95 <main+591>
   0x08048b7a <+564>:	cmp    $0xbc0,%eax
   0x08048b7f <+569>:	je     0x8048d13 <main+973>
   0x08048b85 <+575>:	cmp    $0xbc0,%eax
   0x08048b8a <+580>:	ja     0x8048d37 <main+1009>
   0x08048b90 <+586>:	jmp    0x8048cef <main+937>
   0x08048b95 <+591>:	cmp    $0xbc4,%eax
   0x08048b9a <+596>:	je     0x8048da3 <main+1117>
   0x08048ba0 <+602>:	cmp    $0xbc4,%eax
   0x08048ba5 <+607>:	jb     0x8048d7f <main+1081>
   0x08048bab <+613>:	cmp    $0xbc5,%eax
   0x08048bb0 <+618>:	je     0x8048dc4 <main+1150>
   0x08048bb6 <+624>:	cmp    $0xbc6,%eax
```

it gets the current uid and then do a series of comparison to multiple uid in the 3000 range which corresponds to the user flag00 to flag14.
In particular, flag14 is 3014, so if we manually change the uid to 3014, the program should get us our flag

The issue we face when doing this is that we can't access the getuid function as we get an error message : 'you should not reverse this' and the program exits.

Maybe we can force an access to the instruction that displays the token for level14 by modifying the eip registers that is responsible for the next instruction that need to be executed

```bash
   0x08048bb6 <+624>:	cmp    $0xbc6,%eax
   0x08048bbb <+629>:	je     0x8048de5 <main+1183>
```

if the value of getuid is equal to 0xbc6 (3014 in hexadecimal), the program goes to address 0x8048de5

```bash
   0x08048de5 <+1183>:	mov    0x804b060,%eax
   0x08048dea <+1188>:	mov    %eax,%ebx
   0x08048dec <+1190>:	movl   $0x8049220,(%esp)
   0x08048df3 <+1197>:	call   0x8048604 <ft_des>
```

it then calls the ft_des function with the value in 0x8049220, which is 
```bash
(gdb) x/s 0x8049220
0x8049220:	 "g <t61:|4_|!@IF.-62FH&G~DCK/Ekrvvdwz?v|"
```

as we guessed. If we set $eip=0x08048de5 then move onto the following instructions, the program finally displays:
```bash
0x08048e3f in main ()
(gdb) ni
7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
```

if we use it, we can log in to the flag14 user, and use the getflag command that gives us the same key

```bash
level14@SnowCrash:~$ su flag14
Password: 
Congratulation. Type getflag to get the key and send it to me the owner of this livecd :)
flag14@SnowCrash:~$ getflag
Check flag.Here is your token : 7QiHafiNa3HVozsaXkawuYrTstxbpABHD8CPnHJ
```