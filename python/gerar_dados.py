# -*- coding: utf-8 -*-
"""
gerar_dados.py
==============
Recria a base Human Resources (HR) - o mesmo conjunto de dados de exemplo
disponibilizado no FreeSQL (esquema HR / Oracle HR sample schema) - dentro
de um banco SQLite local e executa EXATAMENTE as consultas dos arquivos
`sql/query_1.sql` e `sql/query_2.sql`, exportando os resultados para
`dados/query_01.csv` e `dados/query_02.csv`.

Por que este script existe?
---------------------------
As consultas do projeto foram escritas para o FreeSQL (MySQL/MariaDB). Para
que qualquer pessoa consiga REPRODUZIR os arquivos CSV sem precisar de
acesso a internet nem de credenciais do FreeSQL, este script carrega os
mesmos dados da base HR e roda as mesmas queries localmente. Assim os CSV
entregues sao, comprovadamente, o resultado das consultas .sql.

Como executar:
    python gerar_dados.py

Saida:
    dados/query_01.csv        -> resultado da Query 1 (Salario por Depto/Cargo)
    dados/query_02.csv        -> resultado da Query 2 (Funcionarios por Regiao)
    sql/hr_seed_mysql.sql     -> script de carga (CREATE + INSERT) para o FreeSQL
"""

import os
import csv
import sqlite3

# ---------------------------------------------------------------------------
# Caminhos (sempre relativos a raiz do projeto, nao ao diretorio atual)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_DIR = os.path.join(BASE_DIR, "sql")
DADOS_DIR = os.path.join(BASE_DIR, "dados")

# ---------------------------------------------------------------------------
# DADOS DA BASE HR  (conjunto de exemplo padrao do esquema Human Resources)
# ---------------------------------------------------------------------------

REGIONS = [
    (1, "Europe"),
    (2, "Americas"),
    (3, "Asia"),
    (4, "Middle East and Africa"),
]

# (COUNTRY_ID, COUNTRY_NAME, REGION_ID)
COUNTRIES = [
    ("AR", "Argentina", 2), ("AU", "Australia", 3), ("BE", "Belgium", 1),
    ("BR", "Brazil", 2), ("CA", "Canada", 2), ("CH", "Switzerland", 1),
    ("CN", "China", 3), ("DE", "Germany", 1), ("DK", "Denmark", 1),
    ("EG", "Egypt", 4), ("FR", "France", 1), ("HK", "HongKong", 3),
    ("IL", "Israel", 4), ("IN", "India", 3), ("IT", "Italy", 1),
    ("JP", "Japan", 3), ("KW", "Kuwait", 4), ("MX", "Mexico", 2),
    ("NG", "Nigeria", 4), ("NL", "Netherlands", 1), ("SG", "Singapore", 3),
    ("UK", "United Kingdom", 1), ("US", "United States of America", 2),
    ("ZM", "Zambia", 4), ("ZW", "Zimbabwe", 4),
]

# (LOCATION_ID, STREET_ADDRESS, POSTAL_CODE, CITY, STATE_PROVINCE, COUNTRY_ID)
LOCATIONS = [
    (1000, "1297 Via Cola di Rie", "00989", "Roma", None, "IT"),
    (1100, "93091 Calle della Testa", "10934", "Venice", None, "IT"),
    (1200, "2017 Shinjuku-ku", "1689", "Tokyo", "Tokyo Prefecture", "JP"),
    (1300, "9450 Kamiya-cho", "6823", "Hiroshima", None, "JP"),
    (1400, "2014 Jabberwocky Rd", "26192", "Southlake", "Texas", "US"),
    (1500, "2011 Interiors Blvd", "99236", "South San Francisco", "California", "US"),
    (1600, "2007 Zagora St", "50090", "South Brunswick", "New Jersey", "US"),
    (1700, "2004 Charade Rd", "98199", "Seattle", "Washington", "US"),
    (1800, "147 Spadina Ave", "M5V 2L7", "Toronto", "Ontario", "CA"),
    (1900, "6092 Boxwood St", "YSW 9T2", "Whitehorse", "Yukon", "CA"),
    (2000, "40-5-12 Laogianggen", "190518", "Beijing", None, "CN"),
    (2100, "1298 Vileparle (E)", "490231", "Bombay", "Maharashtra", "IN"),
    (2200, "12-98 Victoria Street", "2901", "Sydney", "New South Wales", "AU"),
    (2300, "198 Clementi North", "540198", "Singapore", None, "SG"),
    (2400, "8204 Arthur St", None, "London", None, "UK"),
    (2500, "Magdalen Centre, Oxford Science Park", "OX9 9ZB", "Oxford", "Oxford", "UK"),
    (2600, "9702 Chester Road", "09629850293", "Stretford", "Manchester", "UK"),
    (2700, "Schwanthalerstr. 7031", "80925", "Munich", "Bavaria", "DE"),
    (2800, "Rua Frei Caneca 1360", "01307-002", "Sao Paulo", "Sao Paulo", "BR"),
    (2900, "20 Rue des Corps-Saints", "1730", "Geneva", "Geneve", "CH"),
    (3000, "Murtenstrasse 921", "3095", "Bern", "BE", "CH"),
    (3100, "Pieter Breughelstraat 837", "3029SK", "Utrecht", "Utrecht", "NL"),
    (3200, "Mariano Escobedo 9991", "11932", "Mexico City", "Distrito Federal", "MX"),
]

# (DEPARTMENT_ID, DEPARTMENT_NAME, MANAGER_ID, LOCATION_ID)
DEPARTMENTS = [
    (10, "Administration", 200, 1700),
    (20, "Marketing", 201, 1800),
    (30, "Purchasing", 114, 1700),
    (40, "Human Resources", 203, 2400),
    (50, "Shipping", 121, 1500),
    (60, "IT", 103, 1400),
    (70, "Public Relations", 204, 2700),
    (80, "Sales", 145, 2500),
    (90, "Executive", 100, 1700),
    (100, "Finance", 108, 1700),
    (110, "Accounting", 205, 1700),
    (120, "Treasury", None, 1700),
    (130, "Corporate Tax", None, 1700),
    (140, "Control And Credit", None, 1700),
    (150, "Shareholder Services", None, 1700),
    (160, "Benefits", None, 1700),
    (170, "Manufacturing", None, 1700),
    (180, "Construction", None, 1700),
    (190, "Contracting", None, 1700),
    (200, "Operations", None, 1700),
    (210, "IT Support", None, 1700),
    (220, "NOC", None, 1700),
    (230, "IT Helpdesk", None, 1700),
    (240, "Government Sales", None, 1700),
    (250, "Retail Sales", None, 1700),
    (260, "Recruiting", None, 1700),
    (270, "Payroll", None, 1700),
]

# (JOB_ID, JOB_TITLE, MIN_SALARY, MAX_SALARY)
JOBS = [
    ("AD_PRES", "President", 20080, 40000),
    ("AD_VP", "Administration Vice President", 15000, 30000),
    ("AD_ASST", "Administration Assistant", 3000, 6000),
    ("FI_MGR", "Finance Manager", 8200, 16000),
    ("FI_ACCOUNT", "Accountant", 4200, 9000),
    ("AC_MGR", "Accounting Manager", 8200, 16000),
    ("AC_ACCOUNT", "Public Accountant", 4200, 9000),
    ("SA_MAN", "Sales Manager", 10000, 20080),
    ("SA_REP", "Sales Representative", 6000, 12008),
    ("PU_MAN", "Purchasing Manager", 8000, 15000),
    ("PU_CLERK", "Purchasing Clerk", 2500, 5500),
    ("ST_MAN", "Stock Manager", 5500, 8500),
    ("ST_CLERK", "Stock Clerk", 2008, 5000),
    ("SH_CLERK", "Shipping Clerk", 2500, 5500),
    ("IT_PROG", "Programmer", 4000, 10000),
    ("MK_MAN", "Marketing Manager", 9000, 15000),
    ("MK_REP", "Marketing Representative", 4000, 9000),
    ("HR_REP", "Human Resources Representative", 4000, 9000),
    ("PR_REP", "Public Relations Representative", 4500, 10500),
]

# (EMPLOYEE_ID, FIRST_NAME, LAST_NAME, EMAIL, PHONE_NUMBER, HIRE_DATE,
#  JOB_ID, SALARY, COMMISSION_PCT, MANAGER_ID, DEPARTMENT_ID)
EMPLOYEES = [
    (100, "Steven", "King", "SKING", "515.123.4567", "1987-06-17", "AD_PRES", 24000, None, None, 90),
    (101, "Neena", "Kochhar", "NKOCHHAR", "515.123.4568", "1989-09-21", "AD_VP", 17000, None, 100, 90),
    (102, "Lex", "De Haan", "LDEHAAN", "515.123.4569", "1993-01-13", "AD_VP", 17000, None, 100, 90),
    (103, "Alexander", "Hunold", "AHUNOLD", "590.423.4567", "1990-01-03", "IT_PROG", 9000, None, 102, 60),
    (104, "Bruce", "Ernst", "BERNST", "590.423.4568", "1991-05-21", "IT_PROG", 6000, None, 103, 60),
    (105, "David", "Austin", "DAUSTIN", "590.423.4569", "1997-06-25", "IT_PROG", 4800, None, 103, 60),
    (106, "Valli", "Pataballa", "VPATABAL", "590.423.4560", "1998-02-05", "IT_PROG", 4800, None, 103, 60),
    (107, "Diana", "Lorentz", "DLORENTZ", "590.423.5567", "1999-02-07", "IT_PROG", 4200, None, 103, 60),
    (108, "Nancy", "Greenberg", "NGREENBE", "515.124.4569", "1994-08-17", "FI_MGR", 12008, None, 101, 100),
    (109, "Daniel", "Faviet", "DFAVIET", "515.124.4169", "1994-08-16", "FI_ACCOUNT", 9000, None, 108, 100),
    (110, "John", "Chen", "JCHEN", "515.124.4269", "1997-09-28", "FI_ACCOUNT", 8200, None, 108, 100),
    (111, "Ismael", "Sciarra", "ISCIARRA", "515.124.4369", "1997-09-30", "FI_ACCOUNT", 7700, None, 108, 100),
    (112, "Jose Manuel", "Urman", "JMURMAN", "515.124.4469", "1998-03-07", "FI_ACCOUNT", 7800, None, 108, 100),
    (113, "Luis", "Popp", "LPOPP", "515.124.4567", "1999-12-07", "FI_ACCOUNT", 6900, None, 108, 100),
    (114, "Den", "Raphaely", "DRAPHEAL", "515.127.4561", "1994-12-07", "PU_MAN", 11000, None, 100, 30),
    (115, "Alexander", "Khoo", "AKHOO", "515.127.4562", "1995-05-18", "PU_CLERK", 3100, None, 114, 30),
    (116, "Shelli", "Baida", "SBAIDA", "515.127.4563", "1997-12-24", "PU_CLERK", 2900, None, 114, 30),
    (117, "Sigal", "Tobias", "STOBIAS", "515.127.4564", "1997-07-24", "PU_CLERK", 2800, None, 114, 30),
    (118, "Guy", "Himuro", "GHIMURO", "515.127.4565", "1998-11-15", "PU_CLERK", 2600, None, 114, 30),
    (119, "Karen", "Colmenares", "KCOLMENA", "515.127.4566", "1999-08-10", "PU_CLERK", 2500, None, 114, 30),
    (120, "Matthew", "Weiss", "MWEISS", "650.123.1234", "1996-07-18", "ST_MAN", 8000, None, 100, 50),
    (121, "Adam", "Fripp", "AFRIPP", "650.123.2234", "1997-04-10", "ST_MAN", 8200, None, 100, 50),
    (122, "Payam", "Kaufling", "PKAUFLIN", "650.123.3234", "1995-05-01", "ST_MAN", 7900, None, 100, 50),
    (123, "Shanta", "Vollman", "SVOLLMAN", "650.123.4234", "1997-10-10", "ST_MAN", 6500, None, 100, 50),
    (124, "Kevin", "Mourgos", "KMOURGOS", "650.123.5234", "1999-11-16", "ST_MAN", 5800, None, 100, 50),
    (125, "Julia", "Nayer", "JNAYER", "650.124.1214", "1997-07-16", "ST_CLERK", 3200, None, 120, 50),
    (126, "Irene", "Mikkilineni", "IMIKKILI", "650.124.1224", "1998-09-28", "ST_CLERK", 2700, None, 120, 50),
    (127, "James", "Landry", "JLANDRY", "650.124.1334", "1999-01-14", "ST_CLERK", 2400, None, 120, 50),
    (128, "Steven", "Markle", "SMARKLE", "650.124.1434", "2000-03-08", "ST_CLERK", 2200, None, 120, 50),
    (129, "Laura", "Bissot", "LBISSOT", "650.124.5234", "1997-08-20", "ST_CLERK", 3300, None, 121, 50),
    (130, "Mozhe", "Atkinson", "MATKINSO", "650.124.6234", "1997-10-30", "ST_CLERK", 2800, None, 121, 50),
    (131, "James", "Marlow", "JAMRLOW", "650.124.7234", "1997-02-16", "ST_CLERK", 2500, None, 121, 50),
    (132, "TJ", "Olson", "TJOLSON", "650.124.8234", "1999-04-10", "ST_CLERK", 2100, None, 121, 50),
    (133, "Jason", "Mallin", "JMALLIN", "650.127.1934", "1996-06-14", "ST_CLERK", 3300, None, 122, 50),
    (134, "Michael", "Rogers", "MROGERS", "650.127.1834", "1998-08-26", "ST_CLERK", 2900, None, 122, 50),
    (135, "Ki", "Gee", "KGEE", "650.127.1734", "1999-12-12", "ST_CLERK", 2400, None, 122, 50),
    (136, "Hazel", "Philtanker", "HPHILTAN", "650.127.1634", "2000-02-06", "ST_CLERK", 2200, None, 122, 50),
    (137, "Renske", "Ladwig", "RLADWIG", "650.121.1234", "1995-07-14", "ST_CLERK", 3600, None, 123, 50),
    (138, "Stephen", "Stiles", "SSTILES", "650.121.2034", "1997-10-26", "ST_CLERK", 3200, None, 123, 50),
    (139, "John", "Seo", "JSEO", "650.121.2019", "1998-02-12", "ST_CLERK", 2700, None, 123, 50),
    (140, "Joshua", "Patel", "JPATEL", "650.121.1834", "1998-04-06", "ST_CLERK", 2500, None, 123, 50),
    (141, "Trenna", "Rajs", "TRAJS", "650.121.8009", "1995-10-17", "ST_CLERK", 3500, None, 124, 50),
    (142, "Curtis", "Davies", "CDAVIES", "650.121.2994", "1997-01-29", "ST_CLERK", 3100, None, 124, 50),
    (143, "Randall", "Matos", "RMATOS", "650.121.2874", "1998-03-15", "ST_CLERK", 2600, None, 124, 50),
    (144, "Peter", "Vargas", "PVARGAS", "650.121.2004", "1998-07-09", "ST_CLERK", 2500, None, 124, 50),
    (145, "John", "Russell", "JRUSSEL", "011.44.1344.429268", "1996-10-01", "SA_MAN", 14000, 0.4, 100, 80),
    (146, "Karen", "Partners", "KPARTNER", "011.44.1344.467268", "1997-01-05", "SA_MAN", 13500, 0.3, 100, 80),
    (147, "Alberto", "Errazuriz", "AERRAZUR", "011.44.1344.429278", "1997-03-10", "SA_MAN", 12000, 0.3, 100, 80),
    (148, "Gerald", "Cambrault", "GCAMBRAU", "011.44.1344.619268", "1999-10-15", "SA_MAN", 11000, 0.3, 100, 80),
    (149, "Eleni", "Zlotkey", "EZLOTKEY", "011.44.1344.429018", "2000-01-29", "SA_MAN", 10500, 0.2, 100, 80),
    (150, "Peter", "Tucker", "PTUCKER", "011.44.1344.129268", "1997-01-30", "SA_REP", 10000, 0.3, 145, 80),
    (151, "David", "Bernstein", "DBERNSTE", "011.44.1344.345268", "1997-03-24", "SA_REP", 9500, 0.25, 145, 80),
    (152, "Peter", "Hall", "PHALL", "011.44.1344.478968", "1997-08-20", "SA_REP", 9000, 0.25, 145, 80),
    (153, "Christopher", "Olsen", "COLSEN", "011.44.1344.498718", "1998-03-30", "SA_REP", 8000, 0.2, 145, 80),
    (154, "Nanette", "Cambrault", "NCAMBRAU", "011.44.1344.987668", "1998-12-09", "SA_REP", 7500, 0.2, 145, 80),
    (155, "Oliver", "Tuvault", "OTUVAULT", "011.44.1344.486508", "1999-11-23", "SA_REP", 7000, 0.15, 145, 80),
    (156, "Janette", "King", "JKING", "011.44.1345.429268", "1996-01-30", "SA_REP", 10000, 0.35, 146, 80),
    (157, "Patrick", "Sully", "PSULLY", "011.44.1345.929268", "1996-03-04", "SA_REP", 9500, 0.35, 146, 80),
    (158, "Allan", "McEwen", "AMCEWEN", "011.44.1345.829268", "1996-08-01", "SA_REP", 9000, 0.35, 146, 80),
    (159, "Lindsey", "Smith", "LSMITH", "011.44.1345.729268", "1997-03-10", "SA_REP", 8000, 0.3, 146, 80),
    (160, "Louise", "Doran", "LDORAN", "011.44.1345.629268", "1997-12-15", "SA_REP", 7500, 0.3, 146, 80),
    (161, "Sarath", "Sewall", "SSEWALL", "011.44.1345.529268", "1998-11-03", "SA_REP", 7000, 0.25, 146, 80),
    (162, "Clara", "Vishney", "CVISHNEY", "011.44.1346.129268", "1997-11-11", "SA_REP", 10500, 0.25, 147, 80),
    (163, "Danielle", "Greene", "DGREENE", "011.44.1346.229268", "1999-03-19", "SA_REP", 9500, 0.15, 147, 80),
    (164, "Mattea", "Marvins", "MMARVINS", "011.44.1346.329268", "2000-01-24", "SA_REP", 7200, 0.1, 147, 80),
    (165, "David", "Lee", "DLEE", "011.44.1346.529268", "2000-02-23", "SA_REP", 6800, 0.1, 147, 80),
    (166, "Sundar", "Ande", "SANDE", "011.44.1346.629268", "2000-03-24", "SA_REP", 6400, 0.1, 147, 80),
    (167, "Amit", "Banda", "ABANDA", "011.44.1346.729268", "2000-04-21", "SA_REP", 6200, 0.1, 147, 80),
    (168, "Lisa", "Ozer", "LOZER", "011.44.1343.929268", "1997-03-11", "SA_REP", 11500, 0.25, 148, 80),
    (169, "Harrison", "Bloom", "HBLOOM", "011.44.1343.829268", "1998-03-23", "SA_REP", 10000, 0.2, 148, 80),
    (170, "Tayler", "Fox", "TFOX", "011.44.1343.729268", "1998-01-24", "SA_REP", 9600, 0.2, 148, 80),
    (171, "William", "Smith", "WSMITH", "011.44.1343.629268", "1999-02-23", "SA_REP", 7400, 0.15, 148, 80),
    (172, "Elizabeth", "Bates", "EBATES", "011.44.1343.529268", "1999-03-24", "SA_REP", 7300, 0.15, 148, 80),
    (173, "Sundita", "Kumar", "SKUMAR", "011.44.1343.329268", "2000-04-21", "SA_REP", 6100, 0.1, 148, 80),
    (174, "Ellen", "Abel", "EABEL", "011.44.1644.429267", "1996-05-11", "SA_REP", 11000, 0.3, 149, 80),
    (175, "Alyssa", "Hutton", "AHUTTON", "011.44.1644.429266", "1997-03-19", "SA_REP", 8800, 0.25, 149, 80),
    (176, "Jonathon", "Taylor", "JTAYLOR", "011.44.1644.429265", "1998-03-24", "SA_REP", 8600, 0.2, 149, 80),
    (177, "Jack", "Livingston", "JLIVINGS", "011.44.1644.429264", "1998-04-23", "SA_REP", 8400, 0.2, 149, 80),
    (178, "Kimberely", "Grant", "KGRANT", "011.44.1644.429263", "1999-05-24", "SA_REP", 7000, 0.15, 149, None),
    (179, "Charles", "Johnson", "CJOHNSON", "011.44.1644.429262", "2000-01-04", "SA_REP", 6200, 0.1, 149, 80),
    (180, "Winston", "Taylor", "WTAYLOR", "650.507.9876", "1998-01-24", "SH_CLERK", 3200, None, 120, 50),
    (181, "Jean", "Fleaur", "JFLEAUR", "650.507.9877", "1998-02-23", "SH_CLERK", 3100, None, 120, 50),
    (182, "Martha", "Sullivan", "MSULLIVA", "650.507.9878", "1999-06-21", "SH_CLERK", 2500, None, 120, 50),
    (183, "Girard", "Geoni", "GGEONI", "650.507.9879", "2000-02-03", "SH_CLERK", 2800, None, 120, 50),
    (184, "Nandita", "Sarchand", "NSARCHAN", "650.509.1876", "1996-01-27", "SH_CLERK", 4200, None, 121, 50),
    (185, "Alexis", "Bull", "ABULL", "650.509.2876", "1997-02-20", "SH_CLERK", 4100, None, 121, 50),
    (186, "Julia", "Dellinger", "JDELLING", "650.509.3876", "1998-06-24", "SH_CLERK", 3400, None, 121, 50),
    (187, "Anthony", "Cabrio", "ACABRIO", "650.509.4876", "1999-02-07", "SH_CLERK", 3000, None, 121, 50),
    (188, "Kelly", "Chung", "KCHUNG", "650.505.1876", "1997-06-14", "SH_CLERK", 3800, None, 122, 50),
    (189, "Jennifer", "Dilly", "JDILLY", "650.505.2876", "1997-08-13", "SH_CLERK", 3600, None, 122, 50),
    (190, "Timothy", "Gates", "TGATES", "650.505.3876", "1998-07-11", "SH_CLERK", 2900, None, 122, 50),
    (191, "Randall", "Perkins", "RPERKINS", "650.505.4876", "1999-12-19", "SH_CLERK", 2500, None, 122, 50),
    (192, "Sarah", "Bell", "SBELL", "650.501.1876", "1996-02-04", "SH_CLERK", 4000, None, 123, 50),
    (193, "Britney", "Everett", "BEVERETT", "650.501.2876", "1997-03-03", "SH_CLERK", 3900, None, 123, 50),
    (194, "Samuel", "McCain", "SMCCAIN", "650.501.3876", "1998-07-01", "SH_CLERK", 3200, None, 123, 50),
    (195, "Vance", "Jones", "VJONES", "650.501.4876", "1999-03-17", "SH_CLERK", 2800, None, 123, 50),
    (196, "Alana", "Walsh", "AWALSH", "650.507.9811", "1998-04-24", "SH_CLERK", 3100, None, 124, 50),
    (197, "Kevin", "Feeney", "KFEENEY", "650.507.9822", "1998-05-23", "SH_CLERK", 3000, None, 124, 50),
    (198, "Donald", "OConnell", "DOCONNEL", "650.507.9833", "1999-06-21", "SH_CLERK", 2600, None, 124, 50),
    (199, "Douglas", "Grant", "DGRANT", "650.507.9844", "2000-01-13", "SH_CLERK", 2600, None, 124, 50),
    (200, "Jennifer", "Whalen", "JWHALEN", "515.123.4444", "1987-09-17", "AD_ASST", 4400, None, 101, 10),
    (201, "Michael", "Hartstein", "MHARTSTE", "515.123.5555", "1996-02-17", "MK_MAN", 13000, None, 100, 20),
    (202, "Pat", "Fay", "PFAY", "603.123.6666", "1997-08-17", "MK_REP", 6000, None, 201, 20),
    (203, "Susan", "Mavris", "SMAVRIS", "515.123.7777", "1994-06-07", "HR_REP", 6500, None, 101, 40),
    (204, "Hermann", "Baer", "HBAER", "515.123.8888", "1994-06-07", "PR_REP", 10000, None, 101, 70),
    (205, "Shelley", "Higgins", "SHIGGINS", "515.123.8080", "1994-06-07", "AC_MGR", 12008, None, 101, 110),
    (206, "William", "Gietz", "WGIETZ", "515.123.8181", "1994-06-07", "AC_ACCOUNT", 8300, None, 205, 110),
]

# ---------------------------------------------------------------------------
# DDL (estrutura das tabelas) para o SQLite local
# ---------------------------------------------------------------------------
DDL = """
CREATE TABLE REGIONS (
    REGION_ID   INTEGER PRIMARY KEY,
    REGION_NAME TEXT
);
CREATE TABLE COUNTRIES (
    COUNTRY_ID   TEXT PRIMARY KEY,
    COUNTRY_NAME TEXT,
    REGION_ID    INTEGER
);
CREATE TABLE LOCATIONS (
    LOCATION_ID    INTEGER PRIMARY KEY,
    STREET_ADDRESS TEXT,
    POSTAL_CODE    TEXT,
    CITY           TEXT,
    STATE_PROVINCE TEXT,
    COUNTRY_ID     TEXT
);
CREATE TABLE DEPARTMENTS (
    DEPARTMENT_ID   INTEGER PRIMARY KEY,
    DEPARTMENT_NAME TEXT,
    MANAGER_ID      INTEGER,
    LOCATION_ID     INTEGER
);
CREATE TABLE JOBS (
    JOB_ID     TEXT PRIMARY KEY,
    JOB_TITLE  TEXT,
    MIN_SALARY INTEGER,
    MAX_SALARY INTEGER
);
CREATE TABLE EMPLOYEES (
    EMPLOYEE_ID    INTEGER PRIMARY KEY,
    FIRST_NAME     TEXT,
    LAST_NAME      TEXT,
    EMAIL          TEXT,
    PHONE_NUMBER   TEXT,
    HIRE_DATE      TEXT,
    JOB_ID         TEXT,
    SALARY         INTEGER,
    COMMISSION_PCT REAL,
    MANAGER_ID     INTEGER,
    DEPARTMENT_ID  INTEGER
);
"""


def construir_banco():
    """Cria um banco SQLite em memoria e carrega toda a base HR."""
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.executescript(DDL)
    cur.executemany("INSERT INTO REGIONS VALUES (?,?)", REGIONS)
    cur.executemany("INSERT INTO COUNTRIES VALUES (?,?,?)", COUNTRIES)
    cur.executemany("INSERT INTO LOCATIONS VALUES (?,?,?,?,?,?)", LOCATIONS)
    cur.executemany("INSERT INTO DEPARTMENTS VALUES (?,?,?,?)", DEPARTMENTS)
    cur.executemany("INSERT INTO JOBS VALUES (?,?,?,?)", JOBS)
    cur.executemany("INSERT INTO EMPLOYEES VALUES (?,?,?,?,?,?,?,?,?,?,?)", EMPLOYEES)
    con.commit()
    return con


def ler_sql(caminho):
    """Le o texto de um arquivo .sql (unica instrucao SELECT)."""
    with open(caminho, "r", encoding="utf-8") as f:
        return f.read().strip().rstrip(";")


def exportar_csv(con, sql_text, destino):
    """Executa a consulta e grava o resultado (com cabecalho) em CSV."""
    cur = con.cursor()
    cur.execute(sql_text)
    colunas = [d[0] for d in cur.description]
    linhas = cur.fetchall()
    with open(destino, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(colunas)
        writer.writerows(linhas)
    return colunas, linhas


def gerar_seed_mysql(destino):
    """Gera um script CREATE + INSERT compativel com MySQL/FreeSQL,
    para quem quiser recriar a base HR diretamente no FreeSQL."""
    def val(x):
        if x is None:
            return "NULL"
        if isinstance(x, (int, float)):
            return str(x)
        return "'" + str(x).replace("'", "''") + "'"

    def bloco(tabela, colunas, dados):
        linhas = [
            "INSERT INTO {} ({}) VALUES\n".format(tabela, ", ".join(colunas))
        ]
        vals = ["  ({})".format(", ".join(val(c) for c in reg)) for reg in dados]
        return linhas[0] + ",\n".join(vals) + ";\n\n"

    ddl_mysql = DDL.replace("INTEGER PRIMARY KEY", "INT PRIMARY KEY") \
                   .replace(" TEXT", " VARCHAR(100)") \
                   .replace(" REAL", " DECIMAL(4,2)")
    partes = ["-- Script de carga da base HR para MySQL / FreeSQL\n",
              "-- Gerado automaticamente por python/gerar_dados.py\n",
              "-- Execute no FreeSQL para reproduzir a base usada no projeto.\n",
              ddl_mysql, "\n"]
    partes.append(bloco("REGIONS", ["REGION_ID", "REGION_NAME"], REGIONS))
    partes.append(bloco("COUNTRIES", ["COUNTRY_ID", "COUNTRY_NAME", "REGION_ID"], COUNTRIES))
    partes.append(bloco("LOCATIONS", ["LOCATION_ID", "STREET_ADDRESS", "POSTAL_CODE",
                                      "CITY", "STATE_PROVINCE", "COUNTRY_ID"], LOCATIONS))
    partes.append(bloco("DEPARTMENTS", ["DEPARTMENT_ID", "DEPARTMENT_NAME",
                                        "MANAGER_ID", "LOCATION_ID"], DEPARTMENTS))
    partes.append(bloco("JOBS", ["JOB_ID", "JOB_TITLE", "MIN_SALARY", "MAX_SALARY"], JOBS))
    partes.append(bloco("EMPLOYEES", ["EMPLOYEE_ID", "FIRST_NAME", "LAST_NAME", "EMAIL",
                                      "PHONE_NUMBER", "HIRE_DATE", "JOB_ID", "SALARY",
                                      "COMMISSION_PCT", "MANAGER_ID", "DEPARTMENT_ID"], EMPLOYEES))
    with open(destino, "w", encoding="utf-8") as f:
        f.write("".join(partes))


def main():
    os.makedirs(DADOS_DIR, exist_ok=True)
    con = construir_banco()

    # validacao rapida de integridade da carga
    total = con.execute("SELECT COUNT(*) FROM EMPLOYEES").fetchone()[0]
    print("Base HR carregada: {} funcionarios, {} departamentos, {} cargos, "
          "{} localizacoes, {} paises, {} regioes.".format(
              total,
              con.execute("SELECT COUNT(*) FROM DEPARTMENTS").fetchone()[0],
              con.execute("SELECT COUNT(*) FROM JOBS").fetchone()[0],
              con.execute("SELECT COUNT(*) FROM LOCATIONS").fetchone()[0],
              con.execute("SELECT COUNT(*) FROM COUNTRIES").fetchone()[0],
              con.execute("SELECT COUNT(*) FROM REGIONS").fetchone()[0]))

    q1 = ler_sql(os.path.join(SQL_DIR, "query_1.sql"))
    q2 = ler_sql(os.path.join(SQL_DIR, "query_2.sql"))

    _, l1 = exportar_csv(con, q1, os.path.join(DADOS_DIR, "query_01.csv"))
    _, l2 = exportar_csv(con, q2, os.path.join(DADOS_DIR, "query_02.csv"))
    print("query_01.csv gerado com {} linhas (Salario por Departamento e Cargo).".format(len(l1)))
    print("query_02.csv gerado com {} linhas (Funcionarios por Regiao).".format(len(l2)))

    gerar_seed_mysql(os.path.join(SQL_DIR, "hr_seed_mysql.sql"))
    print("sql/hr_seed_mysql.sql gerado (carga para FreeSQL/MySQL).")

    con.close()
    print("Concluido.")


if __name__ == "__main__":
    main()
