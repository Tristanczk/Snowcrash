In level09, we also have an executable level09 and a token file
This type, we can read the token file, but the content contains non displayable characters

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


