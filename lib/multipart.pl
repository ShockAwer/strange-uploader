package multipart;
#
# multipart.pl (2002-11-07)
#
# multipart/form-data ���󂯎��
# �w�b�_�̏�����������ƓK������
#
# require 'multipart.pl';
# @uploadfiles = &multipart::get_multipart(\&func_storeform, $tmpdir);
# @uploadfiles = &multipart::upload_files();
#
#
# �t�@�C�����Ɂu�\�v�u�\�v�u�\�v�Ȃǂ̑��o�C�g�ڂ�0x5C(\)�̕����i�V�t�gJIS�Łj
# ���܂܂�Ă���ƃt�@�C���������܂����o���Ȃ��o�O�i�d�l�j������܂��B
#
use strict;

my $CRLF = "\x0D\x0A";
my $BLKSIZE = 4 * 1024;
@multipart::UploadFiles = ();

# �}���`�p�[�g�f�[�^�ǂݍ���
sub get_multipart {
	
	my ($func_storeform, $tmpdir) = @_;
	$tmpdir ||= '/tmp';
	
	local ($multipart::buffer, $multipart::left);
	$multipart::buffer = '';
	$multipart::left = $ENV{'CONTENT_LENGTH'};
	
	# boundary�̎擾
	my ($boundary) = $ENV{'CONTENT_TYPE'} =~ /boundary=\"?([^\";,]+)\"?/;
	if ( !defined ($boundary) or length ($boundary) > 256 ) {
		die("Boundary not provided\n");
	}
	$boundary = "--" . $boundary
		unless $ENV{'HTTP_USER_AGENT'} =~ /MSIE\s+3\.0[12];\s*Mac/i;
	
	binmode(STDIN);
	
	while (<STDIN>) {
		$multipart::left -= length();
		last if /$boundary$CRLF/o;
	}
	
  Multipart:
	while (!&_end_of_multipart()) {
		my ($header, $cd, $ct);
		
		# �w�b�_�ǂݍ���
		&_readblock(\$header, "${CRLF}${CRLF}") or last Multipart;
		
		foreach (split ($CRLF, $header)) {
			/^Content-Disposition:\s+(.*)/i and do{ $cd = $1; next };
			/^Content-Type:\s+(.*)/i		and do{ $ct = $1; next };
		}
		my ($field) = $cd =~ /\bname="?([^\";]+)"?/;
		my ($fname) = $cd =~ /\bfilename="?([^\";]+)"?/;
		
		unless (defined ($field)) { $field = 'unknown'; }
		
		if ($fname) {	# �Y�t�t�@�C��
			my $upload = &_new_upload_file($fname, $ct, $field, $tmpdir);
			
			open(UPLOAD, "> $upload->{tmpfile}")
				or die("�Y�t�t�@�C���̏o�͂Ɏ��s���܂���\n");
			binmode(UPLOAD);
			
			# �{�f�B�[�ǂݍ���
			&_readblock(\*UPLOAD, "${CRLF}$boundary") or last Multipart;
			
			close(UPLOAD);
		} else {
			my ($value);
			&_readblock (\$value, "${CRLF}$boundary") or last Multipart;
			&$func_storeform($field, $value);
		}
	}
	return @multipart::UploadFiles;
}

sub _end_of_multipart {
	# �u--CRLF�v���Ō�Ɏc�邩�� 4
	($multipart::left + length($multipart::buffer) <= 4 ) ? 1 : 0;
}


# �f���~�^�܂œǂݍ���
sub _readblock {
	# $out �̓X�J���[���t�@�C���n���h���̃��t�@�����X
	my ($out, $delimiter) = @_;
	
	my ($write, $found, $ishandle);
	$found = 0;
	$write = '';
	$ishandle = ref($out) eq 'SCALAR' ? 0 : 1;
	
	until ($found) {
		# �u���b�N�T�C�Y���t�H�[���̎c�肪���Ȃ��Ȃ�����A����B
		my $readbyte = ($multipart::left < $BLKSIZE) ? $multipart::left : $BLKSIZE;
		
		if ($readbyte > 0) {		# �o�b�t�@�ɓǂݍ���
			my $len = read (STDIN, $multipart::buffer, $readbyte, length($multipart::buffer))
				or die ("malformed multipart POST\n");
			$multipart::left -= $len;
		}
		
		my $pos = index ($multipart::buffer, $delimiter);  # �f���~�^��T��
		if ($pos >= 0) {
			# �f���~�^�܂ł�$write�Ɉڂ��B�i�f���~�^�������āj
			$write = substr ($multipart::buffer, 0, $pos);
			substr ($multipart::buffer, 0, $pos + length($delimiter)) = '';
			
			$found++;
		} else {
			die ("malformed multipart POST\n") unless ($readbyte > 0);
			
			# �o�b�t�@�̍Ō�Ƀf���~�^�̐擪�����܂܂��\�����L��̂�
			# ���̕�����������$write�Ɉڂ��B
			my $remove = length ($multipart::buffer) - length ($delimiter) + 1;
			$write = substr ($multipart::buffer, 0, $remove);
			substr ($multipart::buffer, 0, $remove) = '';
		}
		
		# $out�ɏo��
		$ishandle ? print($out $write) : ($$out .= $write);
	}
	$found;
}


# �A�b�v���[�h�t�@�C���̏��
sub _new_upload_file {
	my ($filename, $mimetype, $field, $tmpdir, $basename, $tmpfile);
	
	($filename, $mimetype, $field, $tmpdir) = @_;
	
	# �t�@�C�����������o���B
	($basename) = $filename =~ /^(?:.*[:\\\/])?([^:\\\/]+)/;
	
	$tmpfile = "$tmpdir/".time.$$.'_'.(@multipart::UploadFiles+1).'.tmp';
	
	my $upload_data = {
		filename => $filename,
		field    => $field,
		basename => $basename,
		mimetype => $mimetype,
		tmpfile  => $tmpfile,
	};
	push (@multipart::UploadFiles, $upload_data);
	
	return $upload_data;
}

# �A�b�v���[�h�t�@�C���̃��X�g
sub upload_files {
	return @multipart::UploadFiles;
}

# �e���|�����t�@�C���̌㏈��
END {
	unlink map{ $_->{tmpfile} } @multipart::UploadFiles if (@multipart::UploadFiles);
}

1;