#!/usr/bin/env python3
"""
Circle Map Generator - Mobile Application
Built with Kivy for Android/iOS
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from datetime import datetime
import os
import threading
import webbrowser

# Import the core map circle tool
from map_circle_tool import MapCircleGenerator, geocode_location

# Try to import map widget for visual preview
try:
    from kivy_garden.mapview import MapView, MapMarker
    MAP_AVAILABLE = True
except ImportError:
    MAP_AVAILABLE = False
    print("MapView not available. Install kivy-garden.mapview for map preview.")


class CircleListItem(BoxLayout):
    """Widget representing a circle in the list"""
    def __init__(self, circle_data, index, remove_callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = dp(5)
        self.spacing = dp(5)
        
        # Circle info
        info_text = f"{circle_data['name']}\n{circle_data['display_radius']} - {circle_data['display_line_color']}/{circle_data['display_fill_color']}"
        info_label = Label(
            text=info_text,
            size_hint_x=0.8,
            halign='left',
            valign='middle'
        )
        info_label.bind(size=info_label.setter('text_size'))
        
        # Remove button
        remove_btn = Button(
            text='Remove',
            size_hint_x=0.2,
            background_color=(1, 0.3, 0.3, 1)
        )
        remove_btn.bind(on_press=lambda x: remove_callback(index))
        
        self.add_widget(info_label)
        self.add_widget(remove_btn)


class CircleMapApp(App):
    """Main mobile application for creating map circles"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_location = None
        self.circles = []
        self.map_widget = None
        self.location_marker = None
        
        # Color mappings (KML aabbggrr format)
        self.colors = {
            'Red': 'ff0000ff',
            'Green': 'ff00ff00',
            'Blue': 'ffff0000',
            'Yellow': 'ff00ffff',
            'Magenta': 'ffff00ff',
            'Cyan': 'ffffff00',
            'Orange': 'ff0099ff',
            'Purple': 'ff800080',
            'Black': 'ff000000',
            'White': 'ffffffff'
        }
        
    def build(self):
        """Build the mobile UI"""
        # Main layout with scroll
        main_scroll = ScrollView(size_hint=(1, 1))
        main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Title
        title = Label(
            text='🗺️ Circle Map Generator',
            size_hint_y=None,
            height=dp(50),
            font_size='20sp',
            bold=True
        )
        main_layout.add_widget(title)
        
        # Location Search Section
        search_section = self.create_search_section()
        main_layout.add_widget(search_section)
        
        # Manual Coordinates Section
        coord_section = self.create_coordinates_section()
        main_layout.add_widget(coord_section)
        
        # Current Location Display
        location_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            padding=dp(5)
        )
        location_box.add_widget(Label(
            text='🎯 Current Location',
            size_hint_y=None,
            height=dp(25),
            bold=True
        ))
        self.location_label = Label(
            text='No location set',
            size_hint_y=None,
            height=dp(50),
            color=(0.2, 0.6, 1, 1)
        )
        location_box.add_widget(self.location_label)
        main_layout.add_widget(location_box)
        
        # Map Preview (if available)
        if MAP_AVAILABLE:
            map_section = self.create_map_section()
            main_layout.add_widget(map_section)
            # Add spacer after map to prevent overlap with next section
            main_layout.add_widget(Label(
                text='',
                size_hint_y=None,
                height=dp(10)
            ))
            # Add separator line for visual clarity
            from kivy.uix.widget import Widget
            separator = Widget(
                size_hint_y=None,
                height=dp(1)
            )
            main_layout.add_widget(separator)
            # Another spacer after separator
            main_layout.add_widget(Label(
                text='',
                size_hint_y=None,
                height=dp(10)
            ))
        
        # Circle Configuration Section
        circle_section = self.create_circle_section()
        main_layout.add_widget(circle_section)
        
        # Circles List Section
        circles_list_section = self.create_circles_list_section()
        main_layout.add_widget(circles_list_section)
        
        # Generate Button
        self.generate_btn = Button(
            text='Generate & Save KMZ',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.8, 0.2, 1),
            disabled=True
        )
        self.generate_btn.bind(on_press=self.generate_kmz)
        main_layout.add_widget(self.generate_btn)
        
        # Bottom spacer for breathing room
        main_layout.add_widget(Label(
            text='',
            size_hint_y=None,
            height=dp(20)
        ))
        
        main_scroll.add_widget(main_layout)
        return main_scroll
    
    def create_search_section(self):
        """Create location search section"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(160),
            spacing=dp(8),
            padding=dp(5)
        )
        
        section.add_widget(Label(
            text='📍 Search Location',
            size_hint_y=None,
            height=dp(30),
            bold=True
        ))
        
        self.search_input = TextInput(
            hint_text='Enter place name (e.g., Tokyo Tower)',
            size_hint_y=None,
            height=dp(40),
            multiline=False
        )
        section.add_widget(self.search_input)
        
        search_btn = Button(
            text='Search',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.6, 1, 1)
        )
        search_btn.bind(on_press=self.search_location)
        section.add_widget(search_btn)
        
        self.search_result = Label(
            text='',
            size_hint_y=None,
            height=dp(30),
            color=(0.2, 0.8, 0.2, 1)
        )
        section.add_widget(self.search_result)
        
        return section
    
    def create_coordinates_section(self):
        """Create manual coordinates section"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(170),
            spacing=dp(8),
            padding=dp(5)
        )
        
        section.add_widget(Label(
            text='📌 Manual Coordinates',
            size_hint_y=None,
            height=dp(30),
            bold=True
        ))
        
        coord_grid = GridLayout(
            cols=2,
            size_hint_y=None,
            height=dp(90),
            spacing=dp(8),
            row_default_height=dp(40)
        )
        
        coord_grid.add_widget(Label(
            text='Latitude:',
            size_hint_y=None,
            height=dp(40)
        ))
        self.lat_input = TextInput(
            hint_text='40.7829',
            multiline=False,
            input_filter='float',
            size_hint_y=None,
            height=dp(40)
        )
        coord_grid.add_widget(self.lat_input)
        
        coord_grid.add_widget(Label(
            text='Longitude:',
            size_hint_y=None,
            height=dp(40)
        ))
        self.lon_input = TextInput(
            hint_text='-73.9654',
            multiline=False,
            input_filter='float',
            size_hint_y=None,
            height=dp(40)
        )
        coord_grid.add_widget(self.lon_input)
        
        section.add_widget(coord_grid)
        
        set_btn = Button(
            text='Set Location',
            size_hint_y=None,
            height=dp(40),
            background_color=(0.2, 0.6, 1, 1)
        )
        set_btn.bind(on_press=self.set_manual_location)
        section.add_widget(set_btn)
        
        return section
    
    def create_map_section(self):
        """Create map preview section"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(245),  # Increased from 235dp
            spacing=dp(5),
            padding=(dp(5), dp(5), dp(5), dp(10))  # Extra bottom padding
        )
        
        section.add_widget(Label(
            text='🗺️ Map Preview',
            size_hint_y=None,
            height=dp(30),
            bold=True
        ))
        
        self.map_widget = MapView(
            zoom=2,
            lat=20,
            lon=0,
            size_hint_y=None,
            height=dp(195)
        )
        section.add_widget(self.map_widget)
        
        # Add spacer after map
        section.add_widget(Label(
            text='',
            size_hint_y=None,
            height=dp(10)  # Increased from 5dp
        ))
        
        return section
    
    def create_circle_section(self):
        """Create circle configuration section"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(440),  # Increased from 430dp
            spacing=dp(8),
            padding=(dp(5), dp(15), dp(5), dp(5))  # Increased top padding from 10dp to 15dp
        )
        
        section.add_widget(Label(
            text='⭕ Add Circle',
            size_hint_y=None,
            height=dp(30),
            bold=True
        ))
        
        # Small spacer after header
        section.add_widget(Label(
            text='',
            size_hint_y=None,
            height=dp(5)
        ))
        
        # Radius and unit
        radius_box = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(5)
        )
        radius_box.add_widget(Label(text='Radius:', size_hint_x=0.3))
        self.radius_input = TextInput(
            text='1',
            multiline=False,
            input_filter='float',
            size_hint_x=0.3
        )
        radius_box.add_widget(self.radius_input)
        self.unit_spinner = Spinner(
            text='km',
            values=('meters', 'km', 'miles'),
            size_hint_x=0.4
        )
        radius_box.add_widget(self.unit_spinner)
        section.add_widget(radius_box)
        
        # Circle name
        section.add_widget(Label(
            text='Circle Name (optional):',
            size_hint_y=None,
            height=dp(30)
        ))
        self.circle_name_input = TextInput(
            hint_text='e.g., Coverage Zone',
            size_hint_y=None,
            height=dp(40),
            multiline=False
        )
        section.add_widget(self.circle_name_input)
        
        # Line color
        section.add_widget(Label(
            text='Line Color:',
            size_hint_y=None,
            height=dp(30)
        ))
        self.line_color_spinner = Spinner(
            text='Red',
            values=list(self.colors.keys()),
            size_hint_y=None,
            height=dp(40)
        )
        section.add_widget(self.line_color_spinner)
        
        # Fill color
        section.add_widget(Label(
            text='Fill Color:',
            size_hint_y=None,
            height=dp(30)
        ))
        self.fill_color_spinner = Spinner(
            text='Red',
            values=list(self.colors.keys()),
            size_hint_y=None,
            height=dp(40)
        )
        section.add_widget(self.fill_color_spinner)
        
        # Opacity slider
        opacity_label = Label(
            text='Fill Opacity: 30%',
            size_hint_y=None,
            height=dp(30)
        )
        section.add_widget(opacity_label)
        
        self.opacity_slider = Slider(
            min=0,
            max=100,
            value=30,
            size_hint_y=None,
            height=dp(40)
        )
        self.opacity_slider.bind(value=lambda instance, value: 
                                 opacity_label.setter('text')(opacity_label, f'Fill Opacity: {int(value)}%'))
        section.add_widget(self.opacity_slider)
        
        # Add circle button
        self.add_circle_btn = Button(
            text='Add Circle',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.8, 0.2, 1),
            disabled=True
        )
        self.add_circle_btn.bind(on_press=self.add_circle)
        section.add_widget(self.add_circle_btn)
        
        return section
    
    def create_circles_list_section(self):
        """Create circles list section"""
        section = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(220),
            spacing=dp(8),
            padding=dp(5)
        )
        
        section.add_widget(Label(
            text='📋 Circles List',
            size_hint_y=None,
            height=dp(30),
            bold=True
        ))
        
        # Scrollable list
        self.circles_scroll = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False
        )
        self.circles_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(2)
        )
        self.circles_container.bind(minimum_height=self.circles_container.setter('height'))
        self.circles_scroll.add_widget(self.circles_container)
        
        section.add_widget(self.circles_scroll)
        
        return section
    
    def search_location(self, instance):
        """Search for a location by name"""
        place_name = self.search_input.text.strip()
        if not place_name:
            self.show_popup('Input Required', 'Please enter a place name')
            return
        
        self.search_result.text = 'Searching...'
        self.search_result.color = (0.2, 0.6, 1, 1)
        
        # Run search in background thread
        def search_thread():
            location = geocode_location(place_name)
            Clock.schedule_once(lambda dt: self.on_search_complete(location), 0)
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def on_search_complete(self, location):
        """Handle search completion"""
        if location:
            self.current_location = location
            self.location_label.text = f"{location['display_name']}\nLat: {location['lat']:.6f}, Lon: {location['lon']:.6f}"
            self.search_result.text = f"✓ Found!"
            self.search_result.color = (0.2, 0.8, 0.2, 1)
            self.add_circle_btn.disabled = False
            self.update_generate_button()
            
            # Center map on location
            if MAP_AVAILABLE and self.map_widget:
                self.map_widget.center_on(location['lat'], location['lon'])
                self.map_widget.zoom = 12
                
                # Add marker
                if self.location_marker:
                    self.map_widget.remove_marker(self.location_marker)
                self.location_marker = MapMarker(lat=location['lat'], lon=location['lon'])
                self.map_widget.add_marker(self.location_marker)
        else:
            self.search_result.text = '✗ Location not found'
            self.search_result.color = (1, 0.2, 0.2, 1)
            self.show_popup('Not Found', 'Could not find the specified location')
    
    def set_manual_location(self, instance):
        """Set location using manual coordinates"""
        try:
            lat = float(self.lat_input.text)
            lon = float(self.lon_input.text)
            
            if not (-90 <= lat <= 90):
                raise ValueError("Latitude must be between -90 and 90")
            if not (-180 <= lon <= 180):
                raise ValueError("Longitude must be between -180 and 180")
            
            self.current_location = {
                'lat': lat,
                'lon': lon,
                'display_name': f"Custom Location ({lat:.4f}, {lon:.4f})"
            }
            
            self.location_label.text = f"Custom Location\nLat: {lat:.6f}, Lon: {lon:.6f}"
            self.search_result.text = '✓ Location set manually'
            self.search_result.color = (0.2, 0.8, 0.2, 1)
            self.add_circle_btn.disabled = False
            self.update_generate_button()
            
            # Center map on location
            if MAP_AVAILABLE and self.map_widget:
                self.map_widget.center_on(lat, lon)
                self.map_widget.zoom = 12
                
                # Add marker
                if self.location_marker:
                    self.map_widget.remove_marker(self.location_marker)
                self.location_marker = MapMarker(lat=lat, lon=lon)
                self.map_widget.add_marker(self.location_marker)
                
        except ValueError as e:
            self.show_popup('Invalid Input', str(e))
    
    def convert_to_meters(self, value, unit):
        """Convert radius to meters"""
        if unit == 'meters':
            return value
        elif unit == 'km':
            return value * 1000
        elif unit == 'miles':
            return value * 1609.34
        return value
    
    def format_radius(self, meters, unit):
        """Format radius for display"""
        if unit == 'meters':
            return f"{int(meters)}m"
        elif unit == 'km':
            return f"{meters/1000:.2f}km"
        elif unit == 'miles':
            return f"{meters/1609.34:.2f}mi"
        return f"{int(meters)}m"
    
    def add_circle(self, instance):
        """Add a new circle"""
        if not self.current_location:
            self.show_popup('No Location', 'Please set a location first')
            return
        
        try:
            radius_value = float(self.radius_input.text)
            if radius_value <= 0:
                raise ValueError("Radius must be greater than 0")
            
            unit = self.unit_spinner.text
            radius_meters = self.convert_to_meters(radius_value, unit)
            
            circle_name = self.circle_name_input.text.strip()
            if not circle_name:
                circle_name = self.format_radius(radius_meters, unit)
            
            line_color = self.colors[self.line_color_spinner.text]
            fill_color = self.colors[self.fill_color_spinner.text]
            fill_opacity = self.opacity_slider.value / 100.0
            
            circle_data = {
                'radius': radius_meters,
                'name': circle_name,
                'line_color': line_color,
                'fill_color': fill_color,
                'fill_opacity': fill_opacity,
                'width': 2,
                'display_radius': self.format_radius(radius_meters, unit),
                'display_line_color': self.line_color_spinner.text,
                'display_fill_color': self.fill_color_spinner.text,
                'display_opacity': int(self.opacity_slider.value)
            }
            
            self.circles.append(circle_data)
            
            # Add to list UI
            circle_item = CircleListItem(circle_data, len(self.circles) - 1, self.remove_circle)
            self.circles_container.add_widget(circle_item)
            
            # Clear name input
            self.circle_name_input.text = ''
            
            self.update_generate_button()
            self.show_popup('Success', f"Circle '{circle_name}' added!")
            
        except ValueError as e:
            self.show_popup('Invalid Input', str(e))
    
    def remove_circle(self, index):
        """Remove a circle"""
        if 0 <= index < len(self.circles):
            self.circles.pop(index)
            self.circles_container.clear_widgets()
            
            # Rebuild list with updated indices
            for i, circle in enumerate(self.circles):
                circle_item = CircleListItem(circle, i, self.remove_circle)
                self.circles_container.add_widget(circle_item)
            
            self.update_generate_button()
    
    def update_generate_button(self):
        """Enable/disable generate button"""
        self.generate_btn.disabled = not (self.current_location and self.circles)
    
    def generate_kmz(self, instance):
        """Generate and save KMZ file"""
        if not self.current_location or not self.circles:
            self.show_popup('Cannot Generate', 'Please set a location and add circles')
            return
        
        # Show folder selection dialog
        self.show_folder_selector()
    
    def show_folder_selector(self):
        """Show folder selection dialog"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.kmz_filename = f"circles_{timestamp}.kmz"
        
        # Create popup for folder selection
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # Title and info
        title_label = Label(
            text=f'Select folder to save:\n{self.kmz_filename}',
            size_hint_y=None,
            height=dp(60),
            halign='center'
        )
        content.add_widget(title_label)
        
        # File chooser
        from kivy.utils import platform
        if platform == 'android':
            try:
                from android.storage import primary_external_storage_path
                initial_path = primary_external_storage_path()
            except:
                initial_path = os.path.expanduser('~')
        else:
            # Desktop: start at Downloads or home
            downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
            initial_path = downloads_path if os.path.exists(downloads_path) else os.path.expanduser('~')
        
        filechooser = FileChooserListView(
            path=initial_path,
            dirselect=True,
            size_hint_y=None,
            height=dp(400)
        )
        content.add_widget(filechooser)
        
        # Current path display
        path_label = Label(
            text=f'Current: {filechooser.path}',
            size_hint_y=None,
            height=dp(40),
            halign='left',
            text_size=(Window.width - dp(40), None)
        )
        content.add_widget(path_label)
        
        # Update path label when selection changes
        def update_path_label(instance, value):
            path_label.text = f'Current: {value}'
        filechooser.bind(path=update_path_label)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        save_btn = Button(text='Save Here')
        cancel_btn = Button(text='Cancel')
        
        button_layout.add_widget(save_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        # Create popup
        popup = Popup(
            title='Choose Save Location',
            content=content,
            size_hint=(0.95, 0.9)
        )
        
        def save_to_folder(instance):
            selected_path = filechooser.path
            if filechooser.selection:
                # If a folder is selected in the list, use that
                selected_path = filechooser.selection[0]
            
            filepath = os.path.join(selected_path, self.kmz_filename)
            popup.dismiss()
            self.save_kmz_file(filepath)
        
        def cancel_selection(instance):
            popup.dismiss()
        
        save_btn.bind(on_press=save_to_folder)
        cancel_btn.bind(on_press=cancel_selection)
        
        popup.open()
    
    def save_kmz_file(self, filepath):
        """Save the KMZ file to the specified path"""
        try:
            
            # Create generator
            generator = MapCircleGenerator(
                self.current_location['lat'],
                self.current_location['lon'],
                self.current_location['display_name']
            )
            
            # Add all circles
            for circle in self.circles:
                generator.add_circle(
                    radius_meters=circle['radius'],
                    name=circle['name'],
                    line_color=circle['line_color'],
                    fill_color=circle['fill_color'],
                    fill_opacity=circle['fill_opacity'],
                    width=circle['width']
                )
            
            # Save KMZ
            generator.save_kmz(filepath)
            
            # Show success dialog with actions
            self.show_success_dialog(filepath)
            
        except Exception as e:
            self.show_popup('Error', f"Failed to generate KMZ: {str(e)}")
    
    def show_success_dialog(self, filepath):
        """Show success dialog with actionable buttons"""
        content = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Success icon and message
        success_label = Label(
            text='✓ KMZ File Saved!',
            font_size='20sp',
            bold=True,
            color=(0, 0.8, 0, 1),
            size_hint_y=None,
            height=dp(40)
        )
        content.add_widget(success_label)
        
        # File path display (scrollable)
        path_scroll = ScrollView(size_hint_y=None, height=dp(80))
        path_label = Label(
            text=f'Location:\n{filepath}',
            font_size='12sp',
            halign='left',
            valign='top',
            text_size=(Window.width * 0.75, None),
            size_hint_y=None
        )
        path_label.bind(texture_size=path_label.setter('size'))
        path_scroll.add_widget(path_label)
        content.add_widget(path_scroll)
        
        # Instructions
        instructions = Label(
            text='Upload to Google My Maps:',
            size_hint_y=None,
            height=dp(30),
            font_size='14sp'
        )
        content.add_widget(instructions)
        
        # Action buttons
        def open_google_maps(instance):
            """Open Google My Maps in browser"""
            webbrowser.open('https://www.google.com/mymaps')
            self.show_popup('Instructions',
                          'Google My Maps opened in browser.\n\n'
                          'To upload your KMZ:\n'
                          '1. Click "Create a New Map" or open existing\n'
                          '2. Click "Import" in left panel\n'
                          '3. Select your KMZ file')
        
        open_maps_btn = Button(
            text='🌐 Open Google My Maps',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 1, 1)
        )
        open_maps_btn.bind(on_press=open_google_maps)
        content.add_widget(open_maps_btn)
        
        # Spacer
        content.add_widget(Label(size_hint_y=None, height=dp(10)))
        
        # Close button
        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height=dp(50)
        )
        content.add_widget(close_btn)
        
        # Create popup
        popup = Popup(
            title='Success',
            content=content,
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def show_popup(self, title, message):
        """Show a popup message"""
        content = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        content.add_widget(Label(text=message, halign='center'))
        
        close_btn = Button(text='Close', size_hint_y=None, height=dp(50))
        content.add_widget(close_btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.9, None),
            height=dp(200)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    CircleMapApp().run()
