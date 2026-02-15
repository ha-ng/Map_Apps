================================================================
   CIRCLE MAP GENERATOR - MOBILE EDITION
================================================================

📱 **ANDROID & iOS APPLICATION**

Create map circles on your phone or tablet and export to KMZ
files for Google My Maps!

================================================================
✨ FEATURES
================================================================

🗺️ **Mobile-Optimized Interface**
   - Touch-friendly controls
   - Scrollable layout for small screens
   - Portrait orientation optimized
   - Responsive design

📍 **Location Services**
   - Search by place name (OpenStreetMap)
   - Manual coordinate entry
   - GPS location support (coming soon)
   - Interactive map preview (optional)

⭕ **Circle Creation**
   - Multiple circles per location
   - Flexible radius units (meters, km, miles)
   - Customizable colors (line and fill)
   - Adjustable opacity (0-100%)
   - Real-time preview

💾 **KMZ Export**
   - Save to device storage
   - Share via any app
   - Import to Google My Maps
   - Compatible with Google Earth

================================================================
📋 SYSTEM REQUIREMENTS
================================================================

**Android:**
- Android 5.0 (Lollipop) or higher (API 21+)
- ~50 MB storage space
- Internet connection (for location search)
- Optional: GPS for location services

**iOS:**
- iOS 11.0 or higher
- ~50 MB storage space
- Internet connection (for location search)
- Optional: Location services permission

**Desktop Testing:**
- Python 3.7+
- Windows, macOS, or Linux
- For development and testing before mobile build

================================================================
🚀 QUICK START
================================================================

**Option 1: Install Pre-built APK (Android)**
----------------------------------------------
1. Download CircleMapGenerator.apk
2. Enable "Install from Unknown Sources" in Settings
3. Tap the APK file to install
4. Open the app and start creating circles!

**Option 2: Test on Desktop**
------------------------------
1. Install Python 3.7+ and pip
2. Run: pip install kivy Pillow requests
3. Run: python main.py
4. Test the app before building mobile version

**Option 3: Build from Source**
--------------------------------
See BUILD_INSTRUCTIONS.txt for detailed steps

================================================================
📖 HOW TO USE
================================================================

**1. Set Your Location**
   
   Search Method:
   - Tap "Search Location" field
   - Type place name (e.g., "Eiffel Tower, Paris")
   - Tap "Search" button
   - Wait for results
   
   OR
   
   Manual Method:
   - Enter Latitude (e.g., 48.8584)
   - Enter Longitude (e.g., 2.2945)
   - Tap "Set Location"

**2. Configure Your Circle**
   
   - Enter Radius value (e.g., 1)
   - Select Unit (meters, km, or miles)
   - Optional: Enter custom name
   - Choose Line Color (circle outline)
   - Choose Fill Color (circle interior)
   - Adjust Opacity slider (transparency)

**3. Add Circle**
   
   - Tap "Add Circle" button
   - Circle added to list below
   - Repeat to add more circles
   - Tap "Remove" to delete unwanted circles

**4. Generate KMZ File**
   
   - Tap "Generate & Save KMZ"
   - File saved to device storage
   - Note the file location
   - Ready to share or upload!

**5. Import to Google My Maps**
   
   - Open browser: https://www.google.com/mymaps
   - Sign in with Google account
   - Create New Map or open existing
   - Click "Import"
   - Select your KMZ file
   - Circles appear on map!

================================================================
🎨 EXAMPLE USE CASES
================================================================

📡 **Coverage Areas**
   - Cell tower range
   - WiFi hotspot coverage
   - Delivery zones
   - Service territories

🏃 **Distance Mapping**
   - Walking/running distances
   - 5K, 10K race planning
   - Fitness zone mapping
   - Training route planning

🏢 **Business Planning**
   - Store delivery radius
   - Branch coverage analysis
   - Market penetration zones
   - Competitor mapping

🚨 **Emergency Services**
   - Response coverage areas
   - Evacuation zones
   - Alert radius planning
   - Resource allocation

🏫 **Education**
   - School district boundaries
   - Catchment areas
   - Field trip planning
   - Geography lessons

================================================================
⚙️ SETTINGS & PERMISSIONS
================================================================

**Required Permissions:**

📡 Internet
   - Search locations (OpenStreetMap API)
   - Download map tiles (if map preview enabled)
   
💾 Storage (Read/Write)
   - Save generated KMZ files
   - Access Downloads folder
   - Share files with other apps

**Optional Permissions:**

📍 Location Services
   - Auto-detect current location (future feature)
   - Not required - can enter coordinates manually

**Privacy:**
- No user data collected
- No analytics or tracking
- All processing done locally on device
- Location searches go to OpenStreetMap (public API)
- No account or registration needed

================================================================
🔧 TROUBLESHOOTING
================================================================

**Problem: App won't install**
Solution:
- Enable "Unknown Sources" in Android Settings
- Check available storage space (need 50+ MB)
- Update Android to 5.0 or higher
- Download APK again (may be corrupted)

**Problem: Location search fails**
Solution:
- Check internet connection
- Try different search terms (be specific)
- Use manual coordinates instead
- Verify OpenStreetMap is accessible

**Problem: KMZ file not found**
Solution:
- Check Downloads folder
- Check app's data folder
- Note the file path shown after generation
- Use file manager to locate
- Try generating again

**Problem: Circles don't show in Google My Maps**
Solution:
- Verify KMZ file opens in Google Earth
- Check file size (not 0 bytes)
- Try re-uploading to My Maps
- Clear browser cache and retry
- Use desktop computer to upload

**Problem: App crashes on start**
Solution:
- Clear app data in Settings
- Reinstall the app
- Check Android version (need 5.0+)
- Restart device
- Report bug with details

**Problem: Map preview not working**
Solution:
- Map preview is optional feature
- Requires internet for tiles
- May not work on all devices
- App still fully functional without it
- All other features work normally

================================================================
📱 MOBILE VS DESKTOP
================================================================

Feature                  | Mobile App  | Desktop App
-------------------------|-------------|-------------
Touch Interface          | ✓ Yes       | ✗ Mouse
Portability              | ✓ Phone     | Computer
Installation             | APK/Store   | Python
Dependencies             | None        | Python 3.7+
Map Preview              | Optional    | Optional
Offline Mode             | Partial*    | Partial*
File Sharing             | Built-in    | Manual
GPS Support              | Future      | N/A
Screen Size              | Optimized   | Large

* Offline except location search

================================================================
🔗 SHARING & EXPORTING
================================================================

**Share KMZ File:**
1. After generating, note file location
2. Open file manager
3. Navigate to file
4. Tap "Share" icon
5. Choose app (Email, Drive, WhatsApp, etc.)
6. Send to recipient

**Upload to Cloud:**
- Google Drive: Auto-sync if in Drive folder
- Dropbox: Use Dropbox app to upload
- OneDrive: Use OneDrive app to upload
- Email: Attach file to email

**Import Options:**
- Google My Maps (recommended)
- Google Earth (desktop/mobile)
- ArcGIS Online
- QGIS (desktop GIS software)
- Any KML/KMZ compatible application

================================================================
🆘 SUPPORT & FEEDBACK
================================================================

**Getting Help:**
1. Read this documentation thoroughly
2. Check TROUBLESHOOTING section
3. Review BUILD_INSTRUCTIONS.txt if building
4. Search online for Kivy/Buildozer issues

**Reporting Bugs:**
- Describe the problem clearly
- Include steps to reproduce
- Note your device model and Android version
- Attach screenshots if helpful
- Mention any error messages

**Suggesting Features:**
- Explain the use case
- Describe expected behavior
- Note if it's critical or nice-to-have
- Consider mobile limitations (screen size, battery, etc.)

================================================================
📊 FILE FORMATS
================================================================

**KMZ File Structure:**
- Compressed KML (Keyhole Markup Language)
- ZIP archive with .kmz extension
- Contains XML description of geometry
- Includes styling information
- Compatible with Google Earth/Maps

**Color Format:**
- KML uses aabbggrr (not standard RGB!)
- aa = Alpha (opacity, 00-ff)
- bb = Blue (00-ff)
- gg = Green (00-ff)
- rr = Red (00-ff)
- Example: ff0000ff = Fully opaque red

**Coordinates:**
- Latitude: -90 to +90 (South to North)
- Longitude: -180 to +180 (West to East)
- WGS84 datum (standard GPS coordinates)

================================================================
🎓 LEARNING RESOURCES
================================================================

**KML/KMZ Format:**
- https://developers.google.com/kml/documentation/
- https://en.wikipedia.org/wiki/Keyhole_Markup_Language

**Google My Maps:**
- https://www.google.com/mymaps

**OpenStreetMap:**
- https://www.openstreetmap.org

**Kivy Framework:**
- https://kivy.org
- https://kivy.org/doc/stable/

================================================================
📜 LICENSE & CREDITS
================================================================

**Application:**
- Free and open source
- No restrictions on use
- Modify as needed
- No warranty provided

**Dependencies:**
- Kivy: MIT License
- Pillow: PIL Software License
- Requests: Apache 2.0 License

**Data Sources:**
- OpenStreetMap: ODbL (Open Data Commons Open Database License)
- Map tiles: © OpenStreetMap contributors

================================================================
✅ VERSION INFORMATION
================================================================

Version: 2.0 Mobile Edition
Release Date: 2026-02-15
Platform: Android & iOS
Framework: Kivy 2.2.1
Status: ✅ Production Ready

Minimum Requirements:
- Android 5.0 (API 21) or iOS 11.0
- 50 MB storage
- Internet for search

Recommended:
- Android 8.0+ or iOS 13.0+
- 100 MB storage
- GPS enabled
- 4G/WiFi connection

================================================================

🎉 **Enjoy creating map circles on the go!** 📱🗺️

================================================================
