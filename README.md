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

               
#
#
#
#
#   
# FAQ
#  
#### Can it extract CSV file to cluster node? 
No, it is extracting to local windows OS.

#### Can developers integrate Hive Honew into their ETL pipelines?
No. It's for ad-hoc data retrieval.

#### what's the purpose of Hive Honey?
Improve experience of Data and Business Analysts with Big Data.


#### What are the other ways to extract data from Hive?
You can use Hive syntax to extract data to HDFS or locally (to a node with Hadoop client)


#### Can it be executed without pbrun?
No, It's hardcoded to automate pbrun authorization.

#### Does it create any files?
Yes, it creates sql file with query and expect file for pbrun automation (in your bastion/jump host `/tmp` dir).

#### Explain steps of data extract?
From Windows desktop:
     1. SSH to Linux
     2. Pbrun service login
     3. kinit
     4. beeline executes SQL
     5. Echo of data from beeline is saved on Windows.
                                

#### What technology was used to create this tool
I used Python and paramiko to write it.

#### Can you modify functionality and add features?
Yes, please, ask me for new features.


## Teardown

https://github.com/pydemo/teardown

