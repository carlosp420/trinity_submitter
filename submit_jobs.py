import os
import glob
import re


# create job.sh file for each folder
job = """
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


def get_list_of_folders():
    folders = []
    append = folders.append

    for i in glob.glob("akito_*"):
        if os.path.isdir(i):
            append(i)

    return folders


def get_fastq_files(folder):
    # our files are single or pair ended? _1. _2. ?
    filenames = glob.glob(os.path.join(folder, "*fastq"))
    new_filenames = [re.sub(folder + "/", "", i) for i in filenames]
    return new_filenames


def generate_job_text(job, fastq_files, folder):
    my_folder = folder.replace("akito", "")
    mod_job = job.replace("{{ job_name }}", my_folder)
    return mod_job


def write_job_file(folders):
    for folder in folders:
        fastq_files = get_fastq_files(folder)
        job_text = generate_job_text(job, fastq_files, folder)
# submit job

# count number of fastq files (single? paired?
