import os
import glob
import re
import subprocess
import sys


# create job.sh file for each folder
job = """#!/bin/bash -l
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
    print(">>>>filenames", filenames)
    if len(filenames) < 1:
        return None
    new_filenames = [re.sub(folder + "/", "", i) for i in filenames]
    return new_filenames


def generate_job_text(job, fastq_files, folder):
    my_folder = folder.replace("akito", "")
    mod_job = job.replace("{{ job_name }}", my_folder)

    if len(fastq_files) > 1:
        input_files = "--left " + fastq_files[0] + " --right " + fastq_files[1]
        mod_job2 = mod_job.replace("{{ input_files }}", input_files)
    else:
        input_files = "--single " + fastq_files[0]
        mod_job2 = mod_job.replace("{{ input_files }}", input_files)
    return mod_job2


def write_job_file(folders):
    for folder in folders:
        print(">folder %s" % folder)
        fastq_files = get_fastq_files(folder)
        if fastq_files is not None:
            job_text = generate_job_text(job, fastq_files, folder)
            job_file = os.path.join(folder, "job.sh")
            with open(job_file, "w") as writer:
                writer.write(job_text)

            # submit job
            """
            cmd = "sbatch " + job_file
            p = subprocess.check_call(cmd, shell=True)
            if p != 0:
                print(">>> Error, couldnt submit job: %s" % job_file)
                sys.exit(1)
            """



folders = get_list_of_folders()
print(folders)
write_job_file(folders)

