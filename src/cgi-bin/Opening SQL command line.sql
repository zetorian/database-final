#Opening:

export PATH=$PATH:/usr/local/mysql/bin

mysql -u root -p 
    newpassword

use EMR
SELECT name FROM hospital; 

#Closing:
\q



Blue Insurance

INSERT INTO presciption (patient, doctor, date, expires) VALUES ('503', '100000010', '2016-08-23', '2018-08-04');
INSERT INTO patient (ssn, fname, lname, phone, address, insuranceCo, PrimaryDoctor) VALUES ('444', 'Seth', 'Stoltenow', '323','509','Blue Insurance', '100000000');

INSERT INTO Appointment (dateTime, location, doctor, patient, paid, ammountBilled) VALUES ()

INSERT INTO Appointment (dateTime, location, doctor, patient, paid, ammountBilled) VALUES ('2019-04-26T21:18', 'Blue Hospital', '100000010', '1234567', '50.00', '250.40');

--"dateTime DATETIME, location VARCHAR(255), doctor VARCHAR(9), patient VARCHAR(9), paid DECIMAL(7,2), ammountBilled DECIMAL(7,2)",

INSERT INTO procedures (procedureName, dateTime, doctor, patient, results, paid, amountBilled) VALUES ('In procedure', '2019-07-17T21:18', '100000010', '1234567', 'Here are some results', '50.00', '250.40');

--"id INT AUTO_INCREMENT, procedureName VARCHAR(255), dateTime DATETIME, doctor VARCHAR(9), patient VARCHAR(9), results TEXT, paid DECIMAL(7,2), amountBilled DECIMAL(7,2), PRIMARY KEY(id)",

