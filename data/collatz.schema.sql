CREATE TABLE IF NOT EXISTS PathDetails(
  start TEXT PRIMARY KEY,
  startBitLen INTEGER,
  md5hash TEXT NOT NULL,
  pathLen INTEGER,
  isLoop BOOLEAN DEFAULT false,
  loopLen INTEGER,
  largestValue TEXT,
  largestValueBitLen INTEGER
);

CREATE TABLE IF NOT EXISTS SeenValues(
  md5hash TEXT PRIMARY KEY UNIQUE,
  value TEXT NOT NULL,
  bitLen INTEGER
);

CREATE TABLE IF NOT EXISTS SeenDetails_PathDetails(
  md5hash TEXT,
  start TEXT,
  PRIMARY KEY (md5hash, start),
  FOREIGN KEY (md5hash)
    REFERENCES SeenValues (md5hash)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY (start)
    REFERENCES PathDetails (start)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);
