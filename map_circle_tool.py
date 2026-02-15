#!/usr/bin/env python3
"""
Google Maps Circle Generator
Creates circles around a point and exports to KMZ for Google My Maps
"""

import math
import zipfile
import os
import urllib.request
import urllib.parse
import json
from datetime import datetime
from typing import List, Tuple, Optional, Dict


def geocode_location(place_name: str) -> Optional[Dict[str, any]]:
    """
    Geocode a place name to coordinates using OpenStreetMap Nominatim
    
    Args:
        place_name: Name of the place to search for
        
    Returns:
        Dictionary with 'lat', 'lon', 'display_name' or None if not found
    """
    try:
        # URL encode the place name
        encoded_place = urllib.parse.quote(place_name)
        
        # Nominatim API endpoint (free, no API key required)
        url = f"https://nominatim.openstreetmap.org/search?q={encoded_place}&format=json&limit=1"
        
        # Set user agent as required by Nominatim usage policy
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'MapCircleGenerator/1.0'}
        )
        
        # Make the request
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            if data and len(data) > 0:
                result = data[0]
                return {
                    'lat': float(result['lat']),
                    'lon': float(result['lon']),
                    'display_name': result.get('display_name', place_name)
                }
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None
    
    return None


class MapCircleGenerator:
    """Generate circles on Google Maps and export as KMZ files"""
    
    def __init__(self, center_lat: float, center_lon: float, name: str = "Location"):
        """
        Initialize the generator with a center point
        
        Args:
            center_lat: Latitude of center point
            center_lon: Longitude of center point
            name: Name for the location
        """
        self.center_lat = center_lat
        self.center_lon = center_lon
        self.name = name
        self.circles = []
    
    @classmethod
    def from_place_name(cls, place_name: str) -> Optional['MapCircleGenerator']:
        """
        Create a MapCircleGenerator by searching for a place name
        
        Args:
            place_name: Name of the place to search for
            
        Returns:
            MapCircleGenerator instance or None if place not found
        """
        location = geocode_location(place_name)
        if location:
            return cls(
                center_lat=location['lat'],
                center_lon=location['lon'],
                name=location['display_name']
            )
        return None
        
    def add_circle(self, radius_meters: float, name: str = None, 
                   line_color: str = "ff0000ff", fill_color: str = None,
                   fill_opacity: float = 0.3, width: int = 2):
        """
        Add a circle to be drawn
        
        Args:
            radius_meters: Radius in meters
            name: Optional name for the circle
            line_color: KML line color in format aabbggrr (alpha, blue, green, red)
            fill_color: KML fill color in format aabbggrr. If None, uses line_color
            fill_opacity: Fill opacity from 0.0 (transparent) to 1.0 (opaque)
            width: Line width
        """
        if name is None:
            name = f"Circle {radius_meters}m"
        
        # Use line color for fill if not specified
        if fill_color is None:
            fill_color = line_color
        
        # Clamp opacity between 0 and 1
        fill_opacity = max(0.0, min(1.0, fill_opacity))
        
        self.circles.append({
            'radius': radius_meters,
            'name': name,
            'line_color': line_color,
            'fill_color': fill_color,
            'fill_opacity': fill_opacity,
            'width': width
        })
        
    def _calculate_circle_points(self, radius_meters: float, num_points: int = 64) -> List[Tuple[float, float]]:
        """
        Calculate points around a circle using geographic coordinates
        
        Args:
            radius_meters: Radius in meters
            num_points: Number of points to approximate the circle
            
        Returns:
            List of (longitude, latitude) tuples
        """
        points = []
        
        # Earth radius in meters
        earth_radius = 6371000.0
        
        # Convert radius to angular distance in radians
        angular_distance = radius_meters / earth_radius
        
        # Convert center to radians
        lat_rad = math.radians(self.center_lat)
        lon_rad = math.radians(self.center_lon)
        
        for i in range(num_points + 1):
            # Bearing in radians (0 to 2π)
            bearing = 2 * math.pi * i / num_points
            
            # Calculate new point using the haversine formula
            new_lat = math.asin(
                math.sin(lat_rad) * math.cos(angular_distance) +
                math.cos(lat_rad) * math.sin(angular_distance) * math.cos(bearing)
            )
            
            new_lon = lon_rad + math.atan2(
                math.sin(bearing) * math.sin(angular_distance) * math.cos(lat_rad),
                math.cos(angular_distance) - math.sin(lat_rad) * math.sin(new_lat)
            )
            
            # Convert back to degrees
            points.append((math.degrees(new_lon), math.degrees(new_lat)))
        
        return points
    
    def _generate_kml(self) -> str:
        """Generate KML content with all circles"""
        
        kml_header = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>{name}</name>
    <description>Circles generated around {lat}, {lon}</description>
'''.format(name=self.name, lat=self.center_lat, lon=self.center_lon)
        
        # Add center point placemark
        center_placemark = '''
    <Placemark>
        <name>{name} - Center</name>
        <description>Center point at {lat}, {lon}</description>
        <Point>
            <coordinates>{lon},{lat},0</coordinates>
        </Point>
    </Placemark>
'''.format(name=self.name, lat=self.center_lat, lon=self.center_lon)
        
        circle_placemarks = []
        
        for circle in self.circles:
            points = self._calculate_circle_points(circle['radius'])
            
            # Create coordinates string
            coords = ' '.join([f"{lon},{lat},0" for lon, lat in points])
            
            # Convert opacity to KML alpha (0-255 hex)
            alpha_hex = format(int(circle['fill_opacity'] * 255), '02x')
            fill_color_with_alpha = alpha_hex + circle['fill_color'][2:]  # Replace alpha component
            
            placemark = '''
    <Placemark>
        <name>{name}</name>
        <description>Radius: {radius}m ({radius_km:.2f}km)</description>
        <Style>
            <LineStyle>
                <color>{line_color}</color>
                <width>{width}</width>
            </LineStyle>
            <PolyStyle>
                <color>{fill_color}</color>
                <fill>1</fill>
                <outline>1</outline>
            </PolyStyle>
        </Style>
        <Polygon>
            <outerBoundaryIs>
                <LinearRing>
                    <coordinates>{coords}</coordinates>
                </LinearRing>
            </outerBoundaryIs>
        </Polygon>
    </Placemark>
'''.format(
                name=circle['name'],
                radius=circle['radius'],
                radius_km=circle['radius'] / 1000,
                line_color=circle['line_color'],
                fill_color=fill_color_with_alpha,
                width=circle['width'],
                coords=coords
            )
            
            circle_placemarks.append(placemark)
        
        kml_footer = '''
</Document>
</kml>'''
        
        return kml_header + center_placemark + ''.join(circle_placemarks) + kml_footer
    
    def save_kmz(self, output_path: str = None) -> str:
        """
        Save circles as KMZ file
        
        Args:
            output_path: Path for output file. If None, generates default name
            
        Returns:
            Path to created KMZ file
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"circles_{self.name.replace(' ', '_')}_{timestamp}.kmz"
        
        # Ensure .kmz extension
        if not output_path.endswith('.kmz'):
            output_path += '.kmz'
        
        # Generate KML content
        kml_content = self._generate_kml()
        
        # Create KMZ file (zipped KML)
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as kmz:
            kmz.writestr('doc.kml', kml_content)
        
        return output_path
    
    def save_kml(self, output_path: str = None) -> str:
        """
        Save circles as KML file (uncompressed)
        
        Args:
            output_path: Path for output file. If None, generates default name
            
        Returns:
            Path to created KML file
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"circles_{self.name.replace(' ', '_')}_{timestamp}.kml"
        
        # Ensure .kml extension
        if not output_path.endswith('.kml'):
            output_path += '.kml'
        
        # Generate and save KML content
        kml_content = self._generate_kml()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(kml_content)
        
        return output_path


def main():
    """Example usage of the MapCircleGenerator"""
    
    # Example: Create circles around Singapore
    print("Google Maps Circle Generator")
    print("=" * 50)
    
    # Get user input
    print("\nEnter location coordinates:")
    try:
        lat = float(input("  Latitude: "))
        lon = float(input("  Longitude: "))
        name = input("  Location name (optional): ").strip() or "Location"
    except ValueError:
        print("Invalid input. Using default location (Singapore)")
        lat, lon, name = 1.3521, 103.8198, "Singapore"
    
    # Create generator
    generator = MapCircleGenerator(lat, lon, name)
    
    # Add circles
    print("\nAdd circles (enter radius in meters, 0 to finish):")
    circle_count = 0
    
    # Predefined colors (aabbggrr format - alpha, blue, green, red)
    colors = [
        'ff0000ff',  # Red
        'ff00ff00',  # Green
        'ffff0000',  # Blue
        'ff00ffff',  # Yellow
        'ffff00ff',  # Magenta
        'ffffff00',  # Cyan
    ]
    
    while True:
        try:
            radius_input = input(f"  Circle {circle_count + 1} radius (meters, 0 to finish): ")
            radius = float(radius_input)
            
            if radius <= 0:
                break
            
            circle_name = input(f"    Name (optional): ").strip()
            if not circle_name:
                circle_name = f"Circle {int(radius)}m"
            
            color = colors[circle_count % len(colors)]
            generator.add_circle(radius, circle_name, color)
            circle_count += 1
            
        except ValueError:
            print("Invalid input. Skipping.")
            continue
        except KeyboardInterrupt:
            print("\nInterrupted.")
            break
    
    if circle_count == 0:
        print("No circles added. Exiting.")
        return
    
    # Save to KMZ
    print("\nGenerating KMZ file...")
    output_file = generator.save_kmz()
    print(f"✓ Created: {output_file}")
    print(f"\nYou can now upload this file to Google My Maps:")
    print("  1. Go to https://www.google.com/mymaps")
    print("  2. Click 'Create a New Map'")
    print("  3. Click 'Import' and select the KMZ file")


if __name__ == "__main__":
    main()
