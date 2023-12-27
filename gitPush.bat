@echo off  
chcp 65001
  
for /L %%i in (1,1,100) do (  
    echo 正在执行第 %%i 次推送...  
    git push  
)  
  
echo 所有推送完成！  
pause