CREATE TABLE Descript (
    title varchar(255),
    fileurl varchar(253),
    PRIMARY KEY (fileurl)
);

CREATE TABLE Adresses (
    shortname varchar(4),
    street varchar(255),
    campus varchar(1),
    nr varchar(4),
    PRIMARY KEY (shortname)
);

CREATE TABLE meta (
    setting varchar(255),
    val varchar(255),
    PRIMARY KEY(setting)
);

CREATE TABLE OSMBuildings (
    id Integer,
    adress varchar(4),
    descript varchar(252),
    PRIMARY KEY (id),
    FOREIGN KEY (adress) REFERENCES Adresses(shortname),
    FOREIGN KEY (descript) REFERENCES Descript(fileurl)
);

INSERT INTO meta (setting,val) VALUES ('version',1);