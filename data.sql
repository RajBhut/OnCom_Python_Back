-- Enum: Language
CREATE TYPE "Language" AS ENUM (
  'PYTHON',
  'C',
  'CPP',
  'JAVA',
  'JAVASCRIPT'
);

-- Enum: Difficulty
CREATE TYPE "Difficulty" AS ENUM (
  'EASY',
  'MEDIUM',
  'HARD'
);

-- Table: User
CREATE TABLE "User" (
  id SERIAL PRIMARY KEY,
  email VARCHAR NOT NULL UNIQUE,
  password VARCHAR NOT NULL,
  name VARCHAR,
  createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Problem
CREATE TABLE "Problem" (
  id SERIAL PRIMARY KEY,
  title VARCHAR NOT NULL,
  description TEXT NOT NULL,
  difficulty "Difficulty" NOT NULL,
  creatorId INT NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
  tags TEXT[] NOT NULL,
  edgedata TEXT DEFAULT '',
  nodedata TEXT DEFAULT ''
);

-- Table: Problem_code
CREATE TABLE "Problem_code" (
  id SERIAL UNIQUE,
  function TEXT NOT NULL,
  language "Language" NOT NULL,
  testcases TEXT NOT NULL,
  checker TEXT NOT NULL,
  problemId INT NOT NULL REFERENCES "Problem"(id) ON DELETE CASCADE,
  userId INT NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
  createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (problemId, language)
);

-- Table: Submission
CREATE TABLE "Submission" (
  id SERIAL PRIMARY KEY,
  code TEXT NOT NULL,
  language "Language" NOT NULL,
  status VARCHAR NOT NULL,
  userId INT NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
  problemId INT NOT NULL REFERENCES "Problem"(id) ON DELETE CASCADE,
  score INT NOT NULL,
  createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Contest
CREATE TABLE "Contest" (
  id SERIAL PRIMARY KEY,
  title VARCHAR NOT NULL,
  description TEXT NOT NULL,
  creatorId INT NOT NULL REFERENCES "User"(id) ON DELETE CASCADE
);

-- Table: ContestProblem
CREATE TABLE "ContestProblem" (
  id SERIAL PRIMARY KEY,
  contestId INT NOT NULL REFERENCES "Contest"(id) ON DELETE CASCADE,
  problemId INT NOT NULL REFERENCES "Problem"(id) ON DELETE CASCADE
);

-- Table: ContestParticipant
CREATE TABLE "ContestParticipant" (
  id SERIAL PRIMARY KEY,
  contestId INT NOT NULL REFERENCES "Contest"(id) ON DELETE CASCADE,
  userId INT NOT NULL REFERENCES "User"(id) ON DELETE CASCADE,
  rank INT
);
