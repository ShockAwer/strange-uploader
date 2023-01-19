  STRANGE UPLOADER
                                   December 23, 2002 version



The log format has changed since the November 19, 2002 edition.
  You need to convert the log format when migrating from the November 17, 2002 version or earlier.


In creating this script, we have referred to many scripts including Zurbonaproda.
I would like to thank all the people who made them available. I would like to thank all the people who made them available to the public.


Outline
  This is a CGI script that provides a kind of simple disk space.

Bugs
  When an uploaded file name contains characters whose second byte is 0x5C (\) (in Shift-JIS) such as "so", "ten", "table", etc.
    character (in Shift JIS) such as "so", "ten", "table", etc., the file name is displayed with the character before the character broken.
    (When $LOCAL_FILENAME_SW is 1 or 2)

History
  December 23, 2002
    Support for drawing animation
    Italicized the drawing data in the list to make it easier to distinguish.
    Added page links to the bottom of the page
    Various other modifications

  December 21, 2002
    added a separate file for settings
    Fixed a bug in the log search, and changed the search condition (AND/OR) to be selectable.
    added a configuration item for drawing applet design
    added access restrictions to gw.cgi

  2002.12.14.
    fixed a bug in style sheet selection script

  2002.12.12.
    Supported Opera7 in the style sheet selection script

  2002.11.29
    Minimum size of uploaded files can now be specified
    Created a converter to convert from Zurbonaproda logs

  November 25, 2002
    fixed a strange part of automatic link
    fixed the problem of drawing error processing on infoseek and other servers that include banners even if they are text/plain
    Fixed a serious bug about automatic index page creation

  November 21, 2002
    Changed the name to STRANGE UPLOADER
    Fixed a bug.

  November 19, 2002
    modified the file name can be uploaded as local file name (when the file name is alphanumeric characters and - _ . )
    changed log format accordingly

  November 17, 2002
    added a function to create an index page
    modified to work correctly when taint check (-T option of Perl) is working

  Nov. 15, 2002
    Fixed a bug in the style sheet selection script

  November 11, 2002
    Fixed a bug on access restriction

  2002.11.07
    Fixed a bug that a half-finished file is recorded when interrupted during transmission
    Introduced stylesheet selection script

  2002.11.03
    added drawing function

  2001.11.01
    modified gw.cgi
    fixed a few bugs

  2002.10.27
    Open to the public


Terms of Use

  This script is free software.
  You can use it freely for personal or corporate use, commercial or non-commercial use.
  However, the copyright is not abandoned (^Д^)

  You are free to modify and redistribute this script.

  The author is not responsible for any damage caused by the use of this script.
  Use at your own risk.

  All rights to the following programs included in this archive belong to their respective authors.
  Please follow the terms and conditions of use.

    PaintBBS
    Shi-chan http://www.gt.sakura.ne.jp/~ocosama/

    DynamicPalette (palette.js)
    Noraneko-san http://wondercatstudio.com/

    jcode.pl
    Kazumasa Utashiro http://srekcah.org/jcode/


About the author
  Chinen <chinen@yasashiku.site.ne.jp>
  http://yasashiku.site.ne.jp/uploader/
