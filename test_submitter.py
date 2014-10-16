import unittest

import submit_jobs


class TestSubmitter(unittest.TestCase):
    def setUp(self):
        self.job = """
#!/bin/bash -l
#SBATCH -J trinity{{ job_name }}
#SBATCH -o output_%j.txt
#SBATCH -e errors_%j.txt
#SBATCH -t 120:00:00
#SBATCH -n 1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=8000
#SBATCH -p longrun

#SBATCH --mail-type=ALL
#SBATCH --mail-user=mycalesis@gmail.com


module load biokit

/homeappl/home/pena/appl_taito/trinityrnaseq_r20140717/Trinity --seqType fq --JM 24G {{ input_files }} --CPU 16 --min_kmer_cov 5 --output trinity_run_out

"""

    def test_get_list_of_folders(self):
        result = submit_jobs.get_list_of_folders()
        expected = "akito_adhemarius"
        self.assertEqual(expected, result[0])

    def test_get_fastq_files(self):
        folder = "akito_zeuzerodes"
        result = submit_jobs.get_fastq_files(folder)
        expected = ["SR_1.fastq", "SR_2.fastq"]
        self.assertEqual(expected, result)

    def test_generate_job_text(self):
        fastq_files = ["SR_1.fastq", "SR_2.fastq"]
        folder = "akito_zeuzerodes"
        job_text = submit_jobs.generate_job_text(self.job, fastq_files, folder)

        result = job_text.split("\n")
        expected = "#SBATCH -J trinity_zeuzerodes"

        self.assertEqual(expected, result[2])



