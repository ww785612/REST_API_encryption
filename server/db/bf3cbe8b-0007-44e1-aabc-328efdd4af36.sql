CREATE TABLE IF NOT EXISTS device (
ID INT,
data size INT,
location VARCHAR(45),
name VARCHAR(45),
src_ID INT,
type VARCHAR(45)
);

INSERT INTO device VALUES
(0,15000,'Home','Living room camera',0,'Camera'),
(1,120,'varying','Phone location',0,'GPS'),
(2,25,'Home','Home thermostat',1,'temperature');

CREATE TABLE IF NOT EXISTS deviceSummary (
ID INT,
access duration VARCHAR(45),
device ID INT
);

INSERT INTO deviceSummary VALUES
(0,'access to realtime data',0),
(1,'full access',0),
(2,'access to hourly average',2);

CREATE TABLE IF NOT EXISTS pendingDataRequest (
ID INT,
access end date VARCHAR(20),
access start date VARCHAR(20),
deviceSummary ID INT,
requester ID INT
);

INSERT INTO pendingDataRequest VALUES
(3,'12/5/2017','12/5/2017',2,1);

CREATE TABLE IF NOT EXISTS grantedDataRequest (
ID INT,
access end date VARCHAR(20),
access start date VARCHAR(20),
deviceSummary ID INT,
requester ID INT
);

INSERT INTO grantedDataRequest VALUES
(0,'12/5/2017','12/5/2017',0,0),
(1,'12/5/2017','12/5/2017',1,1),
(2,'12/5/2017','12/5/2017',2,2);


CREATE TABLE IF NOT EXISTS deniedDataRequest (
ID INT,
access end date VARCHAR(20),
access start date VARCHAR(20),
deviceSummary ID INT,
requester ID INT
);

CREATE TABLE IF NOT EXISTS requester (
ID INT,
name VARCHAR(45),
public key VARCHAR(5000)
);

INSERT INTO requester VALUES
(0,'Anti-intruder app','ABR'),
(1,'Google Photos','BLA'),
(2,'Smarthome app','HAH');

CREATE TABLE IF NOT EXISTS data_source (
name VARCHAR(40),
src_ID INT
);

INSERT INTO data_source VALUES
('Illinois Security',0),
('JSM',1);
