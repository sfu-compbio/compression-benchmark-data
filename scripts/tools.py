# 786

import re

def get_quip(ret, l):
	res = re.search("aux: (\d+)", l)
	if res is not None:
		ret['aux'] += int(res.group(1))

	res = re.search("id: (\d+)", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("seq: (\d+)", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	res = re.search("qual: (\d+)", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_sam_comp(ret, l):
	res = re.search("(\d+) .+AUX", l)
	if res is not None:
		ret['aux'] += int(res.group(1))

	res = re.search("(\d+) .+RNAME", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("(\d+) .+SEQ", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	res = re.search("(\d+) .+QUAL", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_tsc(ret, l):
	res = re.search("Aux\s+:\s+(\d+) \([. 0-9%]+\)$", l)
	if res is not None:
		ret['aux'] += int(res.group(1))

	res = re.search("Id\s+:\s+(\d+) \([. 0-9%]+\)$", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("Pair\s+:\s+(\d+) \([. 0-9%]+\)$", l)
	if res is not None:
		ret['pe'] += int(res.group(1))

	res = re.search("Nuc\s+:\s+(\d+) \([. 0-9%]+\)$", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	res = re.search("Qual\s+:\s+(\d+) \([. 0-9%]+\)$", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_deez(ret, l):
	res = re.search("Reference\s+([0-9,]+)", l)
	if res is not None:
		ret['seq'] += int(res.group(1).replace(',', ''))
	res = re.search("Sequences\s+([0-9,]+)", l)
	if res is not None:
		ret['seq'] += int(res.group(1).replace(',', ''))

	res = re.search("Read Names\s+([0-9,]+)", l)
	if res is not None:
		ret['rname'] += int(res.group(1).replace(',', ''))
	res = re.search("Qualities\s+([0-9,]+)", l)
	if res is not None:
		ret['qual'] += int(res.group(1).replace(',', ''))
	
	res = re.search("Paired End\s+([0-9,]+)", l)
	if res is not None:
		ret['pe'] += int(res.group(1).replace(',', ''))

	res = re.search("Flags\s+([0-9,]+)", l)
	if res is not None:
		ret['aux'] += int(res.group(1).replace(',', ''))
	res = re.search("Map. Quals\s+([0-9,]+)", l)
	if res is not None:
		ret['aux'] += int(res.group(1).replace(',', ''))
	res = re.search("Optionals\s+([0-9,]+)", l)
	if res is not None:
		ret['aux'] += int(res.group(1).replace(',', ''))

def get_scramble(ret, l):
	res = re.search("total size\s+(\d+).+ RN$", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("total size\s+(\d+).+ QS$", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

	for i in [ 'IN', 'SC', 'BB', 'BA', 'BS', 'FN', 'FC', 'FP', 'DL', 'AP', 'RI', 'RL', 'RS' ]:
		res = re.search("total size\s+(\d+).+ " + i + "$", l)
		if res is not None:
			ret['seq'] += int(res.group(1))
	res = re.search("Block content_id\s+37, total size\s+(\d+).+", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	for i in [ 'CF', 'NF', 'NS', 'NP', 'TS', 'MF' ]:
		res = re.search("total size\s+(\d+).+ " + i + "$", l)
		if res is not None:
			ret['pe'] += int(res.group(1))

	for i in [ "BF", "MQ", "TL" ]:
		res = re.search("total size\s+(\d+).+ " + i + "$", l)
		if res is not None:
			ret['aux'] += int(res.group(1))

	res = re.search("total size\s+(\d+).+ ([A-Z0-9a-z]{3})$", l)
	if res is not None:
		#print "adding", res.group(2)
		ret['aux'] += int(res.group(1))

def get_cramtools(ret, l):
	res = re.search("total size\s+(\d+).+ RN$", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("total size\s+(\d+).+ QS$", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

	res = re.search("Block CORE\s+, total size\s+(\d+)$", l)
	if res is not None:
		ret['seq'] += int(res.group(1))
	res = re.search("total size\s+(\d+).+BA IN SC$", l)
	if res is not None:
		ret['seq'] += int(res.group(1))
	
	res = re.search("total size\s+(\d+).+TS NP$", l)
	if res is not None:
		ret['pe'] += int(res.group(1))

	res = re.search("total size\s+(\d+).+ ([A-Z0-9a-z]{3}) ", l)
	if res is not None:
		ret['aux'] += int(res.group(1))

def get_samtools(ret, l):
	res = re.search("QUAL:\s+(\d+)", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

	res = re.search("BIN:\s+(\d+)", l)
	if res is not None:
		ret['file'] += int(res.group(1))

	for i in [ 'QNAME', 'RNAMELEN' ]:
		res = re.search(i + ":\s+(\d+)", l)
		if res is not None:
			ret['rname'] += int(res.group(1))

	for i in [ 'REF', 'POS', 'SEQLEN', 'SEQ', 'CIGAR', 'CIGARLEN' ]:
		res = re.search(i + ":\s+(\d+)", l)
		if res is not None:
			ret['seq'] += int(res.group(1))

	for i in [ 'TLEN', 'PREF', 'PNEXT' ]:
		res = re.search(i + ":\s+(\d+)", l)
		if res is not None:
			ret['pe'] += int(res.group(1))

	for i in [ 'MAPQ', 'OF', 'FLAG' ]:
		res = re.search(i + ":\s+(\d+)", l)
		if res is not None:
			ret['aux'] += int(res.group(1))

def get_sam(ret, l, f):
	res = re.search("QUAL:\s+(\d+)\s+(\d+)\s+(\d+)", l)
	if res is not None:
		ret['qual'] += int(res.group(f))

	res = re.search("HEAD:\s+(\d+)\s+(\d+)\s+(\d+)", l)
	if res is not None:
		ret['file'] += int(res.group(f))

	for i in [ 'QNAME', 'RNAME' ]:
		res = re.search(i + ":\s+(\d+)\s+(\d+)\s+(\d+)", l)
		if res is not None:
			ret['rname'] += int(res.group(f))

	for i in [ 'REF', 'POS', 'SEQ', 'CIGAR' ]:
		res = re.search(i + ":\s+(\d+)\s+(\d+)\s+(\d+)", l)
		if res is not None:
			ret['seq'] += int(res.group(f))

	for i in [ 'TLEN', 'PNEXT', 'RNEXT' ]:
		res = re.search(i + ":\s+(\d+)\s+(\d+)\s+(\d+)", l)
		if res is not None:
			ret['pe'] += int(res.group(f))

	for i in [ 'MAPQ', 'OF', 'FLAG', 'AUX' ]:
		res = re.search(i + ":\s+(\d+)\s+(\d+)\s+(\d+)", l)
		if res is not None:
			ret['aux'] += int(res.group(f))

	res = re.search("SIZE:\s+(\d+)", l)
	if res is not None:
		ret['size'] += int(res.group(1))

	for i in [ 'RECORDS', 'LINES' ]:
		res = re.search(i + ":\s+(\d+)", l)
		if res is not None:
			ret['records'] += int(res.group(1))

def get_raw(ret, l): 
	return get_sam(ret, l, 1)

def get_pigz(ret, l): 
	return get_sam(ret, l, 2)

def get_pbzip2(ret, l): 
	return get_sam(ret, l, 3)

def get_dsrc(ret, l):
	res = re.search("TAG:\s+(\d+)", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("DNA:\s+(\d+)", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	res = re.search("QUA:\s+(\d+)", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_fqzcomp(ret, l):
	res = re.search("Names.+\d+ ->\s+(\d+) \(.+\)", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("Bases.+\d+ ->\s+(\d+) \(.+\)", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	res = re.search("Quals.+\d+ ->\s+(\d+) \(.+\)", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_scalce(ret, l):
	res = re.search("(\d+) .+scalce_.\.scalcen", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("(\d+) .+scalce_.\.scalcer", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	res = re.search("(\d+) .+scalce_.\.scalceq", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_scalce_single(ret, l):
	res = re.search("(\d+) .+scalce-single_.\.scalcen", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("(\d+) .+scalce-single_.\.scalcer", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	res = re.search("(\d+) .+scalce-single_.\.scalceq", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_fastqz(ret, l):
	res = re.search("(\d+) .+\.fastqz\.fxh\.zpaq", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("(\d+) .+\.fastqz\.fxb\.zpaq", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	res = re.search("(\d+) .+\.fastqz\.fxq\.zpaq", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_kic(ret, l):
	res = re.search("(\d+) .+\.kic.name", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("(\d+) .+\.kic.seq", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	res = re.search("(\d+) .+\.kic.qual", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_beetl(ret, l):
	ret['seq'] = ret['size']

def get_mince(ret, l):
	res = re.search("(\d+) .+\.lz", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

def get_orcom(ret, l):
	res = re.search("(\d+) .+\.orcom\.c.+", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

def get_kpath(ret, l):
	res = re.search("(\d+) .+\.kpath\.(bittree|counts|enc|flipped|ns)", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

def get_lfqc(ret, l):
	res = re.search("(\d+) \d{4}-\d{2}-\d{2}.+_name_", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("(\d+) \d{4}-\d{2}-\d{2}.+_data_", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	res = re.search("(\d+) \d{4}-\d{2}-\d{2}.+_qual_", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_slimfastq(ret, l):
	res = re.search("REC comp size: (\d+)", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("GEN comp size: (\d+)", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	res = re.search("QLT comp size: (\d+)", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_leon(ret, l):
	res = re.search("Headers compressed size: (\d+)", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	res = re.search("Compression rate: [0-9.]+\s+\((\d+)\)", l)
	if res is not None:
		ret['seq'] += int(res.group(1))

	res = re.search("(\d+) .+\.qual", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_lwfqzip(ret, l):
	res = re.search("(\d+) \d{4}-\d{2}-\d{2}.+.meta.txt.lz", l)
	if res is not None:
		ret['rname'] += int(res.group(1))

	for i in [ 'pos', 'cigar', 'cor', 'add' ]:
		res = re.search("(\d+) \d{4}-\d{2}-\d{2}.+." + i + ".txt.lz", l)
		if res is not None:
			ret['seq'] += int(res.group(1))

	res = re.search("(\d+) \d{4}-\d{2}-\d{2}.+.qs.txt.lz", l)
	if res is not None:
		ret['qual'] += int(res.group(1))

def get_sra(ret, l):
	res = re.search("Content-Length: (\d+)", l)
	if res is not None:
		ret['aux'] += int(res.group(1))

