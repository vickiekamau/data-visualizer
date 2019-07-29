DROP TABLE IF EXISTS dbo.number;
GO


CREATE TABLE dbo.number
(
 ID int identity(1,1)
,Num tinyint NOT NULL
)


-- Do some inserts to mimic the data stream
INSERT INTO dbo.LiveStatsFromSQLServer(num)
SELECT ABS(CHECKSUM(NewId())) % 14
WAITFOR DELAY '00:00:01.500'
GO 1000






