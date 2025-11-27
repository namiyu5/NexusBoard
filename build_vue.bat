@echo off
cd C:\Users\iahme\OneDrive\Belgeler\vscode-projects\NexusBoard\nexusboard_vue
npm run build
xcopy /E /I /Y dist C:\Users\iahme\OneDrive\Belgeler\vscode-projects\NexusBoard\nexusboard_django\static
echo Vue build copied to Django static folder!
