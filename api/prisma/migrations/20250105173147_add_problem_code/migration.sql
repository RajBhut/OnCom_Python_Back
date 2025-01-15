/*
  Warnings:

  - The primary key for the `Problem_code` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - A unique constraint covering the columns `[problemId,language]` on the table `Problem_code` will be added. If there are existing duplicate values, this will fail.

*/
-- AlterTable
ALTER TABLE "Problem_code" DROP CONSTRAINT "Problem_code_pkey",
ADD CONSTRAINT "Problem_code_pkey" PRIMARY KEY ("id");

-- CreateIndex
CREATE UNIQUE INDEX "Problem_code_problemId_language_key" ON "Problem_code"("problemId", "language");
