/// 786 

$(".nav-tabs a").click(function(e) {
	e.preventDefault();
	if ($(this).attr('href') == '#sam') {
		title = 'SAM/BAM';
		loc = 'data_sam.json';
	} else {
		title = 'FASTQ';
		loc = 'data_fastq.json';
	}

	$('#toolbar').text(title);
	$('.filter-show-clear').trigger('click')

	$('#table').bootstrapTable('showLoading');
	$.ajax({
		type: "GET",
		url: loc,
		dataType:"json",
		success : function(data) {
			$("select[class*='bootstrap-table-filter-control']").empty();
			$('#table').bootstrapTable('hideLoading');
			$('#table').data('url', loc)
			$('#table').bootstrapTable('load', data);
		}
	});
})

$('#table').bootstrapTable({
	search: true,
	toggle: 'table',
	toolbar: '#toolbar',
	showToggle: true,
	showColumns: true,
	showPaginationSwitch: true,
	pagination: true,
	pageSize: 20,
	pageList: [20, 50, 100, 'ALL'],
	showFooter: false,
	filterControl: true,
	columns: [
		[{
			title: 'Sample',
			align: 'center',
			colspan: 4,
		}, {
			field: 'tool',
			title: 'Tool',
			rowspan: 2,
			align: 'left',
			valign: 'center',
			sortable: true,
			formatter: formatTool,
			filterControl: 'select',
			filterStrictSearch: true,
		}, {
			field: 'threads',
			title: 'Threads',
			rowspan: 2,
			align: 'right',
			valign: 'center',
			sortable: true,
			filterControl: 'select',
		}, {
			field: 'size',
			title: 'Size (MB)',
			rowspan: 2,
			align: 'right',
			valign: 'center',
			sortable: true,
			formatter: formatSize,
			events: {
				'click .sizedetails': sizeDetails,
			},
			filterControl: 'input',
			customSearch: function(r,v) {
				y=parseInt(v)/1024./1024.;
				return isNaN(y)?true:rangeSearch(r,y)
			}
		}, {
			field: 'seq',
			title: 'Sequence size (MB)',
			rowspan: 2,
			align: 'right',
			valign: 'center',
			sortable: true,
			formatter: formatSize,
			filterControl: 'input',
			customSearch: function(r,v) {
				y=parseInt(v)/1024./1024.;
				return isNaN(y)?true:rangeSearch(r,y)
			},
			visible: false,
		}, {
			field: 'qual',
			title: 'Quality size (MB)',
			rowspan: 2,
			align: 'right',
			valign: 'center',
			sortable: true,
			formatter: formatSize,
			filterControl: 'input',
			customSearch: function(r,v) {
				y=parseInt(v)/1024./1024.;
				return isNaN(y)?true:rangeSearch(r,y)
			},
			visible: false,
		}, {
			field: 'rname',
			title: 'Read identifier size (MB)',
			rowspan: 2,
			align: 'right',
			valign: 'center',
			sortable: true,
			formatter: formatSize,
			filterControl: 'input',
			customSearch: function(r,v) {
				y=parseInt(v)/1024./1024.;
				return isNaN(y)?true:rangeSearch(r,y)
			},
			visible: false,
		}, {
			title: 'Compression Details',
			colspan: 3,
			align: 'center',
		}, {
			title: 'Decompression Details',
			colspan: 3,
			align: 'center',
		}, {
			title: 'Equal output',
			field: 'eq_file',
			align: 'center',
			rowspan: 2,
			sortable: true,
			formatter: formatBool,
		},],
		[{
			field: 'sample',
			title: 'Sample',
			sortable: true,
			filterControl: 'select',
		}, {
			field: 'species',
			title: 'Species',
			sortable: true,
			formatter: function(x) {
				return '<i>'+x+'</i>'
			},
			filterControl: 'select',
		}, {
			field: 'platform',
			title: 'Platform',
			sortable: true,
			filterControl: 'select',
		}, {
			field: 'coverage',
			title: 'Coverage (x)',
			sortable: true,
			filterControl: 'input',
			customSearch: rangeSearch
		}, {
			field: 'status',
			title: 'Succeeded',
			sortable: true,
			align: 'center',
			formatter: formatBool,
		}, {
			field: 'walltime_ratio',
			title: 'Time',
			sortable: true,
			align: 'right',
			formatter: formatTimeRatio,
			events: {
				'click .timedetails': timeDetails,
			},
			filterControl: 'input',
			customSearch: rangeSearch
		}, {
			field: 'memory',
			title: 'Memory (MB)',
			sortable: true,
			align: 'right',
			formatter: formatNumber,
			filterControl: 'input',
			customSearch: rangeSearch
		}, {
			field: 'd_status',
			title: 'Succeeded',
			sortable: true,
			align: 'center',
			formatter: formatBool,
		}, {
			field: 'd_walltime_ratio',
			title: 'Time',
			sortable: true,
			align: 'right',
			formatter: formatNumber,
			filterControl: 'input',
			customSearch: rangeSearch,
			formatter: formatTimeRatio,
			events: {
				'click .timedetails': timeDetails,
			},
		}, {
			field: 'd_memory',
			title: 'Memory (MB)',
			sortable: true,
			align: 'right',
			formatter: formatNumber,
			filterControl: 'input',
			customSearch: rangeSearch
		},]
	],
	detailView: true,
	detailFormatter: detailFormatter,
	striped: true,
	filterShowClear: true,
	onResetView: function() {
		$('.sizedetails').popover({
			'title': 'Size distribution',
			'content': '',
			'html': true,
			'placement':  'auto left',
		})
		$('.timedetails').popover({
			'title': 'Time details',
			'content': '',
			'html': true,
			'placement':  'auto left',
		})
	}
});

function rangeSearch (range, value) {
	fn = function(v,k) {
		return (v + '').toLowerCase().indexOf(k) !== -1
	};

	if (!range || range.length == 0) return true;
	if (range.length < 2) return fn(value, range);
	if (typeof value !== 'number') return false;

	switch(range[0]) {
		case '<': range=range.substr(1); fn = function(v,k) { return v<k } ; break
		case '>': range=range.substr(1); fn = function(v,k) { return v>k } ; break
	}
	if (range.length > 1) switch(range[0]) {
		case '=': range=range.substr(1); _fn = fn; fn = function(v,k) { return v==k || _fn(v,k)} ; break
	}
	return fn(value, range)
}

function formatNumber(n) {
	if (!n || n == "?") return "-";
	return sprintf("%.2f", n).replace(/\B(?=(\d{3})+(?!\d))/g, ",").replace('.00', '');
}
function formatTime(n) {
	if (!n || n == "?") return "N/A";
	var h = parseInt(n / 3600) % 24;
	var m = parseInt(n / 60) % 60;
	var s = parseInt(n % 60);
	return (h < 10 ? "0" + h : h) + ":" + (m < 10 ? "0" + m : m) + ":" + (s  < 10 ? "0" + s : s);
}
function formatBool(b) {
	return '<input type="checkbox" onclick="return false;" onkeydown="return false;" ' + ((b == 1.0) ? "checked" : "") +  '/>';
}

window.tools = {
	'cbc': 'CBC',
	'scramble': 'Scramble',
	'scramble-noref': 'Scramble (without reference)',
	'scramble-bzip2': 'Scramble (with bzip2)',
	'cramtools': 'CRAMTools',
	'deez': 'DeeZ',
	'deez-qual': 'DeeZ (with bzip2 and sam_comp qualities)',
	'samtools': 'SAMtools',
	'picard': 'Picard',
	'quip': 'Quip',
	'quip-asm': 'Quip (assembly)',
	'quip-ref': 'Quip (with reference)',
	'sambamba': 'Sambamba',
	'tsc': 'TSC',
	'beetl': 'BEETL',
	'dsrc': 'DSRC',
	'dsrc-m2': 'DSRC (m2 mode)',
	'fastqz': 'Fastqz',
	'fqzcomp': 'Fqzcomp',
	'fqzcomp-extra': 'Fqzcomp (extra mode)',
	'kic': 'KIC',
	'kpath': 'k-Path',
	'leon': 'Leon',
	'lfqc': 'LFQC',
	'lw-fqzip': 'LWFQZip',
	'mince': 'Mince (paired mode)',
	'mince-single': 'Mince',
	'orcom': 'ORCOM',
	'scalce': 'SCALCE (paired mode)',
	'scalce-single': 'SCALCE',
	'slimfastq': 'Slimfastq',
	'sra': 'NCBI SRA',
	'fqc': 'FQC',
}

window.fields = {
	'command': 'Command',
	'exitcode': 'Exit code',
	'walltime': 'Total time',
	'real': 'Linux real time',
	'user': 'Linux user time',
	'sys': 'Linux system time',
	'process_pid': 'Process PID',
	'd_size': 'Decompressed size (bytes)',
	'eq_file': 'File equality',
	'eq_cmp': 'UNIX cmp tool equality',
	'eq_comment': 'SAM header equality',
	'records': 'Number of records/reads',
	'size': 'Total',
	'seq': 'Sequences',
	'qual': 'Quality scores',
	'rname': 'Read identifiers',
	'aux': 'Auxiliary data',
	'pe': 'Paired-end data',
}

function indict(x,d) {
	if (!(x in d) && x.indexOf('eq_') == 0) {
		return x.substr(3)
	}
	return (x in d) ? d[x] : x
}

function formatTool(x) {	
	return indict(x, window.tools);
}

function detailFormatter(index, row) {
	console.log(row)
	var html = [];


	ifn = function(q) {
		if (!q.f) q.f = function (x) { return x };
		return function(k, v) {
			if (v.substr(0, 2) == 'd_') v = v.substr(2);
			if (v in row && row[v] != null && q.f(row[v]) != '-')  {
				html.push('<dt>' + indict(v,window.fields) + '</dt><dd>' + q.f(row[v]) + '</dd>'); 
			}
		}
	}

	html.push('<h3>Compression</h3><hr/>')
	html.push('<h4>Invocation</h4>')
	html.push('<dl>'); 
	$.each(['command', 'exitcode', 'stdin'], ifn({})); 
	$.each(['stdout', 'stderr'], ifn({f: function(x) {
		if (x.substr(x.length - 4) != '.log') return x;
		file = 'logs/' + encodeURIComponent(row.sample + '.' + row.tool + '.' + row.threads + '.' + 'cmp.log')
		return '<a class="loader" href="' + file + '" onclick="loader_init(this);return false;">' + x + '</a>';
	}})); 
	html.push('</dl>')

	html.push('<h4>Timings</h4>')
	html.push('<dl>'); 
	$.each(['walltime', 'real', 'user', 'sys'], ifn({f: formatTime})); 
	html.push('</dl>')
	html.push('<h4>Resources</h4>')
	html.push('<dl>'); 
	$.each(['process_pid', 'ru_inblock', 'ru_majflt', 'ru_maxrss', 'ru_minflt', 'ru_nivcsw',
   'ru_nvcsw', 'ru_oublock', 'ru_stime', 'ru_utime'], ifn({})); 
   html.push('</dl>')

	html.push('<h3>Decompression</h3><hr/>')
	html.push('<h4>Invocation</h4>')
	html.push('<dl>'); 
	$.each(['d_command', 'd_exitcode', 'd_stdin'], ifn({})); 
	$.each(['d_stdout', 'd_stderr'], ifn({f: function(x) {
		if (x.substr(x.length - 4) != '.log') return x;
		file = 'logs/' + encodeURIComponent(row.sample + '.' + row.tool + '.' + row.threads + '.' + 'cmp.log')
		return '<a class="loader" href="' + file + '" onclick="loader_init(this);return false;">' + x + '</a>';
	}}));  
	html.push('</dl>')
	html.push('<h4>Timings</h4>')
	html.push('<dl>'); 
	$.each(['d_walltime', 'd_real', 'd_user', 'd_sys'], ifn({f: formatTime})); 
	html.push('</dl>')
	html.push('<h4>Resources</h4>')
	html.push('<dl>'); 
	$.each(['d_process_pid', 'd_ru_inblock', 'd_ru_majflt', 'd_ru_maxrss', 'd_ru_minflt', 'd_ru_nivcsw',
   'd_ru_nvcsw', 'd_ru_oublock', 'd_ru_stime', 'd_ru_utime'], ifn({})); 
   html.push('</dl>')

	html.push('<h3>Size & Equality</h3><hr/>')
	html.push('<h4>Compressed sizes</h4>')
	html.push('<dl>'); 
	$.each(['records', 'size', 'seq', 'pe', 'aux', 'qual', 'rname'], ifn({f: formatNumber})); 
	html.push('</dl>')
	html.push('<h4>Equality</h4>')
	html.push('<dl>'); 
	$.each(['d_size'], ifn({f: formatNumber})); 
	arr = ['eq_file', 'eq_cmp', 'eq_comment'];
	$.each(arr.concat(Object.keys(row).filter(function(k) {
		return arr.indexOf(k) == -1 && k.indexOf('eq_') == 0;
	})), ifn({f: function(x) {
		if (x === true) {
			return 'Equal'
		} else if (x === false) {
			return 'Not equal'
		} else {
			return x
		}
	}})); 
	html.push('</dl>')

	return html.join('');
}

function loader_init(a) {
	file=$(a).attr('href')
	p=$(a).parent()
	if (p.next().is('pre')) {
		p.next().remove()
	} else $.ajax({
		url: file, 
		beforeSend: function() {
			p.after('<pre>Loading...</pre>')
		},
		success: function(data) {
			if (p.next().is('pre')) {
				p.next().text(data)
			}
		},
		error: function() {
			if (p.next().is('pre')) {
				p.next().text(' ')
			}
		}
	})
}

function formatSize(n) {
	if (!n || n == "?") return "N/A";
	return '<a class="sizedetails" href="javascript:void(0)">' + formatNumber(n / 1024.0 / 1024.0) + '</a>';
}

function formatTimeRatio(n) {
	if (!n || n == "?") return "N/A";
	return '<a class="timedetails" href="javascript:void(0)" data-field="' + this.field + '">' + formatNumber(n) + '</a>';
}

function timeDetails (e, value, row, index) {
	p = ''
	if ($(this).data('field').substr(0,2) == 'd_') {
		p = 'd_'
	}
	ref = 'samtools'
	if ($('#table').data('url').indexOf('_fastq') != -1) {
		ref = 'pigz'
	}

	html = []
	html.push('<dt>Original time</dt><dd>' + formatTime(row[p + 'walltime']) + '</dd>')
	html.push('<dt>' + indict(ref, tools) + ' time</dt><dd>' + formatTime(row[p + 'walltime'] / row[p + 'walltime_ratio']) + '</dd>')
	html.push('<dt>Ratio</dt><dd>' + formatNumber(row[p + 'walltime_ratio']) + '</dd>')
	$(this).attr('data-content', '<dl class="dl-small">' + html.join('') + '</dl>')
}

function sizeDetails(e, value, row, index) {
	html = []
	f = [ 'seq', 'pe', 'aux', 'qual', 'rname', ]
	$.each(f, function(k, v) {
		if (row[v]) html.push('<dt>' + indict(v,window.fields) + '</dt><dd>' + formatNumber(row[v] / 1024 / 1024) + ' MB</dd>');
	});
	$(this).attr('data-content',  '<dl class="dl-small">' + html.join('') + '</dl>')
}

$('body').on('click', function (e) {
 	$('[data-original-title]').each(function () {
     	if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {
         	$(this).popover('hide');
     	}
 	});
});