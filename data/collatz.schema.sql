CREATE TABLE IF NOT EXISTS PathDetails(
  start TEXT PRIMARY KEY,
  startBitLen INTEGER,
  hash TEXT NOT NULL,
  pathLen INTEGER,
  isLoop BOOLEAN,
  loopLen INTEGER,
  largestValue TEXT,
  largestValueBitLen INTEGER
);

CREATE TABLE IF NOT EXISTS SeenValues(
  hash TEXT PRIMARY KEY UNIQUE,
  value TEXT NOT NULL,
  bitLen INTEGER
);

CREATE TABLE IF NOT EXISTS SeenDetails_PathDetails(
  hash TEXT,
  start TEXT,
  PRIMARY KEY (hash, start),
  FOREIGN KEY (hash)
    REFERENCES SeenValues (hash)
      ON DELETE CASCADE
      ON UPDATE NO ACTION,
  FOREIGN KEY (start)
    REFERENCES PathDetails (start)
      ON DELETE CASCADE
      ON UPDATE NO ACTION
);
