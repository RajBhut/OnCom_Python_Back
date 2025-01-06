/*
  Warnings:

  - The primary key for the `Problem_code` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- AlterTable
ALTER TABLE "Problem_code" DROP CONSTRAINT "Problem_code_pkey",
ADD CONSTRAINT "Problem_code_pkey" PRIMARY KEY ("id", "language");
