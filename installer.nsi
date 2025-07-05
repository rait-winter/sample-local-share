!define APPNAME "�����ļ���Ϣ����"
!define COMPANY "YourCompany"
!define VERSION "1.0.0"
!define EXE_NAME "app.exe"

SetCompressor lzma
Name "${APPNAME} ${VERSION}"
OutFile "�����ļ���Ϣ����װ��.exe"
InstallDir "$PROGRAMFILES\\${APPNAME}"
RequestExecutionLevel admin

Page directory
Page instfiles

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "backend\\dist\\app.exe"
  File /r "backend\\dist\\assets"
  File "backend\\dist\\index.html"
  File "backend\\dist\\icon.svg"
  File "backend\\dist\\vite.svg"
  File /nonfatal /r "backend\\dist\\uploads"
  File /nonfatal /r "backend\\dist\\videos"
  # �������������ļ���������� File /r ...

  CreateShortCut "$DESKTOP\\${APPNAME}.lnk" "$INSTDIR\\app.exe"
  CreateShortCut "$SMPROGRAMS\\${APPNAME}.lnk" "$INSTDIR\\app.exe"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\\${APPNAME}.lnk"
  Delete "$INSTDIR\\app.exe"
  RMDir /r "$INSTDIR\\assets"
  Delete "$INSTDIR\\index.html"
  Delete "$INSTDIR\\icon.svg"
  Delete "$INSTDIR\\vite.svg"
  RMDir /r "$INSTDIR\\uploads"
  RMDir /r "$INSTDIR\\videos"
  RMDir "$INSTDIR"
SectionEnd