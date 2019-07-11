# hivehoney
Extract data from remote Hive to local Windows OS (without Hadoop client).

The most difficult part was figuring out expect+pbrun.

Because there are 2 interactive questions I had to pause after password.

 

Mode expect+pbrun details are here: https://github.com/hive-scripts/hivehoney/blob/master/expect_pbrun_howto.md

 
 

## Data access path.
```
Windows desktop->
               SSH->
                  Linux login->
                       pbrun service login->
                                           kinit
                                           beeline->
                                                   SQL->
                                                       save echo on Windows
                                
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

               







## Other scripts

 - https://github.com/pydemo/snowcli - Snowflake cli.
 - https://github.com/pydemo/Snowpipe-For-SQLServer - Memory pipe from SQLServer to Snowflake
 - https://github.com/pydemo/large-file-split-compress-parallel-upload-to-S3 - Chunked large file upload to S3
 
 
 
 
[<img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png">](https://www.buymeacoffee.com/0nJ32Xg)
