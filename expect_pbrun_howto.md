
Using expect tool you can automate password entry and also answer other pbrun interactive questions.

 

# Option 1.

Hardcoding password in expect file (pblogin.exp)

 
```expect
#!/usr/bin/expect -f  
set timeout 300  
  
  
spawn -noecho pbrun gfocnnsg &  
expect -re "Password:"  
send "your-password\r"  
  
  
sleep 1  
expect "Enter reason for this privilege access:"  
send "your-reason\r"  
interact  
```

 

File permission.

Change file permission so nobody reads your creds.

 

chmod u+wrx pb.exp

ls -al pb.exp

-rwx------ 1 ob66759 analyst 614 Sep  3 11:58 pb.exp

 

Run it like this:

./pblogin.exp

 

 

You can also use parameters in your expect script.

 

# Option 2.

Passing password as argument.

File pblogin_args.exp

 
```expect
#!/usr/bin/expect -f  
set timeout 300  
set usr [lindex $argv 0];  
set pwd [lindex $argv 1];  
set reason[lindex $argv 3];  
spawn -noecho pbrun $usr &  
expect -re "Password:"  
send "$pwd\r"  
sleep 1  
expect "Enter reason for this privilege access:"  
send "$reason\r"  
```

Run it like this:

 

./pblogin_args.exp "your_user" "your_pwd" "your_reason"

 

# Option 3.

Saving password in a temp file.

 
```expect
#!/usr/bin/expect -f  
  
  
if { $argc<1 } {  
        send_user "usage: $argv0 <passwdfile> \n"  
        exit 1  
}  
set timeout 20  
set passwdfile [ open [lindex $argv 0] ]  
catch {spawn -noecho ./myscript.sh}  
expect "Password:\ " {  
        while {[gets $passwdfile passwd] >= 0} {  
                send "$passwd\r"  
                }  
}  
  
  
sleep 1  
expect "Enter reason for this privilege access:"   
send "test\r";  
  
  
interact  
``` 

Run:

 

./run.exp .pfile
