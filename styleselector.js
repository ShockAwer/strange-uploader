/* 
 *  ��փX�^�C���V�[�g�؂�ւ��X�N���v�g
 *
 *  �EIE4�ȍ~�ŃX�^�C���V�[�g�؂�ւ��@�\������������
 *  �E�܂��A��փX�^�C���V�[�g�̋@�\��L���Ă���u���E�U�ł͂��̎g����������コ����
 *
 *  �Q�lURL
 *  http://critical.s6.xrea.com/web/cssselect.shtml
 *  http://east.portland.ne.jp/~sigekazu/css/javascript9.htm
 */

/****************************************************************
  �g����
  
    �ʏ�g�p����X�^�C��
    <link rel="stylesheet" href="normal.css" type="text/css" title="�ʏ�g�p">
    
    ��փX�^�C����񋓂���
    <link rel="alternate stylesheet" href="alter1.css" type="text/css" title="��փX�^�C��1">
    <link rel="alternate stylesheet" href="alter2.css" type="text/css" title="��փX�^�C��2">
    
    �^�C�g�������������Ȃ��Ƌ��ʂ̃X�^�C��
    <link rel="stylesheet" href="common.css" type="text/css">
    
    ���̃X�N���v�g��LINK�v�f�̌�ŌĂяo��
    <script type="text/javascript" src="styleselector.js" charset="Shift_JIS"></script>
    
    �؂�ւ��t�H�[����t�������ꏊ�ɂ��������
    <script type="text/javascript"><!--
      writeCSSSelectForm('�f�U�C���ύX');
    // --></script>

*******************************************************************/

var cdays, cpath, cname, sheet, enableflag, isMozilla;
cdays = 30;		// �N�b�L�[�̕ۑ�����
				// 0�Ȃ�u���E�U���I��������܂ł��L�������ƂȂ�܂��B
cpath = "";		// �N�b�L�[�̗L���ɂ���T�C�g�̃p�X��
				// ��Ȃ�A�N�b�L�[��ݒ肵���y�[�W�̃p�X�����ɂȂ�܂��B
cname = "StyleSheet";

sheet      = "";
enableflag = 0;
isMozilla  = navigator.product == "Gecko";


// �N�b�L�[����X�^�C����ǂݍ���
function initStyle () {
	if (sheet && isExistsCSS(sheet)) {
		changeCSS(sheet);
	}
}


// CSS�̃��X�g�̒��ɑ��݂��邩���ׂ�
function isExistsCSS (ssTitle) {
	
	if (!ssTitle) return false;
	
	var ss =
		(enableflag > 1) ? document.styleSheets :
			document.all ? document.all.tags('LINK') : document.getElementsByTagName('LINK');
	
	for (var i=0; i<ss.length; i++) {
		if (ss[i].type == "text/css" && ss[i].title == ssTitle)
			return true;
	}
	return false;
}


// �X�^�C���V�[�g��؂�ւ���
function changeCSS (ssTitle) {
//	if (!ssTitle) return;
	
	var ss =
		(enableflag > 1) ? document.styleSheets :
			document.all ? document.all.tags('LINK') : document.getElementsByTagName('LINK');
	
	// title�����l��ssTitle�Ȃ�X�^�C���V�[�g��L����
	// title�����̗^�����Ă��Ȃ��O���X�^�C���V�[�g�͏�ɗL���i��΂����ق������������H�j
	for (var i=0; i<ss.length; i++) {
		if (ss[i].type != "text/css") continue;
		ss[i].disabled = (!ss[i].title || ss[i].title == ssTitle) ? false : true;
	}
	
	setCookie(cname, ssTitle);
	sheet = ssTitle;
}


// �X�^�C���V�[�g�؂�ւ��t�H�[�����I�����ꂽ
function selectCSSEvent (obj) {
	changeCSS(obj.value);
	window.focus();
}


// �X�^�C���V�[�g�I���t�H�[�����o�͂���
function writeCSSSelectForm (label) {
	
	if (enableflag) {
		var html = label + ' <select name="selectss" onChange="selectCSSEvent(this);">';
		
		var ss =
			(enableflag > 1) ? document.styleSheets :
				document.all ? document.all.tags('LINK') : document.getElementsByTagName('LINK');
		
		for (var i=0; i<ss.length; i++) {
			if ((ss[i].type != "text/css") || (!ss[i].title)) continue;
			html += '<option value="'
				  + ss[i].title
				  + ((ss[i].title == sheet) ? '" selected="selected">' : '">')
				  + ss[i].title
				  + '</option>';
		}
		html += '</select>';
		document.write('<div align="right">', html, '</div>');
	}
}


// �u���E�U�̃��j���[����X�^�C���V�[�g��I�тȂ����Ă����Ɉ����p�����悤��
// ���ݓK�p����Ă���X�^�C���V�[�g���N�b�L�[�ɕۑ�����
function savePresentSheet () {
	if (!sheet) return;
	
	var ss =
		(enableflag > 1) ? document.styleSheets :
			document.all ? document.all.tags('LINK') : document.getElementsByTagName('LINK');
	
	var present_sheets;
	for (var i=0; i<ss.length; i++) {
		if (ss[i].type != "text/css") continue;
		if ((!ss[i].disabled) && (ss[i].title)) {
			present_sheets = ss[i].title;
			break;
		}
	}
	if (present_sheets != sheet)
		setCookie(cname, present_sheets);
}


// �N�b�L�[���擾
function getCookie (key) {
	var tmp, kstart, vstart, pos;
	
	tmp = document.cookie + ";";
	kstart = 0;
	vstart = key.length + 1;
	while (vstart < tmp.length) {
		pos = tmp.indexOf(";", vstart);
		if (pos == -1) break;
		
		if (tmp.substring(kstart, vstart) == key + "=")
			return (unescape(tmp.substring(vstart, pos)));
		else
			for (pos++; (pos < tmp.length) && (tmp.charAt(pos) == " "); pos++) ;
		kstart = pos;
		vstart = kstart + key.length + 1;
	}
	return("");
}


// �N�b�L�[��ݒ�
function setCookie (key, val) {
	var exp = new Date();
	
	if (val != "")
		exp.setTime(exp.getTime() + cdays*24*60*60*1000);
	else
		exp.setTime(exp.getTime() - 24*60*60*1000);
	
	document.cookie = key + "=" + escape(val)
		+ ((cdays != 0) ? ("; expires=" + exp.toGMTString()) : '')
		+ ((cpath != "") ? ("; path=" + cpath) : '');
}


// document.styleSheets��document.all.tags('LINK')�Ŏ擾����LINK�v�f��disabled�v���p�e�B��
// �ύX���邱�ƂŃX�^�C���V�[�g��؂�ւ��邱�Ƃ��ł���
//
// WinIE�ł́A��`���ꂽLINK�v�f�͂��ׂėL����(disabled=false)�Ȃ��Ă��܂��炵���̂�
// document.styleSheets���g��Ȃ���΂Ȃ�Ȃ��B
// �������AMacIE4.0�͑�փX�^�C���V�[�g��F�����Ȃ��̂ŏ��O����
// MacIE4.5��styleSheets.title���擾�ł��Ȃ��̂ŏ��O����
//
// Mozilla�ł͓ǂݍ��݊����O��document.styleSheets���擾���Ă��܂��Ƒ�փX�^�C���V�[�g��
// �������܂܂�Ă��Ȃ��s���S�ȃR���N�V�������Q�Ƃ�������ꍇ������炵���B
// �����document.all.tags("LINK")���g���B
// if (document.styleSheets) �̂悤�ɘ_���l�Ƃ��ĕ]������\���ł͖��Ȃ��B
//
// Opera7�ł�document.styleSheets�͒�`����ĂȂ����Adocument.all.tags("LINK")�̕���
// ���Ȃ��̂ł�����g���B
// Opera6�ł�disabled�v���p�e�B���ǂݏo����p�Ȃ̂Ŏ��s�ł��Ȃ�

// enableflag = 1 �̎��Adocument.all.tags('LINK')
// enableflag = 2 �̎��Adocument.styleSheets
var ua = navigator.userAgent;

if (document.styleSheets) {
	if (isMozilla)
		enableflag = 1;
	else if (!(ua.indexOf('MSIE 4.') > -1 && ua.indexOf('Mac') > -1))
		enableflag = 2;
} else if (ua.match && ua.match(/Opera[ \/]+(\d+)\./i)) {
	if (RegExp.$1 >= 7)
		enableflag = 1;
}

if (enableflag) {
	
	sheet = getCookie('StyleSheet');
	if (sheet == 'undefined') sheet = "";
	
	if (isMozilla) {
		// meta�v�f�Ŋ���̃X�^�C����ݒ肷��
		if (sheet && isExistsCSS(sheet)) {
			document.write('<meta http-equiv="Default-Style" content="'+ sheet +'">');
		}
		window.onload = initStyle;
	} else {
		initStyle();
	}
	window.onunload = savePresentSheet;
}

