/*
  Warnings:

  - The primary key for the `Problem_code` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- DropIndex
DROP INDEX "Problem_code_problemId_language_key";

-- AlterTable
ALTER TABLE "Problem_code" DROP CONSTRAINT "Problem_code_pkey",
ADD CONSTRAINT "Problem_code_pkey" PRIMARY KEY ("problemId", "language");
