# 📱 Quick Start: Get Your App on Your Phone

Follow these simple steps to build your Android APK using GitHub Actions:

## ✅ Step-by-Step Checklist

### 1. Initialize Git Repository (if not done)
```bash
cd /Users/Haungwei.Ng/Sandbox/Circle_Map_Mobile
git init
```

### 2. Add All Files
```bash
git add .
git commit -m "Initial commit - Circle Map Generator Mobile App"
```

### 3. Create GitHub Repository
- Go to https://github.com/new
- Repository name: `circle-map-mobile` (or any name you like)
- Keep it **Public** (required for free GitHub Actions)
- **Don't** initialize with README (we already have one)
- Click "Create repository"

### 4. Push to GitHub
Replace `YOUR_USERNAME` with your GitHub username:
```bash
git remote add origin https://github.com/YOUR_USERNAME/circle-map-mobile.git
git branch -M main
git push -u origin main
```

### 5. Watch the Build
- Go to your repository on GitHub
- Click the "Actions" tab
- You'll see "Build Android APK" running
- Wait 10-20 minutes for first build (cached builds are faster)

### 6. Download the APK
Once build is complete:
- Click on the successful workflow run
- Scroll to bottom → "Artifacts" section
- Click "CircleMapGenerator-Android" to download
- Unzip the downloaded file to get the `.apk`

### 7. Install on Your Phone

**Option A: USB Cable**
- Connect phone to Mac with USB cable
- Copy the APK to your phone's Downloads folder
- On phone: Files app → Downloads → tap the APK

**Option B: AirDrop (macOS to iPhone won't work, Android only)**
- If you have AirDrop alternatives for Android, use that

**Option C: Cloud Upload**
- Upload APK to Google Drive
- Download on your phone
- Install from Downloads

**Option D: Email/Messaging**
- Email the APK to yourself
- Open email on phone
- Download and install

### 8. Enable Installation (First Time Only)
When installing:
- Android will ask to "Allow from this source"
- Enable it temporarily
- Install the app
- You can disable it after installation

### 9. Open and Use! 🎉
- The app icon will appear in your app drawer
- Open "Circle Map Generator"
- Start creating circles!

---

## 🔄 For Future Updates

When you make changes to the app:

```bash
cd /Users/Haungwei.Ng/Sandbox/Circle_Map_Mobile
git add .
git commit -m "Description of your changes"
git push
```

GitHub Actions will automatically build a new APK. Download it from the Actions tab.

---

## 🏷️ Creating Releases (Optional but Nice)

To create version releases with APKs attached:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Then:
- Go to your repo → Releases
- The APK will be automatically attached
- Share the release link with others!

---

## ❓ Need Help?

If the build fails:
- Check the Actions tab for error logs
- Common issues:
  - `buildozer.spec` syntax errors
  - Missing dependencies (check the workflow file)
  - First build always takes longest (15-20 min)

---

## 📊 What's Happening Behind the Scenes?

GitHub Actions uses:
- Ubuntu Linux environment
- Installs buildozer and Android SDK
- Compiles your Python/Kivy app to Android APK
- Packages everything into an installable APK
- All for free! (Public repos get free build minutes)

---

**You're all set! Start with Step 1 above. 🚀**
