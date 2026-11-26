; Inno Setup 6: tạo dist\OCRDashboard-Setup.exe từ dist\OCRDashboard\ (chạy qua build.bat, không gọi tay).
; File này phải lưu UTF-8 CÓ BOM (tên shortcut tiếng Việt).
;
; - Cài cho người dùng hiện tại, không cần quyền Administrator: %LOCALAPPDATA%\Programs\OCRDashboard
; - KHÔNG tạo .env hay data: lần đầu chạy OCRDashboard.exe mới tạo ở %LOCALAPPDATA%\OCRDashboard
; - Gỡ cài đặt chỉ xóa chương trình, giữ nguyên .env và dữ liệu
; - GIỮ NGUYÊN AppId qua các bản: cài bản mới sẽ ghi đè bản cũ thay vì cài thành 2 chương trình

#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif

[Setup]
AppId={{68BD003B-EE5E-4E53-9624-6EBE2FCCADF1}
AppName=OCR Dashboard
AppVersion={#AppVersion}
AppPublisher=Phòng Kỹ thuật
DefaultDirName={localappdata}\Programs\OCRDashboard
DefaultGroupName=OCR Dashboard
DisableProgramGroupPage=yes
DisableDirPage=yes
PrivilegesRequired=lowest
OutputDir=dist
OutputBaseFilename=OCRDashboard-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\OCRDashboard.exe
CloseApplications=yes

[Tasks]
Name: "desktopicon"; Description: "Tạo shortcut ngoài Desktop"

[Files]
Source: "dist\OCRDashboard\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[InstallDelete]
; cài đè bản mới: xóa thư viện của bản cũ để không lẫn file cũ (KHÔNG đụng tới %LOCALAPPDATA%\OCRDashboard)
Type: filesandordirs; Name: "{app}\_internal"

[Icons]
Name: "{group}\OCR Dashboard"; Filename: "{app}\OCRDashboard.exe"
Name: "{group}\Sửa cấu hình (.env)"; Filename: "{app}\OCRDashboard.exe"; Parameters: "config"
Name: "{group}\Xem log (trực tiếp)"; Filename: "{app}\OCRDashboard.exe"; Parameters: "logs -f"
Name: "{group}\Gỡ cài đặt OCR Dashboard"; Filename: "{uninstallexe}"
Name: "{autodesktop}\OCR Dashboard"; Filename: "{app}\OCRDashboard.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\OCRDashboard.exe"; Description: "Chạy OCR Dashboard ngay (lần đầu sẽ mở file cấu hình để điền)"; Flags: nowait postinstall skipifsilent
