def trans(key, Language):
	translate = {
		"ProgramTitle": {
			"Korean":"ExmanIDE",
			"English":"ExmanIDE",
			},
		"Menu_File_Exit": {
			"Korean":"종료(&x)",
			"English":"E&xit",
			},
		"Menu_File_Exit_Status": {
			"Korean":"ExmanIDE을 종료 합니다",
			"English":"Exit from ExmanIDE",
			},
		"Menu_File": {
			"Korean":"파일(&F)",
			"English":"&File",
			},
		"Menu_File_New": {
			"Korean":"새 파일(&N)",
			"English":"&New",
			},
		"Menu_File_Save": {
			"Korean":"저장 하기(&S)",
			"English":"&Save",
			},

		"Menu_File_SaveAs": {
			"Korean":"다른 이름으로(&a)",
			"English":"Save &As",
			},
		"Menu_File_Open": {
			"Korean":"열기(&O)",
			"English":"&Open",
			},
		"Menu_File_Directory_Open": {
			"Korean":"디렉토리 열기",
			"English":"Open Directory",
			},
		"Menu_File_RecentFile": {
			"Korean":"최근 열어본 파일...",
			"English":"Open recent file...",
			},
		"Menu_File_RecentDir": {
			"Korean":"최근 열어본 디렉토리...",
			"English":"Open recent directory...",
			},
		"Menu_File_RecentProject": {
			"Korean":"최근 열어본 프로젝트...",
			"English":"Open recent Project...",
			},
		"Menu_File_Directory_Close": {
			"Korean":"디렉토리 닫기",
			"English":"Close Directory",
			},
		"Menu_File_Project_New": {
			"Korean":"새 프로젝트",
			"English":"New Project",
			},
		"Menu_File_Project_Open": {
			"Korean":"프로젝트 열기(&P)",
			"English":"Open &Project",
			},
		"Menu_File_Project_Close": {
			"Korean":"프로젝트 닫기",
			"English":"Close Project",
			},
		"Menu_File_Project_Configurator": {
			"Korean":"프로젝트 설정...",
			"English":"Project Configurator...",
			},
		"Menu_File_Project_File_New": {
			"Korean":"새 파일 추가",
			"English":"Add New File",
			},
		"Menu_Edit": {
			"Korean":"편집",
			"English":"Edit",
			},
		"Menu_Edit_Preference": {
			"Korean":"환경 설정...",
			"English":"Preference...",
			},
		"Menu_Edit_Undo": {
			"Korean":"실행 취소\tCtrl-Z",
			"English":"Undo\tCtrl-Z",
			},
		"Menu_Edit_Redo": {
			"Korean":"다시 실행\tCtrl-Y",
			"English":"Redo\tCtrl-Y",
			},
		"Menu_Edit_Cut": {
			"Korean":"자르기\tCtrl-X",
			"English":"Cut\tCtrl-X",
			},
		"Menu_Edit_Copy": {
			"Korean":"복사하기\tCtrl-C",
			"English":"Copy\tCtrl-C",
			},
		"Menu_Edit_Paste": {
			"Korean":"붙이기\tCtrl-V",
			"English":"Paste\tCtrl-V",
			},
		"Menu_Edit_SelectAll": {
			"Korean":"모두 선택\tCtrl-A",
			"English":"Select All\tCtrl-A",
			},
		"Menu_Edit_Find": {
			"Korean":"찾기\tCtrl-F",
			"English":"Search\tCtrl-F",
			},
		"Menu_Edit_Replace": {
			"Korean":"바꾸기\tCtrl-R",
			"English":"Replace\tCtrl-R",
			},
		"Menu_Edit_Goto": {
			"Korean":"줄 이동\tCtrl-G",
			"English":"Go to line\tCtrl-G",
			},
		"Menu_Build": {
			"Korean":"빌드(&B)",
			"English":"&Debug",
			},
		"Menu_Build_Compile": {
			"Korean":"컴파일\tF7",
			"English":"Compile\tF7",
			},
		"Menu_Build_Execute": {
			"Korean":"실행\tCtrl-F5",
			"English":"E&xecute\tCtrl-F5",
			},
		"Menu_Build_Execute_Stop": {
			"Korean":"중단\tShift-F5",
			"English":"Stop\tShift-F5",
			},
		"Menu_Debug": {
			"Korean":"디버그(&D)",
			"English":"&Debug",
			},
		"Menu_Debug_Execute": {
			"Korean":"시작\tF5",
			"English":"E&xecute\tF5",
			},
		"Menu_Debug_Execute_Stop": {
			"Korean":"중단\tShift-F5",
			"English":"Stop\tShift-F5",
			},
		"Menu_Debug_Next": {
			"Korean":"다음\tF10",
			"English":"Step Over\tF10",
			},
		"Menu_Debug_Step": {
			"Korean":"들어가기\tF11",
			"English":"Step\tF11",
			},
		"Menu_Debug_Arguments": {
			"Korean":"아규먼트 설정...",
			"English":"Arguments...",
			},
		"Menu_Help_About": {
			"Korean":"ExmanIDE 대하여",
			"English":"About ExmanIDE",
			},
		"Menu_Help_About_Status": {
			"Korean":"ExmanIDE 대하여",
			"English":"What about ExmanIDE?",
			},
		"Menu_Help": {
			"Korean":"도움말(&H)",
			"English":"&Help",
			},
		"OpenProjects": {
			"Korean":"열린 프로젝트들",
			"English":"Open Projects",
			},
		"SaveChangesTo": {
			"Korean":"바뀐 파일내용을 저장하시겠습니까?",
			"English":"Save Changes to this file?",
			},
		"DontCloseForDebug": {
			"Korean":"디버그 중에는 종료할수 없습니다.",
			"English":"When debugging, you don't close this program.",
			},
		"ModifyVariable": {
			"Korean":"변수 값 변경",
			"English":"Modify this variable's value",
			},
		"CloseFile": {
			"Korean":"닫기",
			"English":"Close",
			},
		"Noname": {
			"Korean":"제목 없음",
			"English":"No name",
			},
		"NoSelectedFile": {
			"Korean":"열린 파일이 없습니다.",
			"English":"File is not opened",
			},
		"AlreadyOpenedFile": {
			"Korean":"이미 열려 있는 파일입니다.",
			"English":"This file was already opened.",
			},
		"Signal": {
			"Korean":"시그널",
			"English":"Signal",
			},
		"SIGHUP": {
			"Korean":"터미널로 부터 접속이 끊어졌을때 (T)",
			"English":"Hangup detected on controlling terminal or death of controlling process",
			},
		"SIGINT": {
			"Korean":"키보드로 부터의 인터럽트 (T)",
			"English":"Interrupt from keyboard",
			},
		"SIGQUIT": {
			"Korean":"키보드로 부터 종료 (C)",
			"English":"Quit from keyboard",
			},
		"SIGILL": {
			"Korean":"적합하지 않은 하드웨어 제어 (C)",
			"English":"Illegal Instruction",
			},
		"SIGABRT": {
			"Korean":"abort() 함수 호출시 (C)",
			"English":"Abort signal from abort()",
			},
		"SIGFPE": {
			"Korean":"부동소수 예외 (C)",
			"English":"Floating point exception",
			},
		"SIGKILL": {
			"Korean":"프로세스 종료 (T)",
			"English":"Kill signal",
			},
		"SIGSEGV": {
			"Korean":"잘못된 메모리 참조 (C)",
			"English":"Invalid memory reference",
			},
		"SIGPIPE": {
			"Korean":"깨진 파이프에 쓰기를 시도할때 (T)",
						   "English":"Broken pipe: write to pipe with no readers",
			},
		"SIGALRM": {
			"Korean":"alarm()에 의해 호출되는 타이머 (T)",
			"English":"Timer signal from alarm()",
			},
		"SIGTERM": {
			"Korean":"프로세스 강제 종료 (T)",
			"English":"Termination signal",
			},
		"SIGUSR1": {
			"Korean":"사용자 정의 1 (T)",
			"English":"User-defined signal 1",
			},
		"SIGUSR2": {
			"Korean":"사용자 정의 2 (T)",
			"English":"User-defined signal 2",
			},
		"SIGCHLD": {
			"Korean":"자식프로세스가 종료됨 (I)",
			"English":"Child stopped or terminated",
			},
		"SIGCONT": {
			"Korean":"정지된 프로세스를 시작",
			"English":"Continue if stopped",
			},
		"SIGSTOP": {
			"Korean":"프로세스 중지 (S)",
			"English":"Stop process",
			},
		"SIGTSTP": {
			"Korean":"tty에서 프로세스 중지 (S)",
			"English":"Stop typed at tty",
			},
		"SIGTTIN": {
			"Korean":"백그라운드 프로세스를 위한 tty 입력 (S)",
			"English":"tty input for background process",
			},
		"SIGTTOU": {
			"Korean":"백그라운드 프로세스를 위한 tty 출력 (S)",
			"English":"tty output for background process",
			},
		"SIGBUS": {
			"Korean":"잘못된 메모리 참조에 의한 BUS에러 (C)",
			"English":"Bus error (bad memory access)",
			},
		"SIGPOLL": {
			"Korean":"SIGIO와 유사한 Pollable event (T)",
			"English":"Pollable event (Sys V). Synonym of SIGIO",
			},
		"SIGPROF": {
			"Korean":"timer 가 만료되었을때 (T)",
			"English":"Profiling timer expired",
			},
		"SIGSYS": {
			"Korean":"Bad argument to routine (SVID) (C)",
			"English":"Bad argument to routine (SVID)",
			},
		"SIGTRAP": {
			"Korean":"Trace/break trapo (C)",
			"English":"Trace/breakpoint trap",
			},
		"SIGURG": {
			"Korean":"소켓의 긴급상황 (I)",
			"English":"Urgent condition on socket (4.2 BSD)",
			},
		"SIGVTALRM": {
			"Korean":"가상 알람시계 (T)",
			"English":"Virtual alarm clock (4.2 BSD)",
			},
		"SIGXCPU": {
			"Korean":"CPU 시간제한 초과 (C)",
			"English":"CPU time limit exceeded (4.2 BSD)",
			},
		"SIGXFSZ": {
			"Korean":"파일사이즈 제한 초과 (C)",
			"English":"File size limit exceeded (4.2 BSD)",
			},
		"SIGIOT": {
			"Korean":"SIGABRT와 유사한 IOT trap (C)",
			"English":"IOT trap. A synonym for SIGABRT",
			},
		"SIGIO": {
			"Korean":"I/O 가능할때 (T)",
			"English":"I/O now possible (4.2 BSD)",
			},
		"SIGCLD": {
			"Korean":"SIGCHLD와 유사 (I)",
			"English":"A synonym for SIGCHLD",
			},
		"SIGPWR": {
			"Korean":"전원 이상 (T)",
			"English":"Power failure (System V)",
			},
		"Apply": {
			"Korean":"적용",
			"English":"Apply",
			},
		"OK": {
			"Korean":"확인",
			"English":"OK",
			},
		"Cancel": {
			"Korean":"취소",
			"English":"Cancel",
			},
		"Back": {
			"Korean":"이전",
			"English":"Back",
			},
		"Skip": {
			"Korean":"무시",
			"English":"Skip",
			},
		"Next": {
			"Korean":"다음",
			"English":"Next",
			},
		"Finish": {
			"Korean":"마침",
			"English":"Finish",
			},
		"ProjectType": {
			"Korean":"프로젝트 유형",
			"English":"Project Type",
			},
		"Project": {
			"Korean":"프로젝트",
			"English":"Project",
			},
		"Project_Custom": {
			"Korean":"사용자 정의",
			"English":"Custom",
			},
		"ProjectSetting": {
			"Korean":"프로젝트 설정",
			"English":"Project Setting",
			},
		"ProjectName": {
			"Korean":"프로젝트명",
			"English":"Project name",
			},
		"ProjectDir": {
			"Korean":"프로젝트 디렉토리",
			"English":"Project directory",
			},
		"ProjectVersion": {
			"Korean":"프로젝트 버전",
			"English":"Version number",
			},
		"ProjectAuthor": {
			"Korean":"만든이",
			"English":"Author",
			},
		"ProjectAuthorEmail": {
			"Korean":"E-mail",
			"English":"E-mai",
			},
		"ProjectHomepage": {
			"Korean":"홈페이지",
			"English":"homepage",
			},
		"FailtoMakeProject": {
			"Korean":"프로젝트를 생성하는데 실패하였습니다.",
			"English":"Fail to make project.",
			},
		"AlreadyProjectDir": {
			"Korean":"이미 프로젝트 디렉토리가 존재합니다.\n이곳에 프로젝트를 생성 하시겠습니까?",
			"English":"This project already exists.\nWould you like to create project at this directory?",
			},
		"SourceHeaderTemplate": {
			"Korean":"소스코드 헤더 템플릿",
			"English":"Header template fo source code",
			},
		"RefreshDir": {
			"Korean":"새로고침",
			"English":"Reload",
			},
		"NotOpenProject": {
			"Korean":"열린 프로젝트가 없습니다.",
			"English":"Any project was not opened.",
			},
		"Sections": {
			"Korean":"분류",
			"English":"Sections",
			},
		"Env_Common": {
			"Korean":"공통",
			"English":"Common",
			},
		"Env_Editor": {
			"Korean":"에디터",
			"English":"Editor",
			},
		"Env_Debugger": {
			"Korean":"디버거",
			"English":"Debugger",
			},
		"LanguageSetting": {
			"Korean":"언어 설정",
			"English":"Language Setting",
			},
		"ChangeToRestart": {
			"Korean":"변경된 언어설정은 ExmanIDE가 재시작 된 후 적용됩니다.",
			"English":"Change to language take effect when you restart ExmanIDE",
			},
		"SplashWindow": {
			"Korean":"스플래시 윈도우",
			"English":"Splash Window",
			},
		"WhenStartingShowSplash": {
			"Korean":"시작할때 스플래시 윈도우를 보여줍니다.",
			"English":"When starting a ExmanIDE, shows the Splash Window.",
			},
		"PythonBinPath": {
			"Korean":"Python 경로",
			"English":"Python Path",
			},
		"PythonFileNotExist": {
			"Korean":"지정한 Python 실행파일이 존재하지 않습니다.",
			"English":"Python file does not exist.",
			},
		"ForSpeedLocalsOff": {
			"Korean":"디버그 속도 향상을 위해 Locals 탭을 보이지 않게 합니다.",
			"English":"For the speed improvement of the debugger\nit does not show the Locals tab.",
			},
		"view_witespace": {
			"Korean":"공백 표시",
			"English":"Witespace",
			},
		"view_endofline": {
			"Korean":"줄바꿈 표시",
			"English":"End of line",
			},
		"view_indentationguide": {
			"Korean":"들여쓰기 표시",
			"English":"Indentation guide",
			},
		"view_linenumber": {
			"Korean":"줄번호",
			"English":"Line number",
			},
		"view_margin": {
			"Korean":"디버그 마크를 위한 여백",
			"English":"Margin for debug mark",
			},
		"view_foldmargin": {
			"Korean":"소스 접기 마크를 위한 여백",
			"English":"Fold margin",
			},
		"view_tabsize": {
			"Korean":"탭 사이즈",
			"English":"Tab size",
			},
		"view_usetabs": {
			"Korean":"들여쓰기에 탭을 사용함",
			"English":"Indentation will use tab characters",
			},
		"view_autoindent": {
			"Korean":"자동 들여쓰기",
			"English":"Auto Indentation",
			},
		"about_author": {
			"Korean":"만든이: 박준철 (jooncheol@gmail.com)",
			"English":"Author: Park joon cheol (jooncheol@gmail.com)",
			},
		"about_license": {
			"Korean":"라이센스: GNU GPL V2",
			"English":"License: GNU GPL V2",
			},
		"about_thankto": {
			"Korean":"Thanks to: 한국 파이썬 사용자 모임 (http://www.python.or.kr)",
			"English":"Thanks to: Python Users' Group in Korea (http://www.python.or.kr)",
			},
		"about_version": {
			"Korean":"ExmanIDE 버전: ",
						   "English":"ExmanIDE Version: ",
			},
		"find_text": {
			"Korean":"찾을 문자열",
			"English":"Find Text",
			},
		"find_matchcase": {
			"Korean":"대소문자 구별",
			"English":"Match upper/lower case",
			},
		"find_wholeword": {
			"Korean":"완전히 일치하는 단어만",
			"English":"Match whole word only",
			},
		"find_regexp": {
			"Korean":"정규 표현식",
			"English":"Regular expression",
			},
		"find_reverse": {
			"Korean":"거꾸로 찾기",
			"English":"Reverse direction",
			},
		"find": {
			"Korean":"찾기",
			"English":"Find",
			},
		"NoSearchWord": {
			"Korean":"검색어를 찾을 수 없습니다.",
			"English":"Search word not found",
			},
		"Replace": {
			"Korean":"바꾸기",
			"English":"Replace",
			},
		"ReplaceAll": {
			"Korean":"모두 바꾸기",
			"English":"Replace All",
			},
		"replace_text": {
			"Korean":"바꿀 문자열",
			"English":"Replace with",
			},
		"WouldYouUpdate": {
			"Korean":"새 버전의 ExmanIDE가 나왔습니다.\n지금 바로 업그레이드 하시겠습니까?",
			"English":"The new version ExmanIDE is available now.\nWould you like to upgrade now?",
			},
		"YouMustRestartForUpgrade": {
			"Korean":"업그레이드가 완료 되었습니다.\nExmanIDE를 다시 시작하십시오.",
			"English":"Upgrade completed.\nYou must restart your ExmanIDE.",
			},
		"SetUsingUpdater": {
			"Korean":"시작할때 실시간 업데이터 자동 실행",
			"English":"When starting a ExmanIDE, execute the real time updater.",
			},
		"RealTimeUpdater": {
			"Korean":"실시간 업데이터",
			"English":"Real time updater",
			},
		"Menu_Help_Upgrade": {
			"Korean":"업그레이드...",
			"English":"Upgrade...",
			},
		"Menu_Help_BugIdea": {
			"Korean":"버그,의견 올리기",
			"English":"Submit Bug,Idea",
			},
		"Menu_Help_Homepage": {
			"Korean":"홈페이지",
			"English":"Homepage",
			},
		"NOBROWSER": {
			"Korean":"기본 브라우져가 없거나 웹브라우져를 실행 할 수 없습니다.",
			"English":"Can't find default browser.",
			},
		"GotoLine": {
			"Korean":"GotoLine",
			"English":"Goto line",
			},
		"GotoLineTitle": {
			"Korean":"이동할 줄번호를 입력하십시오.",
			"English":"Enter the line number.",
			},
		"font_setting": {
			"Korean":"폰트 설정",
			"English":"Font",
			},
		"font_size": {
			"Korean":"폰트 크기",
			"English":"Font size",
			},
		"Menu_Debug_Build_Command": {
			"Korean":"빌드 명령어",
			"English":"Build command",
			},
		"Menu_Debug_Exec_Command": {
			"Korean":"실행 명령어",
			"English":"Command for execution",
			},
		"": {
			"Korean":"",
			"English":"",
			},
		"": {
			"Korean":"",
			"English":"",
			},
		"": {
			"Korean":"",
			"English":"",
			},
		"": {
			"Korean":"",
			"English":"",
			},
	}
	try:
		str = translate[key][Language]
	except KeyError:
		str = "***"
	return str
