#! /usr/local/bin/perl
#
#  ����ڂ񂠂Ղ낾���烍�O�`�����R���o�[�g����CGI�X�N���v�g
#                                    �i2000�N9��3���ňȍ~�̃o�[�W�����ɑΉ��j
#
#
#  �g����
#  �E�ϊ��������t�@�C���Ɠ����f�B���N�g���ɒu���Ď��s���܂��B
#  �E�t�@�C���Ɛ擪�������w�肵�A�ϊ��{�^���������Ă��������B
#
#  �E�Ώۃt�@�C���Ƃ��̃t�@�C�����u����Ă���f�B���N�g���̃p�[�~�b�V������
#    �������݉\�ȏ�Ԃɂ���K�v������܂��B
#  �E�Ώۃt�@�C�����Ɂu.bak�v��t���������O�Ńo�b�N�A�b�v�t�@�C�����쐬���܂��B
#  �E���s�ɂ�Time::Local���W���[�����K�v�ł��B���Ԃ�W���œ����Ă�Ǝv���܂���
#
#  �ϊ��͂����g�̐ӔC�ɂ����čs�Ȃ��Ă�������
#
use strict;
my ($scriptname, $dir, $logtype);

# ���̃X�N���v�g��URL
$scriptname = $ENV{SCRIPT_NAME};

# ���O�t�@�C��������f�B���N�g��
$dir = '.';

# �ϊ��Ώۂ̃��O�`��
#  0 : STRENGE UPLOADER 2002�N11��17���ňȑO�̃��O�`��
#  1 : ����ڂ񂠂Ղ낾
$logtype = 1;

# �^�C���]�[��
$ENV{TZ} = 'JST-9';


######################################################

sub getformdata {
	my $form = {};
	my $url_encoded_data;
	
	if ($ENV{'REQUEST_METHOD'} eq 'POST') {
		read ( STDIN, $url_encoded_data, $ENV{CONTENT_LENGTH} );
	} else {
		$url_encoded_data = $ENV{QUERY_STRING};
	}
	if ($url_encoded_data ne '') {
		$url_encoded_data =~ tr/+/ /;
		
		foreach my $pair ( split (/&/, $url_encoded_data) ) {
			my ($name, $value) =  split (/=/, $pair, 2);
			$name  =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
			$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
			
			$value =~ s/&/&amp;/g;
			$value =~ s/</&lt;/g;
			$value =~ s/>/&gt;/g;
			$value =~ tr/\r\n//d;
			
			$form->{$name} = $value;
		}
	}
	return $form;
}


# ����ڂ񂠂Ղ낾�f�[�^
# id  suffix  comment  host  ua  date  size  mimetype  passwd  md5  dcrc  \n
# �Eid �͎l���̐���
# �Edate��2002�N11/26(��)07:34�̂悤�Ȍ`��
# �E�폜�֎~�̂Ƃ���passwd��*
# �Esize�̓L���o�C�g�P��
# �E�f�[�^�̓^�u��؂�
sub conv_from_zurubon {
	require Time::Local;
	
	my $rl_fields = @_ > 1 ? shift : [];
	my ($line, $prefix) = @_;
	
	my @zurubon = split (/\t/, $line, -1);
	
	return undef if (@zurubon < 9);
	
	my ($id, $suffix, $comment, $host, $ua, $date, $size, $mimetype, $passwd) = @zurubon;
	my ($time, $filename);
	
	$filename = "$prefix$id.$suffix";
	$id += 0;	#�����̓���0�����
	$suffix =~ /^\w+$/ or return undef;
	
	$passwd = '' if ($passwd eq '*');
	
	$date =~ /^(\d+)�N(\d+)\/(\d+)\(\S+?\)(\d+)\:(\d+)$/ or return undef;
	$time = Time::Local::timelocal(0, $5, $4, $3, $2-1, $1-1900);
	$size =~ /^\d+$/ or return undef;
	$size *= 1024;
	
	@$rl_fields = ($id, $suffix, $filename, $filename, $comment, $time, $size, $passwd, $host, $ua, $mimetype);
	
	$rl_fields;
}

# ��: id  suffix  name  comment  time  size  passwd  host  ua  mimetype  \n
# �V: id  suffix  filename  dispname  comment  time  size  passwd  host  ua  mimetype  \n
# �i�f�[�^�̓^�u��؂�j
sub conv_from_old_version {
	my $rl_fields = @_ > 1 ? shift : [];
	my ($line, $prefix) = @_;
	
	@$rl_fields = split (/\t/, $line, -1);
	
	return undef if (@$rl_fields != 10);
	
	my $filename = sprintf("%s%04d.%s", $prefix, $rl_fields->[0], $rl_fields->[1]);
	
	splice (@$rl_fields, 2, 0, $filename);
	
	$rl_fields;
}

sub logconv {
	my ($logfile, $prefix, $convertfunc) = @_;
	
#	print STDERR "$logfile �̃��O�`�����R���o�[�g���܂��B\n";
	
	my @logdata = ();
	
	open (LOG, "$dir/$logfile") or &error("���O�t�@�C���̓ǂݍ��݂Ɏ��s���܂����B($!)\n");
	eval{ flock (LOG, 1) };
	
	while (<LOG>) {
		chop;
		my @fields;
		
		&$convertfunc(\@fields, $_, $prefix)
			or &error("���O�`�����Ⴄ�悤�ł��B�R���o�[�g�𒆎~���܂����B\n");
		
		push (@logdata, join("\t", @fields) . "\n");
	}
	eval{ flock (LOG, 8) };
	close (LOG);
	
	rename ($logfile, "$logfile.bak") or &error("�o�b�N�A�b�v�t�@�C���̍쐬�Ɏ��s���܂����B($!)\n");
	
#	print STDERR "$logfile.bak �Ƀo�b�N�A�b�v�����܂����B\n";
	
	open (LOG, "> $logfile") or &error("���O�t�@�C���̏������݂Ɏ��s���܂����B($!)\n");
	eval{ flock (LOG, 2) };
	print LOG @logdata;
	eval{ flock (LOG, 8) };
	close (LOG);
	
#	print STDERR "�R���o�[�g�I��\n";
	
	&print_msg('', "�R���o�[�g�͖����I���܂����B\n");
}

sub print_html_header {
	my $title = shift || 'logconv';
	
	print <<_EOF;
Content-type: text/html; charset=Shift_JIS
Content-Language: ja

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<title>$title</title>
</head>
<body text="#ffffff" bgcolor="#004040" link="#eeffee" vlink="#dddddd" alink="#ff0000">
_EOF
}

sub html {
	
	&print_html_header();
	
	print <<_EOF;
<h2>���O�R���o�[�^</h2>


<form method="POST" action="$scriptname">
<input type="hidden" name="act" value="confirm">

�t�@�C����I�����Ă��������B
<hr>
<table border="0" width="60%">
<tr>
  <th>File</th>
  <th>Size</th>
  <th>Last-Modified</th>
</tr>
_EOF
	
	opendir (DIR, $dir);
	my @files = sort {$a cmp $b} grep(!/^\.\.?$/, readdir (DIR));
	closedir (DIR);
	
	foreach my $file (@files) {
		next unless (-f "$dir/$file");
		my ($size, $mtime) = (stat(_))[7,9];
		
		my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($mtime);
		my $date = sprintf("%d/%02d/%02d %02d:%02d:%02d",
			$year+1900, $mon+1, $mday, $hour, $min, $sec);
		
		print<<_EOF
<tr>
  <td align="left"><input type="radio" name="fn" value="$file"> $file</td>
  <td align="right">$size byte</td>
  <td align="center">$date</td>
</tr>
_EOF
	}
	
	print <<_EOF;
</table>
<hr>

�擪���� (\$prefix) <input type="text" name="prefix" size="8" value="up">�@
<input type="submit" value="�ϊ�">

</form>

</body>
</html>
_EOF
}

sub confirm {
	my $formdata = shift;
	
	my $backup = $formdata->{fn} . '.bak';
	my $msg;
	
	if (-e "$dir/$backup") {
		$msg = qq|$backup��<font color="red">�㏑������</font>�o�b�N�A�b�v�t�@�C�����쐬���܂�|;
	} else {
		$msg = qq|$backup�Ƀo�b�N�A�b�v�t�@�C�����쐬���܂�|;
	}
	
	&print_html_header();
	
	my $prefix = $formdata->{prefix};
	$prefix = '<i>(����)</i>' if ($prefix eq '');
	
	print <<_EOF;
<h2>���O�R���o�[�^</h2>
<table border="0">
<tr><td nowrap>�t�@�C����</td><td nowrap>�F $formdata->{fn}</td></tr>
<tr><td nowrap>�擪����</td><td nowrap>�F $prefix</td></tr>
<tr><td colspan="2">$msg</td></tr>
<tr><td colspan="2">��낵���ł����H</td></tr>
</table>

<form method="POST" action="$scriptname">
<input type="hidden" name="act"    value="convert">
<input type="hidden" name="fn"     value="$formdata->{fn}">
<input type="hidden" name="prefix" value="$formdata->{prefix}">
<input type="submit" value="�ϊ�">

</form>
</body>
</html>
_EOF
	
}

# �f�[�^�`�F�b�N
sub datacheck {
	my $formdata = shift;
	($formdata->{fn}) = $formdata->{fn} =~ /^([^:\\\/|<>+&]+)$/;
	
#	&error("�擪���������͂���Ă��܂���B\n") if ($formdata->{prefix} eq '');
	&error("�t�@�C�����I������Ă��܂���B\n") if ($formdata->{fn} eq '');
	&error("�t�@�C�������݂��܂���B\n") unless (-f "$dir/$formdata->{fn}");
	&error("�t�@�C���ɓǂݍ��ݑ���������܂���B\n") unless (-r _);
	&error("�t�@�C���ɏ������ݑ���������܂���B\n") unless (-w _);
	&error("�f�B���N�g���ɏ������ݑ������������߃o�b�N�A�b�v�t�@�C�����쐬�ł��܂���B\n")
		unless (-w $dir);
}


# �G���[����
sub error { &print_msg('ERROR', @_); }

sub print_msg {
	my $title  = shift;
	my $errmsg = join('', @_);
	
	&print_html_header($title);
	
	print <<_EOF;
<p><big><strong>$errmsg</strong></big></p>
<hr>
<a href="$scriptname">�߂�</a>
</body>
</html>
_EOF
	exit;
}


Main: {
	my $formdata = &getformdata();
	my $act = $formdata->{act};
	
	if ($act eq 'confirm') {
		&datacheck($formdata);
		&confirm($formdata);
	} elsif ($act eq 'convert') {
		&datacheck($formdata);
		my $f = $logtype ? \&conv_from_zurubon : \&conv_from_old_version;
		&logconv($formdata->{fn}, $formdata->{prefix}, $f);
	} else {
		&html();
	}
	exit;
}

