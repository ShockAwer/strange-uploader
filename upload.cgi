#! /usr/local/bin/perl
#
#�@STRANGE UPLOADER     2002�N12��23����
#
$::COPYRIGHT = 'STRANGE UPLOADER (2002-12-23)';
#
#
#  �����ݒ��upload.init�ɂ���܂��B
#
#
# �y�t�@�C���\����z�p�[�~�b�V�����͏��L�Ҍ�����CGI�������ꍇ
#
#  [cgi-bin] (701) /
#      |
#      |-- upload.cgi         (700)
#      |-- upload.init        (600)
#      |-- style.css          (644)
#      |-- styleselector.js   (644)
#      |-- PaintBBS.jar       (644) (���G�`���@�\�g�p���̂�)
#      |-- palette.js         (644) (���G�`���@�\�g�p���̂�)
#      |-- shiihelp.html      (644) (���G�`���@�\�g�p���̂�)
#      |
#      +-- [lib] (700) /
#      |     |
#      |     |-- multipart.pl (600)
#      |     |-- getpic.pl    (600) (���G�`���@�\�g�p���̂�)
#      |     |-- imagesize.pl (600) (���G�`���@�\�g�p���̂�)
#      |     |-- jcode.pl     (600)
#      |
#      +-- [data] (700) /
#      |     |
#      |     |-- upload.log   (600)
#      |     |-- admin.passwd (600)
#      |     |-- count.file   (600) (�K�v�ɉ�����)
#      |     |-- renzoku.file (600) (�K�v�ɉ�����)
#      |     |-- deny.file    (600) (�K�v�ɉ�����)
#      |
#      +-- [stored] (701) /
#
#   �E�f������N�����͊Ǘ��҃p�X���[�h�o�^��ʂɂȂ�܂��B
#   �E�T�[�o���ړ]�������ɂ́uadmin.passwd�v����[�N���A���Ă��������B
#
#
##################################################

# jcode.pl�Ȃǂ̃��C�u������ʃf�B���N�g���ɒu���������͂����Ŏw��
use lib './lib';

#use strict;
#our ($TITLE, $CGIURL, $BASE_URL, $LOG_FILE, $STORE_DIR, $STORE_URL, $INFORMATION, $LINK_BAR, $BANNER, @STYLESHEET, $BODY,
#	$PREFIX, $DEF_EXT, $LOCAL_FILENAME_SW, $MAX_UPLOAD_SIZE, $DISK_SPACE_MAX,
#	$LOGSAVE, $MSGDISP, $IMAGEDISP, $MAX_COMMENT_SIZE, $MIN_UPLOAD_SIZE,
#	$AUTOLINK, $COUNTFILE, $ADMINPASSWD,
#	$IP_REC, $UA_REC, $RENZOKU_FILE, $RENZOKU_TIME, $ACCESS_CONTROL, @EXCEPT_REFERER, $HTML_EXT,
#	$MAKE_INDEX_SW, $INDEX_FILEPATH, $OEKAKI_SW, $OEKAKI_MAX_SIZE, $OEKAKI_DEF_SIZE, $OEKAKI_ANIMATION, %APPLET_PARAMS,
#	$TMPDIR, %MIMETYPE, $MAX_FILENAME_SIZE, $MAX_PAGE_INDEX, $COOKIE_NAME, $MOJIBAKE_TAISAKU, $TEXT_BANNER,
#	%Form, %Cookie, @UploadFiles, @PictureFiles);

# �ݒ��ǂݍ���
do './upload.init';
&cgidie('�ݒ荀�ڂ̋L�q�Ɍ�肪����܂��B', $@) if ($@);

$STORE_DIR =~ s|/$||;
$STORE_URL .= '/' unless ($STORE_URL =~ m|[\?\/]$|);	#gw.cgi?filename ���g����悤��
$BASE_URL  =~ s|/$||;
$TMPDIR    =~ s|/$||;

$SIG{__DIE__} = \&cgidie;


##################################################
# HTML�㕔����

my $HeaderPrinted = 0;
sub print_header {
	
	my ($title, $is_indexpage) = @_;
	
	if (!$is_indexpage) {
		return if ($HeaderPrinted++);
	}
	
	$title = $title ? $TITLE.' - '.$title : $TITLE;
	$title =~ s/<.*?>//g;
	
	my $stylesheet = '';
	my $cssselector = '';
	if (@STYLESHEET > 2) {
		for (my $i = 0; $i < @STYLESHEET; $i +=2) {
			my $rel = $i == 0 ? 'stylesheet' : 'alternate stylesheet';
			$stylesheet .= qq|<link rel="$rel" type="text/css" href="$BASE_URL/$STYLESHEET[$i]" title="$STYLESHEET[$i+1]">\n|;
		}
		$stylesheet .= qq|<script type="text/javascript" src="$BASE_URL/styleselector.js" charset="Shift_JIS"></script>|;
		$cssselector = qq|<script type="text/javascript"><!--\n  writeCSSSelectForm("�f�U�C���ύX�F");\n// --></script>|;
	} else {
		$stylesheet = qq|<link rel="stylesheet" type="text/css" href="$BASE_URL/$STYLESHEET[0]">|;
	}
	
	if (!$is_indexpage) {
		print <<_EOF;
Content-Type: text/html; charset=Shift_JIS
Content-Language: ja
Cache-Control: no-store, must-revalidate
Pragma: no-cache

_EOF
	}
	print <<_EOF;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=Shift_JIS">
<meta http-equiv="Content-Script-Type" content="text/javascript">
$stylesheet
<title>$title</title>
</head>

$BODY
$cssselector
_EOF
}

sub print_obititle {
	my $title = @_ ? $TITLE.' - '.shift() : $TITLE;
	print <<_EOF;
<table width="100%" border="0" cellpadding="2" cellspacing="1" class="obi" summary="obi">
<tr><td><font size="4"><strong>$title</strong></font></td></tr></table>
<br>
_EOF
}

sub print_footer {
	my $applet = $OEKAKI_SW ?
	  qq|\n���G�`���A�v���b�g <a href="http://www.gt.sakura.ne.jp/~ocosama/">PaintBBS (���������)</a>| : '';
	print <<_EOF;
<hr>
<div align="right"><small>
<strong><a href="http://yasashiku.site.ne.jp/uploader/">$::COPYRIGHT</a></strong>
<!-- <small><a href="$CGIURL?help=disk">��</a></small> --><br>
$applet
</small></div>
$BANNER
</body>
</html>
_EOF
}


##################################################
# ���X�g�\��

sub list {
	
	my $upload_limit = '';
	$upload_limit .= &byte_calc($MIN_UPLOAD_SIZE) . '���� ' if ($MIN_UPLOAD_SIZE);
	$upload_limit .= $MAX_UPLOAD_SIZE ? &byte_calc($MAX_UPLOAD_SIZE) . '�܂�' : '������';
	
	print <<_EOF;
<p>$INFORMATION</p>
<form name="uploadform" method="POST" enctype="multipart/form-data" action="$CGIURL">
<a href="$CGIURL?help=file">�t�@�C��</a><small><strong> �i$upload_limit�j</strong></small><br>
<input type="file" size="30" name="uploadfile">
<select name="suffix"><option value="" selected>����g���q�I��
_EOF
	
	for (sort keys(%MIMETYPE)) {
		next if ($HTML_EXT and /^htm/);
		print qq|<option value="$_">$_\n|;
	}
	
	my $cookie_ok_checked = %Cookie ? ' checked' : '';
	
	print <<_EOF;
</select><br>
�R�����g<br>
<input type="text" size="60" name="comment" value="">
<input type="submit" name="act" value="Up/Reload" class="button"><input type="reset" value="Cancel" class="button"><br>
<a href="$CGIURL?help=del">del pass</a>: <input type="password" size="10" name="delpass" maxlength="10" value="@{[&htmlencode($Cookie{delpass})]}">�@
<input type="checkbox" name="cookie_ok" value="on" $cookie_ok_checked><small>�p�X���[�h���N�b�L�[�ɕۑ�</small>
_EOF
	if ($LOCAL_FILENAME_SW > 0) {
		print qq|<input type="checkbox" name="hidename" value="on"><small>�t�@�C�������B��</small>\n|;
	}
	
	print <<_EOF;
<input type="hidden" name="page" value="$Form{page}">
<input type="hidden" name="lm"	 value="$Form{lm}">
<input type="hidden" name="sort" value="$Form{sort}">
<input type="hidden" name="rev"  value="$Form{rev}">
<input type="hidden" name="k"    value="$MOJIBAKE_TAISAKU">
</form>
_EOF
	
	# ���G�`���@�\
	if ($OEKAKI_SW) {
		my $anime_sw = $OEKAKI_ANIMATION ?
			qq|<input type="checkbox" name="anime" value="on" checked><small>�A�j���L�^</small>| : '';
		print <<_EOF;
<form method="GET" action="$CGIURL">
<input type="hidden" name="m" value="E">
��<select name="hsize">
_EOF
		for (my $i = 100; $i <= $OEKAKI_MAX_SIZE; $i+=50) {
			my $selected = $i == $OEKAKI_DEF_SIZE ? 'selected' : '';
			print qq|<option value="$i"$selected>$i\n|;
		}
		print qq|</select> �~\n�c<select name="vsize">\n|;
		for (my $i = 100; $i <= $OEKAKI_MAX_SIZE; $i+=50) {
			my $selected = $i == $OEKAKI_DEF_SIZE ? 'selected' : '';
			print qq|<option value="$i"$selected>$i\n|;
		}
		print <<_EOF;
</select> pixel
<input type="submit" value="���G�`������" class="button">
$anime_sw
</form>

_EOF
	}
	
	print "<small>";
	if ($COUNTFILE ne ""){	# �J�E���^
		print &counter(), "�@\n";
	}
	print "D : �t�@�C���폜�@";
	print "A : �`��A�j���Đ��@" if ($OEKAKI_ANIMATION);
#	print "�ő�ۑ����F$LOGSAVE";
	print "</small>\n";
	
	print <<_EOF;
<hr><small>
 | <a href="$CGIURL?m=I">�摜�{��</a>
 | <a href="$CGIURL?m=S">�t�@�C������</a>
$LINK_BAR |
</small>
_EOF
	
	open (LOG, $LOG_FILE) or die("Open Error $LOG_FILE: $!\n");
	eval{ flock (LOG, 1) };
	my @log = <LOG>;
	eval{ flock (LOG, 8) };
	close (LOG);
	
	my $sorttype = $Form{sort};
	my $rev      = $Form{rev};
	
	my ($page_index, $first_idx, $last_idx) = &page_index($#log, $MSGDISP, "sort=$sorttype&amp;rev=$rev");
	
	my @sorted = ();
	if ($sorttype or $rev) {
		if ($sorttype eq 'N') {
			my @keys = map { (split(/\t/, $_))[3] } @log;
			@sorted = sort {$keys[$b] cmp $keys[$a]} 0 .. $#log;
		} elsif ($sorttype eq 'S') {
			my @keys = map { (split(/\t/, $_))[6] } @log;
			@sorted = sort {$keys[$b] <=> $keys[$a]} 0 .. $#log;
		} else {
			@sorted = 0 .. $#log;
		}
		if ($rev) { @sorted = reverse @sorted; }
	}
	my %revurl = (N => '', S => '', D => '');
	$revurl{$sorttype||'D'} = '&amp;rev=' . ($rev ? 0 : 1);
	
	print <<_EOF;
<hr>
$page_index
<hr>
<table border="0" cellpadding="1" class="list" summary="list">
<tr>
  <th align="left">ACT</th>
  <th><a href="$CGIURL?page=$Form{page}&amp;lm=$Form{lm}&amp;sort=N$revurl{N}">NAME</a></th>
  <th>COMMENT</th>
  <th align="right"><a href="$CGIURL?page=$Form{page}&amp;lm=$Form{lm}&amp;sort=S$revurl{S}">SIZE(KB)</a></th>
  <th><a href="$CGIURL?page=$Form{page}&amp;lm=$Form{lm}&amp;sort=D$revurl{D}">DATE</a></th>
</tr>
_EOF
	
	my @indexes = @sorted ?
		@sorted[$first_idx..$last_idx] : $first_idx..$last_idx;
	
	foreach (@log[@indexes]) {
		&print_article($_, 0);
	}
	print "</table>\n";
	
	# �����{�^��
	print <<_EOF;
<hr>
$page_index
<hr>
<form method="POST" action="$CGIURL" style="margin: 0px">
<a href="$CGIURL?help=search">����</a>: <input type="text" size="25" name="kwd" value="">
<input type="submit" value="Search" class="button">
<input type="hidden" name="m" value="S">
<input type="hidden" name="k" value="$MOJIBAKE_TAISAKU">
</form>
_EOF

}


##################################################
# �y�[�W�̃����N��\��

sub page_index {
	
	my ($total, $msgdisp, $urlquery) = @_;
	
	my ($page_index, $s, $e, $ss, $ee, $n);
	my $page = int($Form{page}) || 0;
	my $lm   = int($Form{lm})   || $msgdisp;
	
	my $half = int (($MAX_PAGE_INDEX - 1) / 2);
	$s = ($page > $half) ? $page - $half : 0;	# �J�n�y�[�W
	$n = int($total / $lm);						# �S�y�[�W��
	# �y�[�W���𒲐�
	if ($s + $MAX_PAGE_INDEX - 1 < $n) {
		$e = $s + $MAX_PAGE_INDEX - 1; $ee++;
	} else {
		$e = $n;
	}
	if ($e - $MAX_PAGE_INDEX - 1 > 0) {
		$s = $e - $MAX_PAGE_INDEX - 1; $ss++;
	}
	
	$page_index  = "<small>�y�[�W�F";
	$page_index .= "<strong><a href=\"$CGIURL?page=0&amp;lm=$lm&amp;$urlquery\">&lt;&lt;&lt; </a></strong> \n"
		if ($ss);
	$page_index .= "<strong><a href=\"$CGIURL?page=" . ($page-1) . "&amp;lm=$lm&amp;$urlquery\">�O��</a></strong> \n"
		if ($page - 1 >= 0);
	for (my $i = $s; $i <= $e; $i++) {
		my $pagenum = $i + 1;
		if ($i == $page) {
			$page_index .= "[ <strong>$pagenum</strong> ] \n";
		} else {
			$page_index .= qq|[<a href="$CGIURL?page=$i&amp;lm=$lm&amp;$urlquery">$pagenum</a>] \n|;
		}
	}
	if ($lm == $LOGSAVE) {
		$page_index .= "[<a href=\"$CGIURL?page=0&amp;lm=$msgdisp&amp;$urlquery\">NORM</a>] \n";
	} else {
		$page_index .= "[<a href=\"$CGIURL?page=0&amp;lm=$LOGSAVE&amp;$urlquery\">ALL</a>] \n";
	}
	$page_index .= "<strong><a href=\"$CGIURL?page=" . ($page+1) . "&amp;lm=$lm&amp;$urlquery\">����</a></strong> \n"
		if ($page + 1 <= $n);
	$page_index .= "<strong><a href=\"$CGIURL?page=$n&amp;lm=$lm&amp;$urlquery\">&gt;&gt;&gt; </a></strong> \n"
		if ($ee);
	$page_index .= "</small><br>\n";
	
	my $first_idx = ($total +1 < $lm) ? 0 : $page * $lm;
	my $last_idx = ($total < $first_idx+$lm-1) ? $total : $first_idx+$lm-1;
	
	return ($page_index, $first_idx, $last_idx);
}


##################################################
# �L�����ꌏ�\������

sub print_article {
	
	my ($article, $isimageview) = @_;
	
	my ($id, $suffix, $filename, $dispname, $comment, $date, $size, $passwd, $host, $ua, $mimetype, $imageinfo) = 
		ref ($article) ? @$article : split (/\t/, $article);
	
	$date = &getnowdate($date);
	$size = &ins_comma(int(($size+1023)/1024));
	
	if ($isimageview) {
		print <<_EOF;
<p><a href="$STORE_URL$filename"><img src="$STORE_URL$filename" height="250"></a><br>
<a href="$STORE_URL$filename"><b>$dispname</b></a><br>
$comment <small>$date</small></p>
_EOF
	} else {
		my $act = '';
		my @isimage = ('', '');
		
		$comment = '&nbsp;' if ($comment eq '');
		if ($imageinfo =~ /\d+:\d+(?:\:(\w+))?/) {
			@isimage = ('<i>', '</i>');
			$act .= qq|\n    <a href="$CGIURL?m=A&amp;id=$id">A</a>|
				if ($1 eq 'pch');
		}
		
		print <<_EOF;
<tr>
  <td>
    <a href="$CGIURL?m=D&amp;id=$id">D</a>$act
  </td>
  <td>[$isimage[0]<A href="$STORE_URL$filename">$dispname</A>$isimage[1]]</td>
  <td><small>$comment</small></td>
  <td align=right><small><strong>$size</strong></small></td>
  <td><small>$date</small></td>
</tr>
_EOF
	}
}


##################################################
# ���t���擾

my @Weeks = qw/�� �� �� �� �� �� �y/;
sub getnowdate {
	my @time = localtime($_[0]);
	return sprintf("%d/%02d/%02d(%s)%02d:%02d",
		$time[5]+1900, $time[4]+1, $time[3], $Weeks[$time[6]], $time[2], $time[1]);
}


##################################################
# �摜�{��

sub image_view {
	open (LOG, $LOG_FILE) or die("Open Error $LOG_FILE: $!\n");
	eval{ flock (LOG, 1) };
	my @log = <LOG>;
	eval{ flock (LOG, 8) };
	close (LOG);
	
	@log = grep {
		my $type = (split (/\t/, $_))[1];
		$type eq 'jpg' or $type eq 'gif' or $type eq 'png' or $type eq 'bmp';
	} @log;
	
	print "<a href=\"$CGIURL\">Return</a>\n";
	
	my ($page_index, $first_idx, $last_idx) = &page_index($#log, $IMAGEDISP, 'm=I');
	
	print "<hr>", $page_index;
	
	foreach (@log[$first_idx..$last_idx]) {
		&print_article($_, 1);
	}
	
	print $page_index;
}


##################################################
# �t�@�C������

sub search {
	
	my @cond_selected = ('','');
	$cond_selected[ $Form{cond} eq 'or' ? 1 : 0 ] = ' selected';
	
	print <<_EOF;
<form method="POST" action="$CGIURL">
<a href="$CGIURL?help=search">����</a>: <input type="text" size="25" name="kwd" value="$Form{kwd}">
<input type="submit" value="Search" class="button">
<select name="cond">
  <option value="and"$cond_selected[0]>AND����</option>
  <option value="or"$cond_selected[1]>OR����</option>
</select>
<input type="hidden" name="m" value="S">
<input type="hidden" name="k" value="$MOJIBAKE_TAISAKU">
</form>
<a href="$CGIURL">Return</a>
_EOF
	if ($Form{kwd} ne '') {
		print "<hr>\n";
		
		# ��U�_�u���N�E�H�[�g�ɖ߂�
		my $tmp;
		($tmp = $Form{kwd}) =~ s/&quot;/"/g;
		
		my @words = map {
			/^"(.*)"$/ ? scalar ($_ = $1, s/""/&quot;/g, $_) : scalar (s/"/&quot;/g, $_);
		} $tmp =~ /("[^"]*(?:""[^"]*)*"|\S+)(?:\s|$)/g;
		
		print "�������ʁF ";
		foreach (@words){ print "'$_'\n" }
		
		print <<_EOF;
<table border=0 class="list" summary="list">
<tr>
  <th>ACT</th>
  <th>NAME</th>
  <th>COMMENT</th>
  <th>SIZE(KB)</th>
  <th>DATE</th>
</tr>
_EOF
		open (LOG, $LOG_FILE) or die("Open Error $LOG_FILE: $!\n");
		eval{ flock (LOG, 1) };
		
		# $Form{cond}�ɒl���������AND������
		my $cond = $Form{cond} eq 'or' ? '||' : '&&';
		my $checkfunc = &build_match_function($cond, @words);
		
		while (<LOG>) {
			my @article = split (/\t/, $_);
			$_ = join ("\t", @article[2,3,4]);	#filename  dispname  comment
			
			&print_article(\@article) if (&$checkfunc());
		}
		eval{ flock (LOG, 8) };
		close (LOG);
		print "</table>\n";
	}
}


##################################################
# $_ �ɑ΂��Č������s�Ȃ��֐������

sub build_match_function {
	my $cond = shift;
	my $expr = join ($cond, map { 'm/' . quotemeta($_) . '/i' } @_);
	my $sub = eval "sub { $expr }";		# �����̊֐����쐬����
	local ($@);
	die $@ if $@;
	return ($sub);
}


##################################################
# ���e���� (�t�@�C���A�b�v���[�h)

sub file_upload {
#	return unless ($Referer =~ /$CGIURL/i);
	
	if (@UploadFiles > 1) {
		die("��x�ɃA�b�v���[�h�ł���t�@�C���͈�����ł��B\n");
	}
	my $uploadfile = $UploadFiles[0];
	
	my $size = -s $uploadfile->{tmpfile};
	return if ($size == 0);
	
	if ($MIN_UPLOAD_SIZE and $size < $MIN_UPLOAD_SIZE*1024) {
		die ("����������t�@�C���̓A�b�v���[�h�ł��܂���B\n");
	}
	
	my $suffix = &get_filetype($uploadfile);
	$suffix = 'txt' if ($HTML_EXT and $suffix =~ /^htm/);
	
	&post_upload_data($uploadfile, $suffix);
}


##################################################
# ���e���� (���G�`���f�[�^)

sub oekaki_upload {
#	return unless ($Referer =~ /$CGIURL/i);
	
	my ($picturefile, $suffix, $imageinfo);
	
	$picturefile = $PictureFiles[0];
	$suffix = $picturefile->{type};
	
	if ($picturefile->{width} > $OEKAKI_MAX_SIZE or $picturefile->{height} > $OEKAKI_MAX_SIZE) {
		die("�摜�̃T�C�Y���傫�����܂�\n");
	}
	$imageinfo = [$picturefile->{width}, $picturefile->{height}];
	
	# PCH
	if (@PictureFiles > 1 && $PictureFiles[1]->{type} eq 'pch') {
		push (@$imageinfo, $PictureFiles[1]);
	}
	&post_upload_data($picturefile, $suffix, $imageinfo);
}


##################################################
# ���e�����Q

sub post_upload_data {
	my ($uploadfile, $suffix, $rl_imageinfo) = @_;
	
	my (@newlogdata, $num, $filename, $dispname,  $comment, $size, $passwd, $host, $ua, $mimetype, $imageinfo);
	
	if ($RENZOKU_FILE ne '' and &renzoku_seigen()) {
		die("�A�����e�����B���Ԃ�u���Ă�蒼���Ă��������B\n");
	}
	
	# �R�����g
	$comment = $Form{comment};
	if (length($comment) > $MAX_COMMENT_SIZE) {
		die("�R�����g���������܂��B\n");
	}
	&autolink(\$comment) if ($AUTOLINK);
	
	# �t�@�C���T�C�Y
	$size = -s $uploadfile->{tmpfile};
	
	# �폜�p�X
	$passwd = ($Form{delpass} ne '') ? &encrypt($Form{delpass}) : '';
	
	# USER AGENT
	$ua = ($UA_REC > 0) ? $ENV{HTTP_USER_AGENT} : '';
	&htmlencode(\$ua);
	
	# �z�X�g
	$host = ($IP_REC > 0) ? &getremotehost() : '';
	
	# Mime-Type
	$mimetype = defined ($uploadfile->{mimetype}) ? $uploadfile->{mimetype} : '';
	&htmlencode(\$mimetype);
	
	
	$num = 1;
	open (LOG, "+<$LOG_FILE") or die("Open Error $LOG_FILE: $!\n");
	eval{ flock (LOG, 2) };
	
	if (defined($_ = <LOG>)) {
		my ($id) = split (/\t/, $_);
		
		$num = $id + 1;
	}
	
	# �t�@�C����
	if ($LOCAL_FILENAME_SW > 0 and !$Form{hidename} and defined ($uploadfile->{basename})) {
		$dispname = $uploadfile->{basename};
		# �������閼�O�͏ȗ�
		substr ($dispname, $MAX_FILENAME_SIZE) = '..' if (length ($dispname) > $MAX_FILENAME_SIZE);
		
		if ($LOCAL_FILENAME_SW == 2) {
			$filename = &getuploadfilename($uploadfile->{basename}, $suffix);
		}
		# ���[�J���̃t�@�C�������g���Ȃ�������A�ԃt�@�C����
		$filename ||= &getrenbanfilename($num, $suffix) or die ("���O�f�[�^�����Ă�H\n");
	} else {
		# �����Ƃ��A�ԃt�@�C����
		$dispname = $filename = &getrenbanfilename($num, $suffix) or die ("���O�f�[�^�����Ă�H\n");
	}
	&htmlencode(\$dispname);
	
	# ���l�[������
	rename ($uploadfile->{tmpfile}, "$STORE_DIR/$filename")
		or die("Write Error $STORE_DIR/$filename: $!\n");
	
	# ���G�`���f�[�^
	if ($rl_imageinfo) {
		
		# PCH�t�@�C���i���G�`���A�j���f�[�^�j�L�^
		if ($rl_imageinfo->[2]) {
			my $pchfile = $rl_imageinfo->[2];
			my $pchfilename = &getrenbanfilename($num, 'pch') or die ("���O�f�[�^�����Ă�H\n");
			
			rename ($pchfile->{tmpfile}, $STORE_DIR.'/'.$pchfilename)
				or die ("Write Error $STORE_DIR/$filename: $!\n");
			
			$rl_imageinfo->[2] = 'pch';
		}
		$imageinfo = join (':', @$rl_imageinfo);
		
	} else {
		$imageinfo = '';
	}
	
	# ���O�f�[�^�̐擪�ɒǉ�
	push (@newlogdata, join("\t", $num, $suffix, $filename, $dispname, $comment, time, $size, $passwd, $host, $ua, $mimetype, $imageinfo) . "\n");
	
	my $i = 1;
	seek (LOG, 0, 0);
	while (<LOG>) {
		if ($i++ < $LOGSAVE) {
			push (@newlogdata, $_);
		} else {
			my @article = split (/\t/, $_);
			
			&unlink_filedata (\@article);
		}
	}
	
	# �f�B�X�N�T�C�Y�ɂ�鎩���폜�@�\
	# �Â������珇�Ԃɏ����B
	if ($DISK_SPACE_MAX) {
		my $use = &disk_used();
		my $limit = $DISK_SPACE_MAX * 1024;
		while ($use > $limit) {
			my @article = split (/\t/, pop (@newlogdata));
			
			$use -= &unlink_filedata (\@article);
		}
	}
	
	seek (LOG, 0, 0);
	print LOG @newlogdata;
	truncate (LOG, tell(LOG));
	eval{ flock (LOG, 8) };
	close (LOG);
	
#	�ŏ��̃y�[�W����ɂ���B$Form{lm}�͎c��
	$Form{page} = $Form{sort} = $Form{rev} = undef;
	
	&make_index_html() if ($MAKE_INDEX_SW);
}


##################################################
# �A�b�v���[�h�f�[�^�̊g���q�𓾂�

sub get_filetype {
	my ($uploadfile) = @_;
	my $suffix;
	
	# �g���q�蓮�I��
	if ($Form{suffix} =~ /^(\w+)$/) {
		$suffix = $1;
		return $suffix if (exists($MIMETYPE{$suffix}));
	}
	
	# ���[�J���̃t�@�C�����̊g���q
	if ($uploadfile->{basename} =~ /\.(\w+)$/) {
		$suffix = lc ($1);
		return $suffix if (exists($MIMETYPE{$suffix}));
	}
	
	# MIME�^�C�v����g���q�����肷��
	my $mime_type = $uploadfile->{mimetype};
	while (my($ext, $mime) = each (%MIMETYPE)) {
		next unless ($mime);
		return $ext if ($mime_type =~ /$mime/i);
	}
	return $DEF_EXT;	#�f�t�H���g
}


##################################################
# �L�^�t�@�C����ID�Ɗg���q����t�@�C�����𓾂�

sub getrenbanfilename {
	
	# ��������ĂȂ������ׂ�
	my $id     = $_[0] =~ /^(\d+)$/ ? $1 : return undef;
	my $suffix = $_[1] =~ /^(\w+)$/ ? $1 : return undef;
	
	return sprintf("%s%04d.%s", $PREFIX, $id, $suffix);
}


##################################################
# ���[�J���̃t�@�C��������t�@�C�������擾����
# ������Ė����������܂܂�Ă�����undef��Ԃ�

sub getuploadfilename {
	my ($filename, $suffix) = @_;
	
	if ($filename =~ /^(\w[\w\.\-]*)$/) {
		$filename = $1;
		
		# �g���q��}���ւ���
		$filename =~ s/\.+[^\.]*$//;
		
		# ��������t�@�C�����͓r���łԂ����؂�
		substr ($filename, $MAX_FILENAME_SIZE) = '' if (length ($filename) > $MAX_FILENAME_SIZE);
		
		# index.html�͂���
		return undef if ($filename =~ /^index$/i and $suffix =~ /^htm/i);
		
		return undef if ($PREFIX and $filename =~ /^$PREFIX/o);
		
		return "$filename.$suffix" unless -e "$STORE_DIR/$filename.$suffix";
		
		for (my $i=1; $i<=10; $i++) {
			return "$filename($i).$suffix" unless -e "$STORE_DIR/$filename($i).$suffix";
		}
	}
	return undef;
}


##################################################
# ���������N

sub autolink {
	my $s = shift;
	
	my $uric = '\w' . quotemeta(';/?:@=+$,%-.!~*\'()');	# &�͏��O�A_��\w�Ɋ܂܂��
	$uric .= '\#';	# flagment
	
	$$s =~ s{
		\b (?=[hfgmnt])						# �擪�̕������ǂ݂�����ƑI���������Ȃ�
		( (?:https?|ftp|gopher|mailto|news|nntp|telnet) :
		  [$uric]+ (?:&amp;[$uric]*)*  )	# & ��&amp;�ɃG�X�P�[�v����Ă���
	}{<a href="$1">$1</a>}gox;
}


##################################################
# �t�@�C���폜���[�h

sub delete {
	
	if ($Form{delpass} eq '') {
		print <<_EOF;
<h3>ID�F$Form{id}���폜���܂�</h3>
<form method="POST" action="$CGIURL">
<input type="hidden" name="m" value="D">
<input type="hidden" name="id" value="$Form{id}">
�p�X���[�h���́F<input type="password" size="10" name="delpass" value="@{[&htmlencode($Cookie{delpass})]}">
<input type="submit" value="�폜" class="button">
<input type="radio" name="isadmin" value="off" checked>�폜�p�X
<input type="radio" name="isadmin" value="on">�Ǘ��p�X
</form>
_EOF
	} else {
		
		unless ($Form{id} =~ /^\d+$/) { die ("ID�F$Form{id}��������܂���ł����B\n"); }
		
		my $newlogdata = '';
		
		open (LOG, "+< $LOG_FILE") or die ("Open Error $LOG_FILE: $!\n");
		eval { flock (LOG, 2) };
		
		my $flag;
		while (<LOG>) {
			if (/^\Q$Form{id}\E\t/o) {
				$flag++;
				my @field = split (/\t/, $_);
				if ($Form{isadmin} eq 'on') {
					my $adminpasswd;
					open (PASSWD, $ADMINPASSWD) or die ("Open Error $ADMINPASSWD: $!\n");
					chomp ($adminpasswd = <PASSWD>);
					close (PASSWD);
					die("�p�X���|�h���Ⴂ�܂��B\n") unless (&checkpassword($Form{delpass}, $adminpasswd));
				} else {
					die("�p�X���|�h���Ⴂ�܂��B\n") unless (&checkpassword($Form{delpass}, $field[7]));
				}
				
				&unlink_filedata (\@field);
				
				next;
			}
			$newlogdata .= $_;
		}
		unless ($flag) { die("ID�F$Form{id}��������܂���ł����B\n"); }
		
		seek (LOG, 0, 0);
		print LOG $newlogdata;
		truncate (LOG, tell(LOG));
		eval { flock (LOG, 8) };
		close (LOG);
		
		print "<h3>�t�@�C�����폜���܂����B</h3>\n";
		
		&make_index_html() if ($MAKE_INDEX_SW);
		
	}
	print "<a href=\"$CGIURL\">Return</a>\n";
}


##################################################
# �t�@�C�����폜

sub unlink_filedata {
	my $article = shift;
	
	my ($delsize, $delfile, $pchfile);
	
	$delsize = 0;
	($delfile) = $article->[2] =~ /^(\w[\w\.\-\(\)]*)$/ or return 0;
	
	if (-f "$STORE_DIR/$delfile") {
		$delsize += -s _;
		unlink ("$STORE_DIR/$delfile");
	}
	
	# imageinfo
	if ($article->[11] ne '' and $article->[11] =~ /^\d+:\d+:pch/) {
		($pchfile = $delfile) =~ s/\.+[^\.]*$/\.pch/;
		if (-f "$STORE_DIR/$pchfile") {
			$delsize += -s _;
			unlink ("$STORE_DIR/$pchfile");
		}
	}
	
	return ($delsize);
}


##################################################
# �p�X���[�h�Í���

sub encrypt {
	my $inpw = shift;
	
	my (@letters, $salt, $encrypt);
	@letters = ('a'..'z', 'A'..'Z', '0'..'9', '.', '/');
	srand;
	$salt = $letters[rand(@letters)] . $letters[rand(@letters)];
	$encrypt = crypt($inpw, $salt) || crypt ($inpw, '$1$' . $salt);
	return $encrypt;
}


##################################################
# �p�X���[�h�ƍ�

sub checkpassword {
	my ($inpw, $logpw) = @_;
	return undef if ($logpw eq '');
	return crypt($inpw, $logpw) eq $logpw;
}


##################################################
# �C���f�b�N�X�y�[�W�쐬
# ���Ȃ�K��

sub make_index_html {
	open (INDEXPAGE, "> $INDEX_FILEPATH") or die ("Open Error $INDEX_FILEPATH: $!\n");
	my $savefh = select (INDEXPAGE);
	
	# �ϐ�����������ޔ�������
	local ($COUNTFILE, %Form, %Cookie);
	
	&print_header('',1);
	&print_obititle();
	&list();
	&print_footer();
	
	select ($savefh);
	close (INDEXPAGE);
}


##################################################
# ���G�`���A�v���b�g�\��

sub print_canvas {
	
	my $width  = $Form{hsize} || $OEKAKI_DEF_SIZE;
	my $height = $Form{vsize} || $OEKAKI_DEF_SIZE;
	$width  = $OEKAKI_MAX_SIZE if ($width  > $OEKAKI_MAX_SIZE);
	$height = $OEKAKI_MAX_SIZE if ($height > $OEKAKI_MAX_SIZE);
	my $applet_width  = $width  + 120;
	my $applet_height = $height + 120;
	
	my $applet_params = '';
	for (sort keys (%APPLET_PARAMS)) {
		next if ($APPLET_PARAMS{$_} eq '');
		$applet_params .= qq|      <param name="$_" value="$APPLET_PARAMS{$_}">\n|;
	}
	
	my $notice_msg = '';
	if ($OEKAKI_ANIMATION and $Form{anime} eq 'on') {
		$applet_params .= qq|      <param name="thumbnail_type" value="animation">\n|;
		$notice_msg = qq|<tr><td colspan="2"><strong>�`��A�j���f�[�^�L�^��</strong></td></tr>\n|;
	}
	
	my $addoption = '';
	print <<_EOF;
<script type="text/javascript" src="$BASE_URL/palette.js" charset="Shift_JIS"></script>
<script type="text/javascript"><!--
  // PaintBBS�������̃^�C�~���O�ŌĂ΂��
  function paintBBSCallback(value) {
    if (value == "header") { //���M�O
      var pf = document.post_field;
      
      // String�I�u�W�F�N�g��錾���Ȃ��Ƒʖڂ炵��
      var postdata = new String();
      
      for (var i=0; i < pf.elements.length; i++) {
        if (pf.elements[i].name) {
          // IE3 NN2�œ����Ȃ����ǖ����R(�L�[�M)�m
          if (pf.elements[i].type == "select-one" || pf.elements[i].type == "select-multiple") {
            for (var j=0; j < pf.elements[i].options.length; j++) {
              if (pf.elements[i].options[j].selected)
                postdata += pf.elements[i].name + "=" + pf.elements[i].options[j].value + "&";
            }
            continue;
          }
          if (pf.elements[i].type == "checkbox" || pf.elements[i].type == "radio")
            if (!pf.elements[i].checked) continue;
          postdata += pf.elements[i].name + "=" + pf.elements[i].value + "&";
        }
      }
      
      return postdata;
    }
  }
  
  // escape()��Unicode�ɕϊ������΍�
  function url_encode(str) {
    var enc = ""
    for (var i=0; i<str.length; i++) {
      var c = str.substring(i, i+1);
      // ASCII�� 0-9 A-Z a-z �ȊO�A���{��̓X�L�b�v����
      if ( c <= "\057"
        || ("\072" <= c && c <= "\100")
        || ("\133" <= c && c <= "\140")
        || ("\173" <= c && c <= "\177")
      ) {
        enc += escape(c);
      } else {
        enc += c;
      }
    }
    return enc;
  }
//--></script>
<noscript>
  <h3>JavaScript���L���łȂ����߈ꕔ�@�\\������v���܂���B</h3>
</noscript>

<a href="$CGIURL">Return</a>

<hr>
<table border=0 cellspacing=0 cellpadding=0>
  <!-- �{�^���������ƁA���C�u�R�l�N�g���g����PaintBBS�̑��M���������� -->
  <script type="text/javascript"><!--
    document.write(
      '<tr><td colspan="2"><form name="post_field">'
    + '�R�����g<br>'
    + '<input type="text" size="60" name="comment" value="">'
    + '<input type="button" value=" Post " class="button" onClick="document.paintbbs.pExit()"><input type="reset" value="Cancel" class="button"><br>'
    + '<a href="$CGIURL?help=del">del pass</a>: <input type="password" size="10" name="delpass" maxlength="10" value="@{[&htmlencode($Cookie{delpass})]}">  '
    $addoption
    + '</form></td></tr>'
    );
  //--></script>
  
  $notice_msg
  
  <tr>
  <td valign="top">
    <applet name="paintbbs" code="pbbs.PaintBBS.class" codebase="$BASE_URL" archive="PaintBBS.jar"
            width="$applet_width" height="$applet_height" mayscript
            alt="���g�p�̃u���E�U��Java����A�N�e�B�u��ԂɂȂ��Ă��܂��B���̂��߃y�C���g�c�[�����\������܂���B">
      <param name="image_width"  value="$width">
      <param name="image_height" value="$height">
      <param name="image_jpeg" value="true">
      <param name="image_size"   value="65">
      <param name="compress_level" value="15">
      <param name="poo" value="false">
      <param name="send_header" value="">
      <param name="send_language" value="sjis">
      <param name="url_save" value="$CGIURL">
      <param name="url_exit" value="$CGIURL">
$applet_params
    </applet>
  </td>
  <td align="center" valign="top">
    <script type="text/javascript" charset="Shift_JIS"><!--
      PaletteInit();
    //--></script>
  </td>
  </tr>
  <tr>
    <td colspan="2"><br>
    <p>
      �~�X���ăy�[�W��ς�����E�C���h�E�������Ă��܂����肵���ꍇ�͗������ē����L�����o�X�̕���<br>
      �ҏW�y�[�W���J���Ȃ����Ă݂ĉ������B���͎c���Ă��܂��B<br>
      MacIE��l�X�P�S.*�̏ꍇ�̓u���E�U�̃E�C���h�E��S�ĕ��Ă��܂����畜���o���܂���j<br>
    </p>
    <p><a href="$BASE_URL/shiihelp.html" target="_blank">���G�`�������A�v���b�g�̎g����</a></p>
    </td>
  </tr>
</table>
_EOF
}


##################################################
# �L�����ꌏ����Ă���

sub get_article {
	
	my $number = shift;
	my ($flag, @msg);
	
	if ($number =~ /^\d+$/) {
		open (LOG, $LOG_FILE) or die ("Open Error $LOG_FILE: $!\n");
		eval { flock (LOG, 1) };
		while (<LOG>) {
			if (/^\Q$number\E\t/o) {
				chop;
				@msg = split (/\t/, $_);
				$flag = 1;
				last;
			}
		}
		eval { flock (LOG, 8) };
		close (LOG);
	}
	if (!$flag) { die("�Y���t�@�C����������܂���ł����B\n"); }
	
	return @msg;
}


##################################################
# PCH�A�j����`��

sub oekaki_movie {
	
	my ($id, $suffix, $filename, $dispname, $comment, $date, $size, $passwd, $host, $ua, $mimetype, $imageinfo)
	 = &get_article ($Form{id});
	
	my ($width, $height, $pch) = split (/:/, $imageinfo);
	unless ($pch eq 'pch') { die ("���̃t�@�C���ɂ̓A�j���f�[�^�͋L�^����Ă��܂���\n"); }
	
	my $pchfile;
	($pchfile = $filename) =~ s/\.+[^\.]*$/\.pch/;
	unless (-f "$STORE_DIR/$pchfile") { die ("���̃t�@�C���ɂ̓A�j���f�[�^�͋L�^����Ă��܂���\n"); }
	my $datasize = &ins_comma(-s _);
	
	$pchfile = $STORE_URL . $pchfile;
	
	print <<_EOF;
<a href="$CGIURL">Return</a>

<div align="center">
  <applet name="paintbbs" code="pbbs.PaintBBS.class" codebase="$BASE_URL" archive="PaintBBS.jar"
          width="$width" height="$height" mayscript
          alt="���g�p�̃u���E�U��Java����A�N�e�B�u��ԂɂȂ��Ă��܂��B���̂��߃y�C���g�c�[�����\������܂���B">
  <param name="image_width" value="$width">
  <param name="image_height" value="$height">
  <param name="viewer" value="true">
  <param name="pch_file" value="$pchfile">
  <param name="speed" value="10">
  </applet><br>
  <small>Data size : $datasize byte</small><br>
  
  <script type="text/javascript"><!--
  function setSpeed (f) {
    var s = f.speed;
    document.paintbbs.speed = parseInt(s.options[s.selectedIndex].value);
  }
  document.write (
      '<form>'
    + '  <small>�Đ����x '
    + '  <select name="speed">'
    + '    <option value="-1">�ő�</option>'
    + '    <option value="0">����</option>'
    + '    <option value="10" selected>����</option>'
    + '    <option value="80">�ݑ�</option>'
    + '    <option value="500">�X���[</option>'
    + '  </select>'
    + '  <input type="button" value="�ύX" class="button" onClick="setSpeed(this.form)" onKeyPress="setSpeed(this.form)">'
    + '  </small>'
    + '</form>'
  );
  //--></script>
  
  <br>
</div>
_EOF

}


##################################################
# CGI�t�H�[�����̎擾

sub read_cgistream {
	my ($content_type, $content_length, $url_encoded_data,
		$pair, $name, $value, $skip_jconv);
	
	$content_type   = $ENV{CONTENT_TYPE};
	$content_length = $ENV{CONTENT_LENGTH};
	
	if ($MAX_UPLOAD_SIZE and $content_length > $MAX_UPLOAD_SIZE*1024 + $MAX_COMMENT_SIZE) {
		die("���M�f�[�^�ʂ�����l�𒴂��Ă��܂��B\n");
	}
	
	if ($content_type =~ m|multipart/form-data|) {
		require 'multipart.pl';
		@UploadFiles = &multipart::get_multipart(\&storeformdata, $TMPDIR);
	} elsif ($OEKAKI_SW and $content_type eq 'application/octet-stream') {
		require 'getpic.pl';
		
		&getpic::change_error_content_type('application/octet-stream') if ($TEXT_BANNER);
		
		my $recv_thumbnail = $OEKAKI_ANIMATION ? 1 : 0;
		($url_encoded_data, @PictureFiles) =
			&getpic::getpics($recv_thumbnail, $TMPDIR);
		$skip_jconv++;
	} elsif (   $content_type eq ''
			 or	$content_type eq 'application/x-www-form-urlencoded') {
		if ($ENV{REQUEST_METHOD} eq 'POST') {
			read (STDIN, $url_encoded_data, $content_length);
		} else {
			$url_encoded_data = $ENV{QUERY_STRING};
		}
	} else {
		die("Invalid content type!\n");
	}
	
	if ($url_encoded_data ne '') {
		$url_encoded_data =~ tr/+/ /;
		
		foreach $pair ( split (/&/, $url_encoded_data) ) {
			($name, $value) =  split (/=/, $pair, 2);
			$name  =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
			$value =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
			
			&storeformdata($name, $value);
		}
	}
	
	# �����R�[�h�ϊ�
	# $Form{k}�ɓ��ꂽ�����������������Ă�����ϊ�������
	# ���ɕϊ���K�v�Ƃ��Ȃ����� $Form{k} �ɒl�����Ă��Ȃ�
	if (!$skip_jconv and $Form{k} ne '' and $Form{k} ne $MOJIBAKE_TAISAKU) {
		require 'jcode.pl';
		for (keys(%Form)){ &jcode::convert(\$Form{$_}, 'sjis'); }
	}
	
	&getcookie();
	
	if ($Form{act} eq 'Up/Reload') {
		# �`�F�b�N�{�b�N�X��ON�Ȃ�N�b�L�[��H�ׂ�
		if ($Form{cookie_ok}) {
			# �Ȃ񂩕�
			my $tmp = $Form{delpass};
			$tmp =~ s/&quot;/"/g;
			$tmp =~ s/&lt;/</g;
			$tmp =~ s/&gt;/>/g;
			$tmp =~ s/&amp;/&/g;
			&setcookie('delpass' => $tmp);
		# �`�F�b�N�{�b�N�X��OFF�Ȃ̂ɃN�b�L�[�����݂���Ƃ��̓N�b�L�[��j��
		} elsif (%Cookie) {	
			&setcookie();
		}
	}
}
sub storeformdata {
	my ($name, $value) = @_;
	
	return if ($value eq "");
	
	# ���s�R�[�h�𓝈ꂷ��
#	$value =~ s/\x0D\x0A/\n/g;
#	$value =~ tr/\x0D\x0A/\n\n/;
	
	$Form{$name} = &htmlencode(\$value);
}


##################################################
# �����񒆂�HTML�^�O�𖳌��ɂ���

sub htmlencode {
	my $thingy = shift;
	my $s = ref ($thingy) ? $thingy : \$thingy;
	$$s =~ s/&/&amp;/g;
	$$s =~ s/"/&quot;/g;
	$$s =~ s/</&lt;/g;
	$$s =~ s/>/&gt;/g;
	$$s =~ tr/\t\n\r//d;
	$$s;
}


##################################################
# URL�G���R�[�h

sub urlencode {
	my $thingy = shift;
	my $s = ref ($thingy) ? $thingy : \$thingy;
	$$s =~ s/(\W)/'%' . unpack('H2', $1)/eg;
	$$s;
}


##################################################
# COOKIE�𑗐M

sub setcookie {
	my ($cookie, $expday, $gmt, $path);
	
	if (@_ == 0) {
		$cookie = ''; $gmt = 'Fri, 27-Feb-1976 00:00:00 GMT';
		%Cookie = ();
	} else {
		my @week  = qw/Sun Mon Tue Wed Thu Fri Sat/;
		my @month = qw/Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec/;
		
		$expday = 60; # �N�b�L�[�̗L��������60����
		my @t = gmtime(time + $expday * 24 * 60 * 60);
		$gmt = sprintf("%s, %02d-%s-%04d %02d:%02d:%02d GMT",
			$week[$t[6]], $t[3], $month[$t[4]], $t[5]+1900, $t[2], $t[1], $t[0]);
		
		while (@_) {
			my $key = shift(@_);
			my $val = shift(@_);
			$cookie .= $key . '=' . &urlencode($val);
			$cookie .= '&' if (@_);
			$Cookie{$key} = $val;	# ���݂̒l�ɔ��f������
		}
	}
	if ($ENV{SCRIPT_NAME}) {
		$path = substr ($ENV{SCRIPT_NAME}, 0, rindex($ENV{SCRIPT_NAME}, "/")+1);
	}
	
	print "Set-Cookie: $COOKIE_NAME=$cookie; expires=$gmt" . ($path ? "; path=$path\n" : "\n");
}


##################################################
# COOKIE���擾

sub getcookie {
    
    if ($ENV{HTTP_COOKIE} =~ /(?:^|; *)$COOKIE_NAME=([^;]*)(?:;|$)/o) {
		foreach ( split(/&/, $1) ) {
			my ($key, $val) = split(/=/, $_, 2);
			$val =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
			$Cookie{$key} = $val;
		}
	}
}


##################################################
# �o�C�g�T�C�Y�ɒP�ʂ�t����

sub byte_calc {
	my ($n, $m, $unit);
	$n = shift; # KB
	
	if ($n >= 1000 * 1024) {
		$m = 1024 * 1024; $unit = 'GB';
	} elsif ($n >= 1000) {
		$m = 1024; $unit = 'MB';
	} else {
		$unit = 'KB'; $n = int($n);
	}
	if ($m) {
		$n /= $m;
		if ($n != int($n)) {	# ����
			$n = ($n < 100) ? sprintf("%.3g", $n) : int($n);
		}
	}
	return $n . $unit;
}


##################################################
# 3�����ƂɃR���}�ŋ�؂�

sub ins_comma {
	my $n = shift;
	$n =~ s/\G((?:^[-+])?\d{1,3})(?=(?:\d\d\d)+(?!\d))/$1,/g;
	$n;
}


##################################################
# �f�B�X�N�g�p��

sub disk_used {
	my $use;
	opendir (DIR, $STORE_DIR) or die("Open Error $STORE_DIR: $!\n");
	while (defined($_ = readdir(DIR))) {
		next if (/^\.\.?$/);
		next if (/\.tmp$/);		# tmp�t�@�C���̊g���q�ɋC�������ق�����������
		$use += -s $STORE_DIR . '/' . $_;
	}
	closedir (DIR);	
	return $use;
}


##################################################
# �����[�g�z�X�g���擾

my $RemoteHost;
sub getremotehost {
	unless ($RemoteHost) {
		$RemoteHost = $ENV{REMOTE_HOST} || $ENV{REMOTE_ADDR};
		if ($RemoteHost eq $ENV{REMOTE_ADDR}) {
			$RemoteHost = gethostbyaddr( pack("C4", split(/\./, $RemoteHost)) ,2) || $RemoteHost;
		}
	}
	$RemoteHost;
}


##################################################
# �A�����e����

sub renzoku_seigen {
	my ($myip, @list, $flag);
	$myip = $ENV{REMOTE_ADDR};
	
	open (RENZOKU, "+<$RENZOKU_FILE") or die("Open Error $RENZOKU_FILE: $!\n");
	eval{ flock (RENZOKU, 2) };
	
	my $limit = time - $RENZOKU_TIME;
	
	while (<RENZOKU>) {
		my ($ip, $t) = split(/:/, $_);
		chop($t);
		next if ($t <= $limit);
		
		$flag++ if ($myip eq $ip);
		push (@list, $_);
	}
	unless ($flag) { push (@list, join(':',$myip,time)."\n"); }
	
	seek (RENZOKU, 0, 0);
	print RENZOKU @list;
	truncate (RENZOKU, tell(RENZOKU));
	eval{ flock (RENZOKU, 8) };
	close (RENZOKU);
	
	return $flag;
}


##################################################
# �֎~�h���C�������ׂ� (return 1:�֎~�h���C��, 0:���̑�)

sub checkdomain {
	my ($domain, $host, $hostip, $ret);
	my $access_control_file = shift;
	
	open (AXSCTRL, $access_control_file) or die("Open Error $access_control_file: $!\n");
	while (<AXSCTRL>) {
		next if (/^#/ or /^$/);
		chomp;
		if (m#^(\d+\.\d+\.\d+\.\d+)(?:/(\d+))?$#) {
			my $mask  = $2;
			my $domip = &inetaddr2int($1);
			
			$hostip ||= &inetaddr2int($ENV{REMOTE_ADDR});
			
			if (defined($mask)) {
				$mask = ~((1<<(32-$mask))-1);
			} else {
				# ���ʃr�b�g��0�Ŗ��߂��Ă��邩���ׂ�
				$mask = ~0;
				foreach (0xFFFFFFFF, 0xFFFFFF, 0xFFFF, 0xFF) {
					unless ($domip & $_) {
						$mask = ~$_;
						last;
					}
				}
			}
			if (($hostip & $mask) == ($domip & $mask)) {# �w��IP
				close (AXSCTRL); return undef;
			}
		} else {
			$host ||= &getremotehost();
			if ($host =~ m#(^|\.)\Q${_}\E$#) {			# �w��h���C�����ŏI���z�X�g
				close (AXSCTRL); return undef;
			}
		}
	}
	close (AXSCTRL); return 1;
}
sub inetaddr2int {
	my $addr = shift;
	my @ip = split(/\./, $addr);
	((((($ip[0]<<8)+$ip[1])<<8)+$ip[2])<<8)+$ip[3];
}


##################################################
# �Q�Ɛ�𒲂ׂ�
sub checkreferer {
	my $rl_except = shift;
	
	my $referer = $ENV{HTTP_REFERER};
	$referer =~  s/%([0-9A-Fa-f][0-9A-Fa-f])/pack('H2', $1)/eg;
	
	for (@$rl_except) {
		return undef if ($referer =~ /\Q$_\E/);
	}
	return 1;
}


##################################################
# �J�E���^

sub counter {
	local ($@);
	open (COUNTER, "+< $COUNTFILE") or return "ERROR";
	
	eval{ flock (COUNTER, 2) };
	# �m���u���b�L���O�B�J�E���^���Ƃ��Ńu���b�N������̂��n���n�������Ǝv����
	# �ł�����ς��߂�
#	if (!eval{ flock(COUNTER, 6) } and !$@) { close (COUNTER); return "BUSY"; }
	
#	my $count = <COUNTER>;
	my ($count, $date);
	if (defined($_ = <COUNTER>)) {
		($count, $date) = split (/:/, $_);
	}
	unless ($date) {
		my @lt=localtime();
		$date = sprintf ("%d/%02d/%02d", $lt[5]+1900, $lt[4]+1, $lt[3]);
	}
	$count++;
	
	seek (COUNTER, 0, 0);
	print COUNTER "$count:$date";
	truncate (COUNTER, tell(COUNTER));
	eval{ flock (COUNTER, 8) };
	close (COUNTER);
	
	return "$date ���� $count";
}


##################################################
# �G���[�o��

sub cgidie {
	my $errmsg = join('<br>', @_);
	
	&print_header('�G���[');
	print "<h3>$errmsg</h3>\n<a href=\"$CGIURL\">Return</a>\n</body>\n</html>\n";
	exit;
}


##################################################
# �w���v�\��

sub help {
	
	my $help_genre = $Form{help};
	if ($help_genre eq 'file') {
		print "<h3>�Ή��t�@�C���t�H�[�}�b�g</h3>\n<p><tt>";
		my $i = 0;
		for (sort keys(%MIMETYPE)) {
			print "*.$_ ";
			print "<br>\n" if ((++$i % 12) == 0);
		}
		print "<br>\n</tt>\n���̑��̃t�@�C���t�H�[�}�b�g�͓��Ɏw��̖�������*.$DEF_EXT�Ƃ��ĕۑ�����܂��B<br></p>\n";
	} elsif ($help_genre eq 'del') {
		print <<_EOF;
<h3>���e�L���폜�p�X�ɂ���</h3>
<p>
���e�҂���X�����̓��e�L�����폜�������ꍇ�ɓ��͂��܂��B<br>
�p�X���[�h�����͂���Ȃ��܂ܓ��e���ꂽ�L���͊Ǘ��҂ɂ����폜�ł��Ȃ��Ȃ�܂��B<br>
�p�X���[�h�ɂ�10���������̉p���L�����w��ł��܂��B<br>
</p>
_EOF
	} elsif ($help_genre eq 'search') {
		print <<_EOF;
<h3>�����L�[���[�h�ɂ���</h3>
<p>
�L�[���[�h�́u���p�X�y�[�X�v�ŋ�؂��ĕ����w�肷�邱�Ƃ��ł��܂��B<br>
�L�[���[�h�ɔ��p�X�y�[�X���g�������Ƃ��͂��̃L�[���[�h�𔼊p�̃_�u���N�E�H�[�g�u"�v�Ŋ����Ă��������B<br>
�R�����g�ƃt�@�C�����̃t�B�[���h�Ƀ}�b�`���܂��B<br>
</p>
_EOF
	} elsif ($help_genre eq 'disk') {
		my $use = &disk_used();
		
		print <<_EOF;
<h3>�f�B�X�N�g�p��</h3>
<p>
���݂̃f�B�X�N�g�p�ʂ�${\(&byte_calc($use/1024))} (${\(&ins_comma($use))}�o�C�g)�ł��B<br>
_EOF
		if ($DISK_SPACE_MAX) {
			print "${\(&byte_calc($DISK_SPACE_MAX))} �𒴂���Ǝ����I�Ƀt�@�C�����폜����܂��B<br>\n";
		}
		print "</p>\n";
	}
	print "<a href=\"$CGIURL\">Return</a>\n";
}


##################################################
# �Ǘ��p�X�ݒ�

sub set_adimn_passwd {
	&print_header('�͂��߂܂���(^�D^)');
	
	if ($Form{admpass} ne '') {
		my $encrypt = &encrypt($Form{admpass});
		
		open (PASSWD, "> $ADMINPASSWD") or die("Open Error $ADMINPASSWD: $!\n");
		print PASSWD $encrypt;
		close (PASSWD);
		chmod (0600, $ADMINPASSWD);
		print "<h3>�p�X���[�h��ݒ肵�܂����B</h3>\n<a href=\"$CGIURL\">Return</a>\n";
	} else {
		print <<_EOF;
<h3>�p�X���[�h�ݒ���s���܂��B</h3>
���ꂩ��A�b�v���[�_�̊Ǘ��Ŏg�p����u�Ǘ��p�p�X���[�h�v����͂��Ă��������B<br>
<form action="$CGIURL" method="POST">
<input type="password" name="admpass" size=10>
<input type="submit" value="Set">
</form>
_EOF
	}
	&print_footer();
}


##################################################
# Main
# die ("���݃����e�i���X���ł��B\n");

if ($ACCESS_CONTROL ne '' and !&checkdomain($ACCESS_CONTROL)) {
	die("���Ȃ��ɂ̓A�N�Z�X����������܂���B\n");
}

# �{���ɂ��̃T�C�g����̗��q���֎~�������Ȃ�
# �����ԃA�N�Z�X���֎~����悤�ȏ����ɏ���������Ƃ�������
if (@EXCEPT_REFERER and !&checkreferer(\@EXCEPT_REFERER)) {
	print "Location: http://www5b.biglobe.ne.jp/~iwasas/pu/P-main.html\n\n";
	exit;
}

&read_cgistream();

if (!(-e $ADMINPASSWD) || -z _) {
	&set_adimn_passwd();
	exit;
}

#if ($MAKE_INDEX_SW && !(-e $INDEX_FILEPATH)) {
#	&make_index_html() 
#}

if (@UploadFiles) {
	&file_upload();
} elsif (@PictureFiles) {
	&oekaki_upload();
	print "Content-Type: text/plain\n\n", "ok\n";
	exit;
}
if ($OEKAKI_SW and $Form{m} eq 'E') {
	&print_header('���G�`��');
	&print_obititle('���G�`��');
	&print_canvas();
} elsif ($Form{m} eq 'I') {
	&print_header('�摜�{��');
	&print_obititle('�摜�{��');
	&image_view();
} elsif ($Form{m} eq 'S') {
	&print_header('�t�@�C������');
	&print_obititle('�t�@�C������');
	&search();
} elsif ($Form{m} eq 'D') {
	&print_header('�t�@�C���폜');
	&print_obititle('�t�@�C���폜');
	&delete();
} elsif ($Form{m} eq 'A') {
	&print_header('�`��A�j���[�V�����Đ�');
	&print_obititle('�`��A�j���[�V�����Đ�');
	&oekaki_movie();
} elsif ($Form{help} ne '') {
	&print_header('Notice�I');
	&help();
} else {
	&print_header();
	&print_obititle();
	&list();
}
&print_footer();
