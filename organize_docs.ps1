# PowerShell脚本：整理文档文件

# 定义文档分类
$docCategories = @{
    "project" = @(
        "DEVELOPMENT_PLAN.md",
        "WEEKLY_PLAN.md", 
        "WEEK3_PLAN.md",
        "DATA_ACCURACY_PLAN.md",
        "PROJECT_STRUCTURE.md",
        "PROGRESS_REPORT.md"
    )
    
    "guides" = @(
        "MANUAL_TEST_GUIDE.md",
        "QUICK_FIX_GUIDE.md",
        "FIX_DOCKER_PATH.md",
        "AUTOMATED_MONITOR_SETUP.md"
    )
    
    "reports" = @(
        "CODE_AUDIT_REPORT.md",
        "CODE_COMPLETENESS_CHECKLIST.md",
        "COMPLETE_DELIVERY_CHECKLIST.md",
        "PUSH_MECHANISM_ANALYSIS.md",
        "TEST_COMMIT_NOTIFICATION.md"
    )
    
    "development" = @(
        "GIT_BRANCH_MANAGEMENT.md",
        "GIT_COMMIT_ZH.md"
    )
    
    "knowledge" = @(
        "guardian-bot-manual.md",
        "valen-repo-template.md"
    )
}

# 需要保留在根目录的文件
$rootFiles = @(
    "README.md",
    "AGENTS.md",
    "BOOTSTRAP.md",
    "HEARTBEAT.md",
    "IDENTITY.md",
    "SOUL.md",
    "TOOLS.md",
    "USER.md"
)

Write-Host "开始整理文档文件..." -ForegroundColor Green
Write-Host ""

# 移动文档文件
foreach ($category in $docCategories.Keys) {
    $targetDir = "docs\$category"
    
    foreach ($file in $docCategories[$category]) {
        if (Test-Path $file) {
            $destination = "$targetDir\$file"
            
            # 如果目标文件已存在，添加序号
            $counter = 1
            $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file)
            $extension = [System.IO.Path]::GetExtension($file)
            
            while (Test-Path $destination) {
                $destination = "$targetDir\${baseName}_${counter}${extension}"
                $counter++
            }
            
            Move-Item $file $destination -Force
            Write-Host "移动: $file -> $destination" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "文档整理完成!" -ForegroundColor Green
Write-Host ""

# 显示整理结果
Write-Host "整理结果:" -ForegroundColor Cyan
Write-Host "---------"

Get-ChildItem docs -Recurse -File | ForEach-Object {
    $relativePath = $_.FullName.Substring((Get-Location).Path.Length + 1)
    Write-Host "  $relativePath"
}

Write-Host ""
Write-Host "保留在根目录的文件:" -ForegroundColor Cyan
Write-Host "-------------------"

foreach ($file in $rootFiles) {
    if (Test-Path $file) {
        Write-Host "  $file"
    }
}