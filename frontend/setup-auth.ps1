# 🚀 Installation & Setup Script
# Run this to set up the RhythmLink frontend authentication system

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  RhythmLink Frontend - Authentication Setup" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the frontend directory
if (-not (Test-Path "package.json")) {
    Write-Host "❌ Error: package.json not found!" -ForegroundColor Red
    Write-Host "Please run this script from the frontend directory" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Found package.json" -ForegroundColor Green
Write-Host ""

# Step 1: Install Zustand
Write-Host "📦 Step 1: Installing dependencies..." -ForegroundColor Yellow
Write-Host "Installing Zustand for state management..." -ForegroundColor Gray
pnpm install zustand

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Step 2: Check .env.local
Write-Host "🔧 Step 2: Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env.local") {
    Write-Host "✓ .env.local file exists" -ForegroundColor Green
    $envContent = Get-Content ".env.local" -Raw
    if ($envContent -match "NEXT_PUBLIC_API_URL") {
        Write-Host "✓ API URL is configured" -ForegroundColor Green
    } else {
        Write-Host "⚠ Warning: NEXT_PUBLIC_API_URL not found in .env.local" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ .env.local file not found!" -ForegroundColor Red
    Write-Host "Please create .env.local with NEXT_PUBLIC_API_URL=http://localhost:8000" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Verify folder structure
Write-Host "📁 Step 3: Verifying folder structure..." -ForegroundColor Yellow
$requiredDirs = @(
    "src/types",
    "src/lib/api",
    "src/lib/utils",
    "src/store",
    "src/hooks",
    "src/components/ui",
    "src/modules/auth",
    "src/app/(public)/login",
    "src/app/(public)/register"
)

$allExist = $true
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "  ✓ $dir" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $dir missing!" -ForegroundColor Red
        $allExist = $false
    }
}
Write-Host ""

# Step 4: Summary
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Setup Summary" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

if ($allExist) {
    Write-Host "✅ All authentication files are in place!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Make sure Django backend is running on port 8000" -ForegroundColor White
    Write-Host "2. Run: pnpm dev" -ForegroundColor White
    Write-Host "3. Navigate to: http://localhost:3000/login" -ForegroundColor White
    Write-Host "4. Test login/register functionality" -ForegroundColor White
    Write-Host ""
    Write-Host "📚 Documentation:" -ForegroundColor Yellow
    Write-Host "See AUTHENTICATION_README.md for complete usage guide" -ForegroundColor White
} else {
    Write-Host "⚠ Some files are missing. Please check the setup." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Ready to start developing! 🎉" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
