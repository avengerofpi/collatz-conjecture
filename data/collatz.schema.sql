CREATE TABLE IF NOT EXISTS PathDetails(
  start TEXT PRIMARY KEY,
  startBitLen INTEGER,
  pathLen INTEGER,
  isLoop BOOLEAN,
  loopLen INTEGER
);
