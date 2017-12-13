CREATE TABLE IF NOT EXISTS data (
device_name VARCHAR(18),
device_location VARCHAR(7),
requester_public key VARCHAR(3),
grantedDataRequest_ID INT,
device_data size INT,
pendingDataRequest_requester ID INT,
grantedDataRequest_access start date VARCHAR(9),
device_ID INT,
pendingDataRequest_ID INT,
data source_name VARCHAR(17),
grantedDataRequest_deviceSummary ID INT,
pendingDataRequest_access start date VARCHAR(9),
device_type VARCHAR(11),
pendingDataRequest_access end date VARCHAR(9),
grantedDataRequest_access end date VARCHAR(9),
requester_ID INT,
deviceSummary_device ID INT,
deviceSummary_access duration VARCHAR(24),
device_src_ID INT,
deviceSummary_ID INT,
pendingDataRequest_deviceSummary ID INT,
requester_name VARCHAR(17),
grantedDataRequest_requester ID INT,
data source_src_ID INT
);

INSERT INTO data VALUES
('Living room camera','Home','ABR',0,15000,1,'12/5/2017',0,3,'Illinois Security',0,'12/5/2017','Camera','12/5/2017','12/5/2017',0,0,'access to realtime data',0,0,2,'Anti-intruder app',0,0),
('Phone location','varying','BLA',1,120,1,'12/5/2017',1,3,'JSM',1,'12/5/2017','GPS','12/5/2017','12/5/2017',1,0,'full access',0,1,2,'Google Photos',1,1),
('Home thermostat','Home','HAH',2,25,1,'12/5/2017',2,3,NULL,2,'12/5/2017','temperature','12/5/2017','12/5/2017',2,2,'access to hourly average',1,2,2,'Smarthome app',2,NULL);