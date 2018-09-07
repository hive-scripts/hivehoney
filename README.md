# hivehoney
Extract data from Hive to local Windows OS.

The most difficult part was figuring out expect+pbrun.

Because there are 2 interactive questions I had to pause after password.

 

Mode expect+pbrun details are here: https://github.com/hive-scripts/hivehoney/blob/master/expect_pbrun_howto.md

 
 

## Data access path.
```
Linux login->
            pbrun service login->
                                kinit
                                beeline->
                                        SQL->
                                            save echo on Windows OS
                                
```
 

 

## Run it like this:

 
```
set PROXY_HOST=your_bastion_host

set SERVICE_USER=you_func_user

set LINUX_USER=your_SOID

set LINUX_PWD=your_pwd

python hh.py --query_file=query.sql
```
 

### query.sql

select * from gfocnnsg_work.pytest LIMIT  1000000;  
 

## Result:

 

      TOTAL BYTES:    60000127

      Elaplsed: 79.637 s

      exit status:  0

      0

      []

      TOTAL Elaplsed: 99.060 s

 

### data_dump.csv

 

      c:\tmp>dir data_dump.csv



      Directory of c:\tmp

      09/04/2018  12:53 PM        60,000,075 data_dump.csv

                     1 File(s)     60,000,075 bytes

                     0 Dir(s)     321,822,720 bytes free

               
