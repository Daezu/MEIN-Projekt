CREATE SEQUENCE user_id_seq INCREMENT BY 50;

CREATE TABLE "tbl_user" (
    userid BIGINT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL
);
CREATE TABLE "tbl_symptom" (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    userid BIGINT,
    name VARCHAR(255) NOT NULL,
    severity VARCHAR(255),
    first_occurrence TIMESTAMP,
    last_occurrence TIMESTAMP,

    PRIMARY KEY(timestamp, userid),
    FOREIGN KEY(userid) REFERENCES tbl_user(userid)
);
CREATE TABLE "tbl_medicine" (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    userid BIGINT,
    name VARCHAR(255) NOT NULL,
    dose VARCHAR(255),
    first_intake TIMESTAMP,
    last_intake TIMESTAMP,

    PRIMARY KEY(timestamp, userid),
    FOREIGN KEY(userid) REFERENCES tbl_user(userid)
);