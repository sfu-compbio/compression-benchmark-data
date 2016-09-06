#!/usr/bin/env python
# coding=utf8
# 786

import re, os, sys
import collections
import numpy as np
import pandas as pd

import tools, plot

# Constants
SAMPLES = [ {  
		'sample': 'SRR554369',
		'paired': True,
		'coverage': 25,
		'species': 'P.aeruginosa',
		'platform': 'Illumina GAIIx',
		'bases': [ 165156400, 165156400 ],
		'read_size': [ 100, 100 ]
	}, {  
		'sample': 'SRR327342',
		'paired': True,
		'coverage': 80,
		'species': 'S.cerevisiae',
		'platform': 'Illumina GAII',
	}, {  
		'sample': 'MH0001_081026_clean',
		'paired': True,
		'coverage': 'Unknown',
		'species': 'Human Gut Microbiome',
		'platform': 'Illumina GAII',
	}, {  
		'sample': 'SRR1284073',
		'paired': False,
		'coverage': 140,
		'species': 'E.coli',
		'platform': 'PacBio',
	}, {  
		'sample': 'SRR870667',
		'paired': True,
		'coverage': 20,
		'species': 'T.cacao',
		'platform': 'Illumina GAIIx',
	}, {  
		'sample': 'ERR174310',
		'paired': True,
		'coverage': 7,
		'species': 'H.Sapiens',
		'platform': 'Illumina HiSeq 2000',
	}, {  
		'sample': 'ERP001775',
		'paired': True,
		'coverage': 120,
		'species': 'H.Sapiens',
		'platform': 'Illumina HiSeq 2000',
	}, {  
		'sample': 'MiSeq_Ecoli_DH10B_110721_PF',
		'paired': True,
		'coverage': 420,
		'species': 'E.coli',
		'platform': 'Illumina MiSeq'
	}, {  
		'sample': '9827_2#49',
		'paired': True,
		'coverage': 2,
		'species': 'H.sapiens',
		'platform': 'Illumina HiSeq 2000'
	}, {  
		'sample': 'sample-2-10_sorted',
		'paired': False,
		'coverage': 0.6,
		'species': 'H.sapiens',
		'platform': 'IonTrorent',
	}, {  
		'sample': 'NA12878_S1',
		'paired': True,
		'coverage': 50,
		'species': 'H.sapiens',
		'platform': 'Illumina HiSeq 2000'
	}, {  
		'sample': 'NA12878.pacbio.bwa-sw.20140202',
		'paired': False,
		'coverage': 15,
		'species': 'H.sapiens',
		'platform': 'PacBio'
	}, {  
		'sample': 'HCC1954.mix1.n80t20',
		'paired': True,
		'coverage': 30,
		'species': 'H.sapiens',
		'platform': 'Illumina-like (Cancer cell line)',
	}, {  
		'sample': 'dm3PacBio',
		'paired': True,
		'coverage': 75, 
		'species': 'D.melangoster',
		'platform': 'PacBio'
	}, {  
		'sample': 'K562_cytosol_LID8465_TopHat_v2',
		'paired': True,
		'coverage': 6,
		'species': 'H.sapiens',
		'platform': 'Illumina RNASeq'
	},
]
THREADS = [1, 4, 8]

# Parsing

def get_fields(tool_name, sample, directory, file_type='sam', file_id=1):
	result = collections.defaultdict(int)
	function_name = tool_name

	if file_type == 'sam':
		if 'deez' in tool_name:
			log = directory + '/log/1.{tool}.{thread}.cmp'
		elif 'quip' in tool_name:
			log = directory + '/log/1.{tool}.{thread}.cmp'
		elif 'tsc' in tool_name:
			log = directory + '/log/1.{tool}.1.cmp'
		elif 'scramble' in tool_name:
			log = directory + '/other/1.{tool}.size'
		elif 'cramtools' in tool_name:
			log = directory + '/other/1.{tool}.size'
		elif 'pigz' in tool_name:
			log = directory + '/other/1.sam.size'
		elif 'sam_comp' in tool_name:
			log = directory + '/other/1.sam_comp.size'
		elif 'pbzip2' in tool_name:
			log = directory + '/other/1.sam.size'
		elif 'samtools' in tool_name:
			log = directory + '/other/1.bam.size'
		elif 'raw' in tool_name:
			log = directory + '/other/1.sam.size'
		else:	
			return result
	elif file_type == 'fastq':
		if 'dsrc' in tool_name:
			log = directory + '/log/{id}.{tool}.{thread}.cmp'
		elif 'fqzcomp' in tool_name:
			log = directory + '/log/{id}.{tool}.{thread}.cmp'
		elif 'quip' in tool_name:
			log = directory + '/log/{id}.{tool}.{thread}.cmp'
		elif 'slimfastq' in tool_name:
			log = directory + '/log/{id}.{tool}.{thread}.cmp'
		elif 'fastqz' in tool_name:
			log = directory + '/other/{id}.fastqz.size'
		elif 'pigz' in tool_name:
			log = directory + '/other/{id}.fastq.size'
		elif 'pbzip2' in tool_name:
			log = directory + '/other/{id}.fastq.size'
		elif 'beetl' in tool_name:
			log = directory + '/other/{id}.fastq.size'
		elif 'kic' in tool_name:
			log = directory + '/other/{id}.kic.size'
		elif 'leon' in tool_name:
			log = directory + '/other/{id}.leon.size'
		elif 'scalce-single' in tool_name:
			log = directory + '/other/1.scalce-single.size'
			function_name = 'scalce_single'
		elif 'scalce' in tool_name:
			log = directory + '/other/1.scalce.size'
		elif 'sra' in tool_name:
			log = directory + '/other/1.sra.size'
		elif 'kpath' in tool_name:
			log = directory + '/other/1.kpath.size'
		elif 'orcom' in tool_name:
			log = directory + '/other/1.orcom.size'
		elif 'lfqc' in tool_name:
			log = directory + '/other/1.lfqc.size'
		elif 'lw-fqzip' in tool_name:
			log = directory + '/other/1.lwfqzip.size'
			function_name = 'lwfqzip'
		elif 'raw' in tool_name:
			log = directory + '/other/{id}.fastq.size'
		else:
			return result
	else:
		return result

	# find the first threading mode available
	for t in THREADS:
		fn = log.format(id=file_id, tool=tool_name, thread=t)
		if os.path.exists(fn):
			log = fn
			break

	# remove mode suffix
	function_name = function_name.split('-')[0]
	function = getattr(tools, 'get_' + function_name)
	try:
		with open(log) as f:
			for line in f: function(result, line)
	except: # Exception as e:
		#print log, e, traceback.print_exc()
		pass
	return result

def process_sample(sample, directory):
	file_type = 'fastq' if 'fastq' in directory else 'sam'
	print 'Detected', file_type

	df = pd.DataFrame()
	i = 1
	while os.path.isfile(directory + '/other/{}.{}.size'.format(i, file_type)):
		data = get_fields('raw', sample, directory, file_type, i)
		data.update({
			'tool': 'raw',
			'sample': sample,
			'fileno': i,
			'threads': 1,
		})
		i += 1
		df = df.append(data, ignore_index=True)
	
	with open(directory + '/benchmark.log') as f:
		threads = 1
		data = {}
		for l in f:
			# thread count
			res = re.search('\+\s+(.+) with (\d+) threads\s+\+', l)
			if res is not None:
				threads = int(res.group(2))
			
			# tool name
			res = re.search('#\s+(\S+)\s+#', l)
			if res is not None:
				if 'command' in data:
					df = df.append(data, ignore_index=True)
				data = {
					'sample': sample,
					'threads': threads,
					'tool': res.group(1),
					'fileno': 1,
				}
				data.update(get_fields(data['tool'], sample, directory, file_type, data['fileno']))
				p = 'd'
			if file_type == 'fastq':
				res = re.search('>>> (.+) .File (\d+)', l)
				if res is None:
					res = re.search('>>> (.+)_(\d+)', l)
				if res is not None:
					if 'command' in data:
						df = df.append(data, ignore_index=True)
					data['fileno'] = int(res.group(2))
					data.update(get_fields(data['tool'], sample, directory, file_type, data['fileno']))
					p = 'd'

			# success status
			res = re.search('\*\*\* ([A-Z]+) \*\*\*', l)
			if res is not None:
				p = 'd' if p == '' else ''
				key = 'status'
				if p != '': key = p + '_' + key
				data[key] = res.group(1) == 'OK'

			# other fields
			res = re.search('^\s+(Command):\s+(.+)\s*', l)
			if res is None:
				res = re.search('^\s+(.+?):\s+\S+\s+\((\S+) ms\)', l)
			if res is None:
				res = re.search('^\s+(.+?):\s+\S+\s+\((\S+) bytes\)', l)
			if res is None:
				res = re.search('^\s+(.+?):\s+(\S+)\s*', l)
			if res is not None and res.group(1) != 'Free space':
				key = res.group(1).lower().replace(' ', '').split('(')[0]
				if p != '': key = p + '_' + key
				data[key] = res.group(2)
	
	if 'command' in data:
		df = df.append(data, ignore_index=True)

	for idx, row in df[['fileno','tool']].drop_duplicates().iterrows():
		fno, tool = int(row.fileno), row.tool
		fp = directory + '/diff/{}.{}.cmp'.format(fno, tool)
		if not os.path.exists(fp):
			# print 'Cannot locate ', fp, '-- ignoring it'
			continue

		cmp_equal = False
		file_equal = False
		comment_equal = True
		mismatches = {}
		with open(fp) as f:
			for l in f:
				l = l.strip()
				
				res = re.search('Equal cmp', l)			
				if res is not None:
					cmp_equal = True
				
				if l == 'Equal':
					file_equal = True

				res = re.search('[<>] (\S+)\s+(\d+)', l)
				if res is not None:
					mismatches[res.group(1)] = res.group(2)

				res = re.search('(\S+)\s+(\d+) lines$', l)
				if res is not None:
					mismatches[res.group(1)] = res.group(2)
				
				res = re.search('Comments\s+not equal', l)
				if res is not None:
					comment_equal = False
				
				res = re.search('(\S+)\s+(\d+) lines unequal', l)
				if res is not None:
					mismatches[res.group(1)] = res.group(2)

				res = re.search('(\S+)\s+(\d+) missing,\s+(\d+) extra,\s+(\d+) unequal', l)
				if res is not None:
					mismatches[res.group(1)] = '/'.join([res.group(i) for i in range(2,5)])

		if 'ORIG' in mismatches and mismatches['COPY'] == mismatches['ORIG']:
			del mismatches['COPY']
			del mismatches['ORIG']
		if len(mismatches) == 0 or cmp_equal:
			file_equal = True

		# Binary... Equal... Comments...
		df.ix[df.tool == tool, 'eq_file'] = file_equal
		df.ix[df.tool == tool, 'eq_cmp'] = cmp_equal
		if file_type == 'sam':
			df.ix[df.tool == tool, 'eq_comment'] = comment_equal
		for k, v in mismatches.iteritems():
			df.ix[df.tool == tool, 'eq_' + k.lower()] = v

	return df

def get_table(directory, force=False):
	data = pd.DataFrame()
	file_type = 'fastq' if 'fastq' in directory else 'sam'
	ref_tool = 'samtools' if file_type == 'sam' else 'pigz'

	pickle = 'cache/{}.pickle'.format(file_type)
	if not force and os.path.exists(pickle):
		data = pd.read_pickle(pickle)
		return data
	else:
		for sample in os.listdir(directory)[:]:
			df = process_sample(sample, directory + '/' + sample)
			data = pd.concat([data, df], ignore_index=True)

	data = data.replace({'?': np.nan})
	data = data.apply(lambda x: pd.to_numeric(x, errors='ignore'))

	data['sample'] = data['sample'].replace({'.bam': ''}, regex=True)
	data = data.apply(lambda x: pd.to_numeric(x, errors='ignore'))

	# print data[data.tool=='raw'][['sample']]
	data = data.merge(pd.DataFrame(SAMPLES), on='sample')

	if file_type == 'fastq':
		data['fullsample'] = data['sample']
		data['sample'] = data['sample'] + '_' + (data['fileno']).map(int).map(str)

		grouped = data.groupby(['fullsample', 'tool', 'threads'])
		func = {c: np.sum for c in ['aux', 'size', 'rname', 
											'qual', 'seq', 'walltime', 'user', 
											'sys', 'real', 'records', 'memory', 
											'd_sys', 'd_user', 'd_real', 
											'd_walltime', 'd_size']}
		func.update({c: np.max for c in ['memory', 'd_memory']})
		func.update({c: np.min for c in ['status', 'd_status']})
		combined = grouped.aggregate(func).reset_index()
		combined['sample'] = combined['fullsample']
		data = pd.concat([data, combined], ignore_index=True)

	for s in data['sample']:
		mask = (data['sample'] == s)
		ref = data.loc[(data.tool == ref_tool) & (data.threads == 1) & mask]
		
		# try:
		data.loc[mask, 'walltime_ratio'] = data.walltime / ref.iloc[0].walltime
		data.loc[mask, 'd_walltime_ratio'] = data.d_walltime / ref.iloc[0].d_walltime

		# fixes
		ref = data.loc[mask & (data.tool == 'sra')]
		data.loc[mask & (data.tool == 'sra'), 'size'] = ref['aux']
		ref = data.loc[mask & (data.tool == 'beetl')]
		data.loc[mask & (data.tool == 'beetl'), 'seq'] = ref['size']
		ref = data.loc[mask & (data.tool == 'mince-single')]
		data.loc[mask & (data.tool == 'mince-single'), 'seq'] = ref['size']
		ref = data.loc[mask & (data.tool == 'mince')]
		data.loc[mask & (data.tool == 'mince'), 'seq'] = ref['size']

	mask = data['status'] == False
	data = data[data['tool'] != 'sra']
	data.loc[mask, data.columns.isin(['size', 'd_size', 'seq', 'pe', 'aux', 'rname', 'qual'])] = None
	data.loc[mask, ['d_status'] + [x for x in data.columns if x[:2] == 'eq']] = False

	data.to_pickle(pickle)
	return data

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print 'Usage: print.py <filetype> <mode>'
		exit(1)

	filetype, mode = sys.argv[1], sys.argv[2]

	data = get_table('../data/{}'.format(filetype), False)
	tools = data['tool'].drop_duplicates()
	samples = data['sample'].drop_duplicates()

	if mode == 'json':
		print data.to_json(orient='records')
		exit(0)

	if mode == 'plot':
		if filetype == 'fastq':
			tools = ['pigz', 'pbzip2', 'dsrc', 'dsrc-m2', 'fqzcomp', 'fqzcomp-extra', 'slimfastq', 'fqc', 'scalce-single', 'lw-fqzip', 'quip', 'leon', 'kic']
			samples = ['SRR554369_1', 'SRR327342_1', 'MH0001_081026_clean_1', 'SRR1284073_1', 'SRR870667_1', 'ERR174310_1', 'ERP001775']
		else:
			tools = ['pigz', 'pbzip2', 'samtools', 'picard', 'sambamba', 'cramtools', 'scramble', 'scramble-noref', 'scramble-bzip2', 'deez', 'deez-qual', 'tsc', 'quip', 'quip-ref']
			samples = ['MiSeq_Ecoli_DH10B_110721_PF',  '9827_2#49',  'sample-2-10_sorted',  'K562_cytosol_LID8465_TopHat_v2', 'dm3PacBio',  'NA12878.pacbio.bwa-sw.20140202',  'HCC1954.mix1.n80t20',  'NA12878_S1']
		plot.generate_plot(data, tools, samples, filetype)
		exit(0)

	if mode == 'paired':
		samples = samples[~samples.str.contains('_') & ~samples.str.contains('ERP') & ~samples.str.contains('SRR1')]
		
		columns_top = ['size', 'seq']
		columns = ['walltime_ratio', 'd_walltime_ratio']

		print 'Tool', '\t',
		for sample in samples:
			 print sample, '\t', '\t',
		print
		for tool in tools:
			print tool, 
			for i in xrange(2):
				print '\t',
				dy = data[(data.tool == tool)]
				for sample in samples:
					dz = dy[(dy['sample'] == sample) & (dy['size'].notnull())]
					f = np.nan
					if len(dz) > 0: 
						f = dz.ix[dz['threads'].argmin()][columns_top[i]]
					print '{:,.0f}'.format(f / 1e6), '\t',
					f = np.nan
					if len(dz) > 0: 
						f = dz.ix[dz['threads'].argmin()][columns[i]]
						if i == 1 and dz.ix[dz['threads'].argmin()]['d_status'] != 1:
							f = np.nan
					print '{:.2f}'.format(f), '\t',
				print
		exit(0)
		
	if filetype == 'fastq':
		samples = samples[(samples.str.contains('_1') & ~samples.str.contains('ERP')) | (samples == ('ERP001775'))]

	if mode in ['final', 'main']:
		columns_top = ['size', 'seq']
		columns = ['walltime_ratio', 'd_walltime_ratio']

		print 'Tool', '\t',
		for sample in samples:
			 print sample, '\t', '\t',
		print
		for tool in tools:
			print tool, 
			for i in xrange(2):
				print '\t',
				dy = data[(data.tool == tool)]
				for sample in samples:
					dz = dy[(dy['sample'] == sample) & (dy['size'].notnull())]
					f = np.nan
					if len(dz) > 0: 
						f = dz.ix[dz['threads'].argmin()][columns_top[i]]
					if i == 0 or filetype == 'fastq':
						print '{:,.0f}'.format(f / 1e6),  
					print '\t',
					f = np.nan
					if len(dz) > 0: 
						f = dz.ix[dz['threads'].argmin()][columns[i]]
						if i == 1 and dz.ix[dz['threads'].argmin()]['d_status'] != 1:
							f = np.nan
					print '{:.2f}'.format(f), '\t',
				print
	elif mode in ['seq', 'qual', 'rname', 'aux']:
		print 'Tool', '\t',
		for sample in samples:
			print sample[:15], '\t', '\t',
		print
		for tool in tools:
			print tool, '\t',
			dy = data[(data.tool == tool)]
			raw = data[(data.tool == 'raw')]
			for sample in samples:
				dz = dy[(dy['sample'] == sample) & (dy[mode].notnull())]
				f, fr = np.nan, np.nan
				if filetype == 'sam' and mode == 'aux':
					dz = dy[(dy['sample'] == sample) & (dy[mode].notnull() | dy['pe'].notnull())].fillna(0)
					if len(dz) > 0:
						f = dz.ix[dz['threads'].argmin()]
						f = f[mode] + f['pe']
						fr = raw[raw['sample'] == sample]
						fr = fr[mode].fillna(0) + fr['pe'].fillna(0)
						fr = f / fr.iloc[0]
				elif len(dz) > 0:
					f = dz.ix[dz['threads'].argmin()][mode]
					fr = f / raw[raw['sample'] == sample][mode].iloc[0]
				f /= 1e6
				if f < 10:
					print '{:,.2f}'.format(f), '\t',
				else:
					print '{:,.0f}'.format(f), '\t',
				print '{:.2f}'.format(fr), '\t',
			print
	elif mode in ['time', 'mem']:
		columns = ['walltime_ratio', 'd_walltime_ratio']
		if mode == 'mem':
			columns = ['memory', 'd_memory']

		print 'Tool', '\t',
		for sample in samples:
			print sample, '\t' * (len(THREADS)), 
		print
		print 'Threads', '\t',
		for sample in samples:
			print '\t'.join(map(str, THREADS)), '\t',
		print
		for tool in tools:
			print tool, 
			for i in xrange(2):
				print '\t',
				dy = data[(data.tool == tool) & (data.status == 1)]
				for sample in samples:
					for th in THREADS:
						if th == 8 and sample in ['NA12878_S1', 'ERP001775']:
							continue
						dz = dy[(dy['sample'] == sample) & (dy['threads'] == th)]
						f = np.nan
						if len(dz[columns[i]]) > 0:
							f = dz[columns[i]].iloc[0]
							if i == 1 and dz.ix[dz['threads'].argmin()]['d_status'] != 1:
								f = np.nan
						print '{:,.2f}'.format(f), '\t',
				print
	else:
		print 'Mode {} not recognized'.format(mode)
