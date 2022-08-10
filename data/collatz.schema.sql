CREATE TABLE IF NOT EXISTS PathDetails(
  start TEXT PRIMARY KEY,
  startBitLen INTEGER,
  pathLen INTEGER,
  calcTime INTEGER,
  isLoop BOOLEAN,
  loopLen INTEGER
);

CREATE TABLE IF NOT EXISTS ShortcutDetails(
  start TEXT PRIMARY KEY,
  startBitLen INTEGER,
  pathLen INTEGER,
  calcTime INTEGER,
  isLoop BOOLEAN,
  loopLen INTEGER
);
