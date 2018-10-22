-- CREATE TABLE GenreType (
--        Id CHAR(1) PRIMARY KEY NOT NULL,
--        TypeName TEXT,
--        Seq INTEGER
-- );

-- CREATE TABLE MediaType (
--        Id CHAR(1) PRIMARY KEY NOT NULL,
--        TypeName TEXT,
--        Seq INTEGER
-- );

-- CREATE TABLE ProfessionType (
--        Id CHAR(1) PRIMARY KEY NOT NULL,
--        TypeName TEXT,
--        Seq INTEGER
--);

DROP TABLE IF EXISTS TitleGenre;
DROP TABLE IF EXISTS Title;
DROP TABLE IF EXISTS EpisodeOf;
DROP TABLE IF EXISTS Rating;
DROP TABLE IF EXISTS RegionInfo;
DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Wrote;
DROP TABLE IF EXISTS Directed;
DROP TABLE IF EXISTS PlayedCharacter;
DROP TABLE IF EXISTS PrincipalIn;
DROP TABLE IF EXISTS KnownFor;

CREATE TABLE TitleGenre (
       TitleID NOT NULL REFERENCES Title(TitleID),
       Genre NOT NULL, -- REFERENCES GenreType(genre),
       PRIMARY KEY(TitleID, Genre)
);

CREATE TABLE Title (
       TitleID  PRIMARY KEY NOT NULL,
       RunTime INTEGER,
       OriginalTitle TEXT,
       StartYear TEXT,
       EndYear TEXT,
       Description TEXT,
       MediaType NOT NULL -- REFERENCES MediaType(MediaType)
);

CREATE TABLE EpisodeOf (
       EpisodeId INTEGER REFERENCES Title(TitleID),
       SeriesId INTEGER REFERENCES Title(TitleID),
       SeasonNumber INTEGER,
       EpisodeNumber INTEGER,
       PRIMARY KEY(EpisodeID, SeriesId)
);

CREATE TABLE Rating (
       TitleID PRIMARY KEY NOT NULL,
       AverageRating REAL,
       VoteCount INTEGER,
       MetaScore REAL,
       Revenue REAL
);

CREATE TABLE RegionInfo (
       TitleID INTEGER REFERENCES Title(TitleID),
       Ordering INTEGER,
       Region CHAR(2),
       LocalTitle TEXT,
       LocalLanguage TEXT,
       IsOriginal BOOLEAN,
       PRIMARY KEY (TitleID, Ordering)
);

CREATE TABLE Person (
       PersonID PRIMARY KEY NOT NULL,
       PersonName TEXT,
       BirthYear TEXT,
       DeathYear TEXT,
       PProffession INTEGER NOT NULL, -- REFERENCES ProfessionType(PProffession),
       PProffession2 INTEGER, -- REFERENCES ProfessionType(PProffession2),
       PProffession3 INTEGER --  REFERENCES ProfessionType(PProffession3)
);

CREATE TABLE KnownFor (
       TitleID INTEGER REFERENCES Title(TitleID),
       PersonID INTEGER REFERENCES Person(PersonID),
       PRIMARY KEY(TitleID, PersonID)
);

CREATE TABLE Wrote (
       TitleID INTEGER REFERENCES Title(TitleID),
       PersonID INTEGER REFERENCES Person(PersonID),
       PRIMARY KEY(TitleID, PersonID)
);

CREATE TABLE Directed (
       TitleID INTEGER REFERENCES Title(TitleID),
       PersonID INTEGER REFERENCES Person(PersonID),
       PRIMARY KEY(TitleID, PersonID)
);

CREATE TABLE PlayedCharacter (
       TitleID INTEGER REFERENCES Title(TitleID),
       PersonID INTEGER REFERENCES Person(PersonID),
       CharacterName TEXT
);

CREATE TABLE PrincipalIn (
       TitleID INTEGER REFERENCES Title(TitleID),
       PersonID INTEGER REFERENCES Person(PersonID),
       Ordering INTEGER,
       JobType TEXT,
       JobTitle TEXT,
       PRIMARY KEY(TitleID, PersonID, Ordering)
);

-- INSERT INTO MediaType VALUES ('a', 'alternative', 1);
-- INSERT INTO MediaType VALUES ('d', 'dvd', 2);
-- INSERT INTO MediaType VALUES ('f', 'festival', 3);
-- INSERT INTO MediaType VALUES ('t', 'tv', 4);
-- INSERT INTO MediaType VALUES ('v', 'video', 5);
-- INSERT INTO MediaType VALUES ('w', 'working',6);
-- INSERT INTO MediaType VALUES ('o', 'original', 7);
-- INSERT INTO MediaType VALUES ('i', 'imbdDisplay',8);
