from wxPython.wx import *
from wxPython.stc import *
import keyword, string

def stcstyle(stc,config,type="NULL"):
	stc.StyleClearAll()
	stc.SetCodePage(1)

	language = config.read_config("default_language")
	font = config.read_config("font_string")
	if font==None and language=='Korean': 
		font = 'gothic,times'
	elif font==None:
		font='times'
	font = font.replace(",","|")
	size = config.read_config("font_size")
	if size==None:
		size=12
	else:
		size=int(size)
		
	# Global default styles for all languages
	stc.StyleSetSpec(wxSTC_STYLE_DEFAULT,	 "face:%s,size:%d" % (font, size))
	stc.StyleSetSpec(wxSTC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%s,size:%d" % (font, size))
	stc.StyleSetSpec(wxSTC_STYLE_CONTROLCHAR, "face:%s" % font)
	stc.StyleSetSpec(wxSTC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
	stc.StyleSetSpec(wxSTC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
	stc.StyleSetSpec(wxSTC_STYLE_BRACEBAD,	"fore:#000000,back:#FF0000,bold")


	font_base="font:%s,size:%d" % (font, size)
	font_small="font:%s,size:%d" % (font, size)
	font_comment="font:%s,size:%d" % (font, size)
	font_code_comment_box=font_comment
	font_code_comment_line=font_comment
	font_code_comment_doc=font_comment
	font_text="font:%s,size:%d" % (font, size)
	font_text_comment="font:%s,size:%d" % (font, size)
	font_embedded_base="font:%s,size:%d" % (font, size)
	font_embedded_comment="font:%s,size:%d" % (font, size)
	font_monospace="font:%s,size:%d" % (font, size)
	colour_code_comment_box="fore:#007F00"
	colour_code_comment_line="fore:#007F00"
	colour_code_comment_doc="fore:#3F703F"
	colour_text_comment="fore:#0000FF,back:#D0F0D0"
	colour_other_comment="fore:#007F00"
	colour_embedded_comment="back:#E0EEFF"
	colour_embedded_js="back:#F0F0FF"
	colour_notused="back:#FF0000"
	colour_number="fore:#007F7F"
	colour_keyword="fore:#00007F"
	colour_string="fore:#7F007F"
	colour_char="fore:#7F007F"
	colour_operator="fore:#000000"
	colour_preproc="fore:#7F7F00"
	colour_error="fore:#FFFF00,back:#FF0000"

	if type=="PYTHON":
		stc.SetLexer(wxSTC_LEX_PYTHON)
		stc.SetKeyWords(0, string.join(keyword.kwlist))
		
		stc.StyleSetSpec(wxSTC_P_DEFAULT, "fore:#808080,face:%s,size:%d" % (font, size))
		stc.StyleSetSpec(wxSTC_P_COMMENTLINE, "fore:#007F00,face:%s,size:%d" % (font, size))
		stc.StyleSetSpec(wxSTC_P_NUMBER, "fore:#007F7F,size:%d" % size)
		stc.StyleSetSpec(wxSTC_P_STRING, "fore:#7F007F,face:%s,size:%d" % (font, size))
		stc.StyleSetSpec(wxSTC_P_CHARACTER, "fore:#7F007F,face:%s,size:%d" % (font, size))
		stc.StyleSetSpec(wxSTC_P_WORD, "fore:#00007F,bold,size:%d" % size)
		stc.StyleSetSpec(wxSTC_P_TRIPLE, "fore:#7F0000,size:%d" % size)
		stc.StyleSetSpec(wxSTC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%d" % size)
		stc.StyleSetSpec(wxSTC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%d" % size)
		stc.StyleSetSpec(wxSTC_P_DEFNAME, "fore:#007F7F,bold,size:%d" % size)
		stc.StyleSetSpec(wxSTC_P_OPERATOR, "bold,size:%d" % size)
		stc.StyleSetSpec(wxSTC_P_IDENTIFIER, "fore:#808080,face:%s,size:%d" % (font, size))
		stc.StyleSetSpec(wxSTC_P_COMMENTBLOCK, "fore:#7F7F7F,size:%d" % size)
		stc.StyleSetSpec(wxSTC_P_STRINGEOL, "fore:#000000,face:%s,back:#EOC0E0,eolfilled,size:%d" % (font, size))
	elif type=="PHP":
		stc.SetLexer(wxSTC_LEX_PHP)
		stc.SetKeyWords(0,"and argv as argc endwhile \
for break continue if else elseif endif do while return switch \
case function class new static define \
__LINE__ __FILE__ PHP_VERSION PHP_OS TRUE FALSE E_ERROR \
E_ALL E_WARNING E_PARSE E_NOTICE HTTP_COOKIE_VARS HTTP_GET_VARS HTTP_POST_VARS \
HTTP_POST_FILES HTTP_ENV_VARS HTTP_SERVER_VARS PHP_OS PHP_SELF PHP_VERSION \
int integer real double float string array object var")

		stc.StyleSetSpec(wxSTC_HPHP_DEFAULT, "back:#FFF8F8,eolfilled")
		stc.StyleSetSpec(wxSTC_HPHP_HSTRING, "fore:#E8C100,"+font_monospace+",back:#FFF8F8")
		stc.StyleSetSpec(wxSTC_HPHP_SIMPLESTRING, "fore:#E8C100,"+font_monospace+",back:#FFF8F8")
		stc.StyleSetSpec(wxSTC_HPHP_WORD, "fore:#00007F,bold,back:#FFF8F8")
		stc.StyleSetSpec(wxSTC_HPHP_NUMBER, "fore:#007F00,"+font_monospace+",back:#FFF8F8")
		stc.StyleSetSpec(wxSTC_HPHP_VARIABLE, "back:#FFF8F8")
		stc.StyleSetSpec(wxSTC_HPHP_COMMENT, "fore:#FF0000,"+font_comment+",back:#FFF8F8")
		stc.StyleSetSpec(wxSTC_HPHP_COMMENTLINE, "fore:#FF0000,"+font_comment+",back:#FFF8F8")
		stc.StyleSetSpec(wxSTC_HPHP_HSTRING_VARIABLE, "back:#FFF8F8,eolfilled")
		stc.StyleSetSpec(wxSTC_HPHP_OPERATOR, "fore:#000000,back:#FFF8F8")
	elif type=="CPP":
		stc.SetLexer(wxSTC_LEX_CPP)
		stc.SetKeyWords(0,"asm auto bool break case catch char class const const_cast continue \
default delete do double dynamic_cast else enum explicit export extern false float for \
friend goto if inline int long mutable namespace new operator private protected public \
register reinterpret_cast return short signed sizeof static static_cast struct switch \
template this throw true try typedef typeid typename union unsigned using \
virtual void volatile wchar_t while")

		stc.StyleSetSpec(wxSTC_C_DEFAULT,"fore:#808080")
		stc.StyleSetSpec(wxSTC_C_COMMENT,colour_code_comment_box+","+font_code_comment_box)
		stc.StyleSetSpec(wxSTC_C_COMMENTLINE,colour_code_comment_line+","+font_code_comment_line)
		stc.StyleSetSpec(wxSTC_C_COMMENTDOC,colour_code_comment_doc+","+font_code_comment_doc)
		stc.StyleSetSpec(wxSTC_C_NUMBER,colour_number)
		stc.StyleSetSpec(wxSTC_C_WORD,colour_keyword+",bold")
		stc.StyleSetSpec(wxSTC_C_STRING,colour_string)
		stc.StyleSetSpec(wxSTC_C_CHARACTER,colour_char)
		stc.StyleSetSpec(wxSTC_C_UUID,"fore:#804080")
		stc.StyleSetSpec(wxSTC_C_PREPROCESSOR,colour_preproc)
		stc.StyleSetSpec(wxSTC_C_OPERATOR,colour_operator+",bold")
		stc.StyleSetSpec(wxSTC_C_IDENTIFIER,"")
		stc.StyleSetSpec(wxSTC_C_STRINGEOL,"fore:#000000,"+font_monospace+",back:#E0C0E0,eolfilled")
		stc.StyleSetSpec(wxSTC_C_VERBATIM,"fore:#007F00,"+font_monospace+",back:#E0FFE0,eolfilled")
		stc.StyleSetSpec(wxSTC_C_REGEX,"fore:#3F7F3F,"+font_monospace+",back:#E0F0FF,eolfilled")
		stc.StyleSetSpec(wxSTC_C_COMMENTLINEDOC,colour_code_comment_doc+","+font_code_comment_doc)
		stc.StyleSetSpec(wxSTC_C_WORD2,"fore:#B00040")
		stc.StyleSetSpec(wxSTC_C_COMMENTDOCKEYWORD,"fore:#3060A0,"+font_code_comment_doc)
		stc.StyleSetSpec(wxSTC_C_COMMENTDOCKEYWORDERROR,"fore:#804020,"+font_code_comment_doc)
		
	else:
		stc.SetLexer(wxSTC_LEX_NULL)
	
	# refresh style
	"""
	stc.SetScrollWidth(stc.GetScrollWidth())
	stc.SetUseHorizontalScrollBar(True)
	stc.SetEndAtLastLine(1)
	"""

"""

// Lexical states for SCLEX_HTML, SCLEX_XML
#define wxSTC_H_DEFAULT 0
#define wxSTC_H_TAG 1
#define wxSTC_H_TAGUNKNOWN 2
#define wxSTC_H_ATTRIBUTE 3
#define wxSTC_H_ATTRIBUTEUNKNOWN 4
#define wxSTC_H_NUMBER 5
#define wxSTC_H_DOUBLESTRING 6
#define wxSTC_H_SINGLESTRING 7
#define wxSTC_H_OTHER 8
#define wxSTC_H_COMMENT 9
#define wxSTC_H_ENTITY 10

// XML and ASP
#define wxSTC_H_TAGEND 11
#define wxSTC_H_XMLSTART 12
#define wxSTC_H_XMLEND 13
#define wxSTC_H_SCRIPT 14
#define wxSTC_H_ASP 15
#define wxSTC_H_ASPAT 16
#define wxSTC_H_CDATA 17
#define wxSTC_H_QUESTION 18

// More HTML
#define wxSTC_H_VALUE 19

// X-Code
#define wxSTC_H_XCCOMMENT 20

// SGML
#define wxSTC_H_SGML_DEFAULT 21
#define wxSTC_H_SGML_COMMAND 22
#define wxSTC_H_SGML_1ST_PARAM 23
#define wxSTC_H_SGML_DOUBLESTRING 24
#define wxSTC_H_SGML_SIMPLESTRING 25
#define wxSTC_H_SGML_ERROR 26
#define wxSTC_H_SGML_SPECIAL 27
#define wxSTC_H_SGML_ENTITY 28
#define wxSTC_H_SGML_COMMENT 29
#define wxSTC_H_SGML_1ST_PARAM_COMMENT 30
#define wxSTC_H_SGML_BLOCK_DEFAULT 31

// Embedded Javascript
#define wxSTC_HJ_START 40
#define wxSTC_HJ_DEFAULT 41
#define wxSTC_HJ_COMMENT 42
#define wxSTC_HJ_COMMENTLINE 43
#define wxSTC_HJ_COMMENTDOC 44
#define wxSTC_HJ_NUMBER 45
#define wxSTC_HJ_WORD 46
#define wxSTC_HJ_KEYWORD 47
#define wxSTC_HJ_DOUBLESTRING 48
#define wxSTC_HJ_SINGLESTRING 49
#define wxSTC_HJ_SYMBOLS 50
#define wxSTC_HJ_STRINGEOL 51
#define wxSTC_HJ_REGEX 52

// ASP Javascript
#define wxSTC_HJA_START 55
#define wxSTC_HJA_DEFAULT 56
#define wxSTC_HJA_COMMENT 57
#define wxSTC_HJA_COMMENTLINE 58
#define wxSTC_HJA_COMMENTDOC 59
#define wxSTC_HJA_NUMBER 60
#define wxSTC_HJA_WORD 61
#define wxSTC_HJA_KEYWORD 62
#define wxSTC_HJA_DOUBLESTRING 63
#define wxSTC_HJA_SINGLESTRING 64
#define wxSTC_HJA_SYMBOLS 65
#define wxSTC_HJA_STRINGEOL 66
#define wxSTC_HJA_REGEX 67

// Embedded VBScript
#define wxSTC_HB_START 70
#define wxSTC_HB_DEFAULT 71
#define wxSTC_HB_COMMENTLINE 72
#define wxSTC_HB_NUMBER 73
#define wxSTC_HB_WORD 74
#define wxSTC_HB_STRING 75
#define wxSTC_HB_IDENTIFIER 76
#define wxSTC_HB_STRINGEOL 77

// ASP VBScript
#define wxSTC_HBA_START 80
#define wxSTC_HBA_DEFAULT 81
#define wxSTC_HBA_COMMENTLINE 82
#define wxSTC_HBA_NUMBER 83
#define wxSTC_HBA_WORD 84
#define wxSTC_HBA_STRING 85
#define wxSTC_HBA_IDENTIFIER 86
#define wxSTC_HBA_STRINGEOL 87

// Embedded Python
#define wxSTC_HP_START 90
#define wxSTC_HP_DEFAULT 91
#define wxSTC_HP_COMMENTLINE 92
#define wxSTC_HP_NUMBER 93
#define wxSTC_HP_STRING 94
#define wxSTC_HP_CHARACTER 95
#define wxSTC_HP_WORD 96
#define wxSTC_HP_TRIPLE 97
#define wxSTC_HP_TRIPLEDOUBLE 98
#define wxSTC_HP_CLASSNAME 99
#define wxSTC_HP_DEFNAME 100
#define wxSTC_HP_OPERATOR 101
#define wxSTC_HP_IDENTIFIER 102

// ASP Python
#define wxSTC_HPA_START 105
#define wxSTC_HPA_DEFAULT 106
#define wxSTC_HPA_COMMENTLINE 107
#define wxSTC_HPA_NUMBER 108
#define wxSTC_HPA_STRING 109
#define wxSTC_HPA_CHARACTER 110
#define wxSTC_HPA_WORD 111
#define wxSTC_HPA_TRIPLE 112
#define wxSTC_HPA_TRIPLEDOUBLE 113
#define wxSTC_HPA_CLASSNAME 114
#define wxSTC_HPA_DEFNAME 115
#define wxSTC_HPA_OPERATOR 116
#define wxSTC_HPA_IDENTIFIER 117


// Lexical states for SCLEX_PERL
#define wxSTC_PL_DEFAULT 0
#define wxSTC_PL_ERROR 1
#define wxSTC_PL_COMMENTLINE 2
#define wxSTC_PL_POD 3
#define wxSTC_PL_NUMBER 4
#define wxSTC_PL_WORD 5
#define wxSTC_PL_STRING 6
#define wxSTC_PL_CHARACTER 7
#define wxSTC_PL_PUNCTUATION 8
#define wxSTC_PL_PREPROCESSOR 9
#define wxSTC_PL_OPERATOR 10
#define wxSTC_PL_IDENTIFIER 11
#define wxSTC_PL_SCALAR 12
#define wxSTC_PL_ARRAY 13
#define wxSTC_PL_HASH 14
#define wxSTC_PL_SYMBOLTABLE 15
#define wxSTC_PL_REGEX 17
#define wxSTC_PL_REGSUBST 18
#define wxSTC_PL_LONGQUOTE 19
#define wxSTC_PL_BACKTICKS 20
#define wxSTC_PL_DATASECTION 21
#define wxSTC_PL_HERE_DELIM 22
#define wxSTC_PL_HERE_Q 23
#define wxSTC_PL_HERE_QQ 24
#define wxSTC_PL_HERE_QX 25
#define wxSTC_PL_STRING_Q 26
#define wxSTC_PL_STRING_QQ 27
#define wxSTC_PL_STRING_QX 28
#define wxSTC_PL_STRING_QR 29
#define wxSTC_PL_STRING_QW 30

// Lexical states for SCLEX_VB, SCLEX_VBSCRIPT
#define wxSTC_B_DEFAULT 0
#define wxSTC_B_COMMENT 1
#define wxSTC_B_NUMBER 2
#define wxSTC_B_KEYWORD 3
#define wxSTC_B_STRING 4
#define wxSTC_B_PREPROCESSOR 5
#define wxSTC_B_OPERATOR 6
#define wxSTC_B_IDENTIFIER 7
#define wxSTC_B_DATE 8

// Lexical states for SCLEX_PROPERTIES
#define wxSTC_PROPS_DEFAULT 0
#define wxSTC_PROPS_COMMENT 1
#define wxSTC_PROPS_SECTION 2
#define wxSTC_PROPS_ASSIGNMENT 3
#define wxSTC_PROPS_DEFVAL 4

// Lexical states for SCLEX_LATEX
#define wxSTC_L_DEFAULT 0
#define wxSTC_L_COMMAND 1
#define wxSTC_L_TAG 2
#define wxSTC_L_MATH 3
#define wxSTC_L_COMMENT 4

// Lexical states for SCLEX_LUA
#define wxSTC_LUA_DEFAULT 0
#define wxSTC_LUA_COMMENT 1
#define wxSTC_LUA_COMMENTLINE 2
#define wxSTC_LUA_COMMENTDOC 3
#define wxSTC_LUA_NUMBER 4
#define wxSTC_LUA_WORD 5
#define wxSTC_LUA_STRING 6
#define wxSTC_LUA_CHARACTER 7
#define wxSTC_LUA_LITERALSTRING 8
#define wxSTC_LUA_PREPROCESSOR 9
#define wxSTC_LUA_OPERATOR 10
#define wxSTC_LUA_IDENTIFIER 11
#define wxSTC_LUA_STRINGEOL 12
#define wxSTC_LUA_WORD2 13
#define wxSTC_LUA_WORD3 14
#define wxSTC_LUA_WORD4 15
#define wxSTC_LUA_WORD5 16
#define wxSTC_LUA_WORD6 17

// Lexical states for SCLEX_ERRORLIST
#define wxSTC_ERR_DEFAULT 0
#define wxSTC_ERR_PYTHON 1
#define wxSTC_ERR_GCC 2
#define wxSTC_ERR_MS 3
#define wxSTC_ERR_CMD 4
#define wxSTC_ERR_BORLAND 5
#define wxSTC_ERR_PERL 6
#define wxSTC_ERR_NET 7
#define wxSTC_ERR_LUA 8
#define wxSTC_ERR_CTAG 9
#define wxSTC_ERR_DIFF_CHANGED 10
#define wxSTC_ERR_DIFF_ADDITION 11
#define wxSTC_ERR_DIFF_DELETION 12
#define wxSTC_ERR_DIFF_MESSAGE 13

// Lexical states for SCLEX_BATCH
#define wxSTC_BAT_DEFAULT 0
#define wxSTC_BAT_COMMENT 1
#define wxSTC_BAT_WORD 2
#define wxSTC_BAT_LABEL 3
#define wxSTC_BAT_HIDE 4
#define wxSTC_BAT_COMMAND 5
#define wxSTC_BAT_IDENTIFIER 6
#define wxSTC_BAT_OPERATOR 7

// Lexical states for SCLEX_MAKEFILE
#define wxSTC_MAKE_DEFAULT 0
#define wxSTC_MAKE_COMMENT 1
#define wxSTC_MAKE_PREPROCESSOR 2
#define wxSTC_MAKE_IDENTIFIER 3
#define wxSTC_MAKE_OPERATOR 4
#define wxSTC_MAKE_TARGET 5
#define wxSTC_MAKE_IDEOL 9

// Lexical states for SCLEX_DIFF
#define wxSTC_DIFF_DEFAULT 0
#define wxSTC_DIFF_COMMENT 1
#define wxSTC_DIFF_COMMAND 2
#define wxSTC_DIFF_HEADER 3
#define wxSTC_DIFF_POSITION 4
#define wxSTC_DIFF_DELETED 5
#define wxSTC_DIFF_ADDED 6

// Lexical states for SCLEX_CONF (Apache Configuration Files Lexer)
#define wxSTC_CONF_DEFAULT 0
#define wxSTC_CONF_COMMENT 1
#define wxSTC_CONF_NUMBER 2
#define wxSTC_CONF_IDENTIFIER 3
#define wxSTC_CONF_EXTENSION 4
#define wxSTC_CONF_PARAMETER 5
#define wxSTC_CONF_STRING 6
#define wxSTC_CONF_OPERATOR 7
#define wxSTC_CONF_IP 8
#define wxSTC_CONF_DIRECTIVE 9

// Lexical states for SCLEX_AVE, Avenue
#define wxSTC_AVE_DEFAULT 0
#define wxSTC_AVE_COMMENT 1
#define wxSTC_AVE_NUMBER 2
#define wxSTC_AVE_WORD 3
#define wxSTC_AVE_KEYWORD 4
#define wxSTC_AVE_STATEMENT 5
#define wxSTC_AVE_STRING 6
#define wxSTC_AVE_ENUM 7
#define wxSTC_AVE_STRINGEOL 8
#define wxSTC_AVE_IDENTIFIER 9
#define wxSTC_AVE_OPERATOR 10

// Lexical states for SCLEX_ADA
#define wxSTC_ADA_DEFAULT 0
#define wxSTC_ADA_COMMENT 1
#define wxSTC_ADA_NUMBER 2
#define wxSTC_ADA_WORD 3
#define wxSTC_ADA_STRING 4
#define wxSTC_ADA_CHARACTER 5
#define wxSTC_ADA_OPERATOR 6
#define wxSTC_ADA_IDENTIFIER 7
#define wxSTC_ADA_STRINGEOL 8

// Lexical states for SCLEX_BAAN
#define wxSTC_BAAN_DEFAULT 0
#define wxSTC_BAAN_COMMENT 1
#define wxSTC_BAAN_COMMENTDOC 2
#define wxSTC_BAAN_NUMBER 3
#define wxSTC_BAAN_WORD 4
#define wxSTC_BAAN_STRING 5
#define wxSTC_BAAN_PREPROCESSOR 6
#define wxSTC_BAAN_OPERATOR 7
#define wxSTC_BAAN_IDENTIFIER 8
#define wxSTC_BAAN_STRINGEOL 9
#define wxSTC_BAAN_WORD2 10

// Lexical states for SCLEX_LISP
#define wxSTC_LISP_DEFAULT 0
#define wxSTC_LISP_COMMENT 1
#define wxSTC_LISP_NUMBER 2
#define wxSTC_LISP_KEYWORD 3
#define wxSTC_LISP_STRING 6
#define wxSTC_LISP_STRINGEOL 8
#define wxSTC_LISP_IDENTIFIER 9
#define wxSTC_LISP_OPERATOR 10

// Lexical states for SCLEX_EIFFEL and SCLEX_EIFFELKW
#define wxSTC_EIFFEL_DEFAULT 0
#define wxSTC_EIFFEL_COMMENTLINE 1
#define wxSTC_EIFFEL_NUMBER 2
#define wxSTC_EIFFEL_WORD 3
#define wxSTC_EIFFEL_STRING 4
#define wxSTC_EIFFEL_CHARACTER 5
#define wxSTC_EIFFEL_OPERATOR 6
#define wxSTC_EIFFEL_IDENTIFIER 7
#define wxSTC_EIFFEL_STRINGEOL 8

// Lexical states for SCLEX_NNCRONTAB (nnCron crontab Lexer)
#define wxSTC_NNCRONTAB_DEFAULT 0
#define wxSTC_NNCRONTAB_COMMENT 1
#define wxSTC_NNCRONTAB_TASK 2
#define wxSTC_NNCRONTAB_SECTION 3
#define wxSTC_NNCRONTAB_KEYWORD 4
#define wxSTC_NNCRONTAB_MODIFIER 5
#define wxSTC_NNCRONTAB_ASTERISK 6
#define wxSTC_NNCRONTAB_NUMBER 7
#define wxSTC_NNCRONTAB_STRING 8
#define wxSTC_NNCRONTAB_ENVIRONMENT 9
#define wxSTC_NNCRONTAB_IDENTIFIER 10

// Lexical states for SCLEX_MATLAB
#define wxSTC_MATLAB_DEFAULT 0
#define wxSTC_MATLAB_COMMENT 1
#define wxSTC_MATLAB_COMMAND 2
#define wxSTC_MATLAB_NUMBER 3
#define wxSTC_MATLAB_KEYWORD 4
#define wxSTC_MATLAB_STRING 5
#define wxSTC_MATLAB_OPERATOR 6
#define wxSTC_MATLAB_IDENTIFIER 7

// Lexical states for SCLEX_SCRIPTOL
#define wxSTC_SCRIPTOL_DEFAULT 0
#define wxSTC_SCRIPTOL_COMMENT 1
#define wxSTC_SCRIPTOL_COMMENTLINE 2
#define wxSTC_SCRIPTOL_COMMENTDOC 3
#define wxSTC_SCRIPTOL_NUMBER 4
#define wxSTC_SCRIPTOL_WORD 5
#define wxSTC_SCRIPTOL_STRING 6
#define wxSTC_SCRIPTOL_CHARACTER 7
#define wxSTC_SCRIPTOL_UUID 8
#define wxSTC_SCRIPTOL_PREPROCESSOR 9
#define wxSTC_SCRIPTOL_OPERATOR 10
#define wxSTC_SCRIPTOL_IDENTIFIER 11
#define wxSTC_SCRIPTOL_STRINGEOL 12
#define wxSTC_SCRIPTOL_VERBATIM 13
#define wxSTC_SCRIPTOL_REGEX 14
#define wxSTC_SCRIPTOL_COMMENTLINEDOC 15
#define wxSTC_SCRIPTOL_WORD2 16
#define wxSTC_SCRIPTOL_COMMENTDOCKEYWORD 17
#define wxSTC_SCRIPTOL_COMMENTDOCKEYWORDERROR 18
#define wxSTC_SCRIPTOL_COMMENTBASIC 19
"""
