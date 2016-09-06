# [HTS Compression Benchmark Suite](https://github.com/sfu-compbio/compression-benchmark) <br> Data Repository

A searchable database of all results contained here is available at https://sfu-compbio.github.io/compression-benchmark-data/.

### Contributing

We are accepting pull requests containing benchmarks of the tools not included here. Please make sure to benchmark the reference tools as well (pigz or Samtools), and to follow the directory structure as outlined below.

### File Structure

Within `data` directory, you will find `fastq` and `sam` directories holding benchmarking logs for FASTQ and SAM/BAM samples, respectively.

Each sample is organized as follows:

- `benchmark.log`: contains benchmarking information (running times, memory usage etc.)

- `log/`: non-empty logs produced by compression tools

	- `<file>.<tool>.<threads>.<mode>`: log of tool `<tool>` in mode `<mode>`, ran on file `<file>` with `<threads>` threads

		- `<file>` is the number of file in input data set. For SAM/BAM files, it is always 1. For FASTQ files, it is the number of file in the library (for `ERR174310_2.fastq`, `<file>` will be 2)

		- `<mode>` is `cmp` for compression, and `dec` for decompression.

		- `<tool>` is the name of the tool.

		- `<threads>` is the number of threads which particular tool used.

	**Example:** `1.orcom.4.cmp` in `SRR870667/log/` represents the output of Orcom's compression mode which was ran on `SRR870667_1.fastq` with 4 threads.

- `diff/`: differences between the original and decompressed files

	- `<file>.<tool>.cmp`: difference between outputs of tool `<tool>` and original file `<file>`

	> **Note:** diff files were produced by our comparison tools available [here](https://github.com/sfu-compbio/compression-benchmark).


- `other/`: sizes of specific fields within the archive (e.g. size of quality scores within a compressed archive)

	- `<file>.<tool>.size`: size of various fields produced by tool `<tool>` on file `<file>`

		- `fastq.size`, `bam.size` and `sam.size` files were produced by `columnar` tool available [here](https://github.com/sfu-compbio/compression-benchmark). They also contain sizes of each column with Gzip and bzip2 applied on them.
		- `scramble.size` and `cram.size` were produced by `cram_size` tool found in [Staden Package](https://sourceforge.net/projects/staden/).
		- `lfqc.size` and `lw-fqzip.size` are output of `tar tvf` command on final compressed files.
		- `sra.size` are sizes of NCBI SRA archives obtained via 	`curl`. We could not run NCBI SRA software ourselves, so we just measured the size of SRA files stored online. Note that this size includes both paired-ends.

	> **Note:** For some tools, there was no need to produce special `size` file since all necessary information was available in their compression log found in `log/` directory. Please consult `scripts/print.py` and `scripts/tools.py` script for details where to find such information.

### Utility scripts

All of there are available in `scrips` directory.

- `print.py`: prints the tables as found in paper and on the website.

	Usage: `print.py <file-type> <mode>`, where `<file-type>` is either `fastq` or `sam`, and `<mode>` is:
	- **Main paper**:
		- `main`: table from the main paper
	- **Supplementary tables:**
		- `seq`: supplementary table 1(a) / 3(a)
		- `qual`: supplementary table 1(b) / 3(b)
		- `rname`: supplementary table 1(c) / 3(c)
		- `aux`: supplementary table 3(d)
		- `time`: supplementary table 2(a) / 4(a)
		- `mem`: supplementary table 2(b) / 4(b)
		- `paired`: supplementary table 5

		> **Note:** `scalce` and `mince` are supposed to be used only in `paired` table. Every other table should use `scale-single` and `mince-single` because those tables only show single-end results.

	- **Supplementary figures:**
		- `plot`: produces the supplementary figure 1
	- **Website:**
		- `json`: website JSON dump

### Website

Website source code is available in `docs/` directory. It is based upon [Bootstrap Table Project](https://github.com/wenzhixin/bootstrap-table).

### Miscellanea

ADAM and Goby results (supplementary table from section 4.2) are located [here](data/sam/MiSeq_Ecoli_DH10B_110721_PF.bam/benchmark-extra.log). Random access results (supplementary table from section 5.3.2) are located [here](data/random-access.log).

### Help and contact info

Please check out our main repository [here](https://github.com/sfu-compbio/compression-benchmark) for contact info.

### License

[MIT License](LICENSE)
