#! /usr/local/bin/perl
#
# �肾���ꂭ���[
#
# �g�p���@
#   r.cgi?�]����URL �ŌĂяo��
#
my $url = $ENV{QUERY_STRING} || "http://$ENV{SERVER_NAME}/";
$url =~ s/&/&amp;/g;
$url =~ s/</&lt;/g;
$url =~ s/>/&gt;/g;

print <<_EOF;
Content-Type: text/html; charset=Shift_JIS
Content-Language: ja

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html lang="ja">
<head>
<meta http-equiv="Content-type" content="text/html; charset=Shift_JIS">
<meta http-equiv="Refresh" content="0;URL=$url">
<title>�肾���ꂭ���[</title>
</head>

<body bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">
<p>
 $url �ɓ]�����Á����R(�L�[�M)�m
</p>
</body>
</html>
_EOF
