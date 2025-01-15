/*
  Warnings:

  - Changed the type of `difficulty` on the `Problem` table. No cast exists, the column would be dropped and recreated, which cannot be done if there is data, since the column is required.
  - Changed the type of `language` on the `Submission` table. No cast exists, the column would be dropped and recreated, which cannot be done if there is data, since the column is required.
  - Added the required column `password` to the `User` table without a default value. This is not possible if the table is not empty.

*/
-- CreateEnum
CREATE TYPE "Language" AS ENUM ('PYTHON', 'C', 'CPP', 'JAVA', 'JAVASCRIPT');

-- CreateEnum
CREATE TYPE "Difficulty" AS ENUM ('EASY', 'MEDIUM', 'HARD');

-- AlterTable
ALTER TABLE "Problem" ADD COLUMN     "tags" TEXT[],
DROP COLUMN "difficulty",
ADD COLUMN     "difficulty" "Difficulty" NOT NULL;

-- AlterTable
ALTER TABLE "Submission" DROP COLUMN "language",
ADD COLUMN     "language" "Language" NOT NULL;

-- AlterTable
ALTER TABLE "User" ADD COLUMN     "password" TEXT NOT NULL;

-- CreateTable
CREATE TABLE "Problem_code" (
    "id" SERIAL NOT NULL,
    "function" TEXT NOT NULL,
    "language" "Language" NOT NULL,
    "testcases" TEXT NOT NULL,
    "checker" TEXT NOT NULL,
    "problemId" INTEGER NOT NULL,
    "userId" INTEGER NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Problem_code_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Problem_code_id_key" ON "Problem_code"("id");

-- CreateIndex
CREATE UNIQUE INDEX "Problem_code_problemId_language_key" ON "Problem_code"("problemId", "language");

-- AddForeignKey
ALTER TABLE "Problem_code" ADD CONSTRAINT "Problem_code_problemId_fkey" FOREIGN KEY ("problemId") REFERENCES "Problem"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Problem_code" ADD CONSTRAINT "Problem_code_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
