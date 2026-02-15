# Circle Map Generator - Mobile Edition

A mobile application for creating map circles with specified radius and generating KMZ files for Google My Maps.

Built with Kivy for cross-platform mobile support (Android/iOS).

## Features

- 🔍 Search locations by name or enter coordinates manually
- 🗺️ Interactive map preview (optional, requires kivy-garden.mapview)
- ⭕ Add multiple circles with custom radius and colors
- 💾 Generate KMZ files with folder selection
- 📤 Direct link to upload to Google My Maps
- 📱 Mobile-optimized touch interface

## Running on Desktop (for testing)

### Requirements
- Python 3.8+
- Kivy 2.2.1

### Installation

```bash
# Install Kivy
pip install kivy==2.2.1

# Install map preview (optional)
pip install kivy-garden.mapview

# Run the app
python3 main.py
```

## Building for Android

### Option 1: GitHub Actions (Recommended)

The easiest way to build the Android APK is using GitHub Actions, which builds automatically in the cloud:

#### Steps:

1. **Create a GitHub Repository**
   ```bash
   cd /Users/Haungwei.Ng/Sandbox/Circle_Map_Mobile
   git init
   git add .
   git commit -m "Initial commit - Circle Map Generator Mobile"
   ```

2. **Push to GitHub**
   - Create a new repository on GitHub (e.g., `circle-map-mobile`)
   - Follow GitHub's instructions to push your local repository:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/circle-map-mobile.git
   git branch -M main
   git push -u origin main
   ```

3. **Automatic Build**
   - GitHub Actions will automatically start building the APK
   - Go to your repository → "Actions" tab
   - Wait for the build to complete (takes 10-20 minutes first time)

4. **Download the APK**
   - Click on the completed workflow run
   - Scroll down to "Artifacts"
   - Download "CircleMapGenerator-Android"
   - Extract the ZIP file to get the APK

5. **Install on Phone**
   - Transfer the APK to your phone
   - Enable "Install from Unknown Sources" in Android settings
   - Open the APK file to install

#### Manual Trigger

You can also manually trigger a build:
- Go to Actions tab → "Build Android APK"
- Click "Run workflow" → "Run workflow"

#### Create a Release

To create a release with the APK attached:
```bash
git tag v1.0.0
git push origin v1.0.0
```
The APK will be automatically attached to the GitHub release.

### Option 2: Local Build with Docker

If you have Docker installed:

```bash
# Pull buildozer Docker image
docker pull kivy/buildozer

# Build the APK
docker run -v "$PWD":/home/user/app kivy/buildozer android debug

# APK will be in bin/ folder
```

### Option 3: Linux Build

Buildozer works best on Linux. On Ubuntu/Debian:

```bash
# Install dependencies
sudo apt install -y python3-pip build-essential git openjdk-17-jdk

# Install buildozer
pip3 install buildozer

# Build APK
buildozer android debug

# APK will be in bin/ folder
```

## Transferring APK to Phone

### Method 1: USB Cable
1. Connect phone to computer via USB
2. Copy the APK file to your phone's Download folder
3. On phone, open Files app → Downloads → tap the APK

### Method 2: Cloud Storage
1. Upload APK to Google Drive, Dropbox, etc.
2. Download on your phone
3. Open and install

### Method 3: Direct Download
If you created a GitHub release, download directly on your phone:
- Open browser on phone
- Go to your GitHub repository releases
- Download the APK

## App Permissions

The app requires the following Android permissions:
- **Internet Access**: For location search (geocoding)
- **Storage**: To save KMZ files

## Usage

1. **Search Location**: Enter a place name and tap "Search"
   - Or enter coordinates manually
2. **Add Circles**: 
   - Set radius (meters/km/miles)
   - Choose line and fill colors
   - Adjust opacity
   - Tap "Add Circle"
3. **Generate KMZ**:
   - Tap "Generate & Save KMZ"
   - Choose folder to save
   - Tap "Open Google My Maps"
4. **Upload to Google**:
   - In Google My Maps, click "Import"
   - Select your KMZ file
   - Done!

## Troubleshooting

### Map not showing
- Install map widget: `pip install kivy-garden.mapview`
- Or use without map preview (core functionality still works)

### Build fails on macOS
- Use GitHub Actions (Option 1) - it builds on Linux automatically
- Or use Docker/Linux VM

### APK won't install on phone
- Enable "Install from Unknown Sources" in Android settings
- Check that you downloaded the APK (not the ZIP)

## Files

- `main.py` - Main application code
- `map_circle_tool.py` - Core circle generation logic
- `buildozer.spec` - Android build configuration
- `.github/workflows/build-android.yml` - GitHub Actions workflow

## License

Free to use and modify.

## Support

For issues or questions, create a GitHub issue in your repository.
