"""
Drag and drop UI components
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, List
import os


class DropZoneFrame(ttk.Frame):
    """Drag and drop zone for file selection"""
    
    def __init__(self, parent, drop_callback: Callable[[List[str]], None]):
        """
        Initialize drop zone
        
        Args:
            parent: Parent widget
            drop_callback: Callback function called when files are dropped
        """
        super().__init__(parent)
        self.drop_callback = drop_callback
        
        # Configure drop zone appearance
        self.configure(relief='ridge', borderwidth=2)
        
        # Create drop zone content
        self._create_content()
        
        # Enable drag and drop
        self._setup_drag_drop()
    
    def _create_content(self):
        """Create the visual content of the drop zone"""
        # Main container
        container = ttk.Frame(self)
        container.pack(expand=True, fill='both')
        
        # Icon and text
        icon_label = ttk.Label(
            container,
            text="📁",
            font=('Arial', 48)
        )
        icon_label.pack(pady=(50, 10))
        
        title_label = ttk.Label(
            container,
            text="Drop files here",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(0, 5))
        
        desc_label = ttk.Label(
            container,
            text="Drag and drop PDF or CSV files\nor click 'Add Files' button",
            font=('Arial', 10),
            foreground='gray'
        )
        desc_label.pack(pady=(0, 10))
        
        # Supported formats
        formats_label = ttk.Label(
            container,
            text="Supported: .pdf, .csv",
            font=('Arial', 9),
            foreground='blue'
        )
        formats_label.pack(pady=(10, 50))
    
    def _setup_drag_drop(self):
        """Set up drag and drop functionality"""
        # Bind drag and drop events
        self.drop_target_register('DND_Files')
        self.dnd_bind('<<Drop>>', self._on_drop)
        self.dnd_bind('<<DragEnter>>', self._on_drag_enter)
        self.dnd_bind('<<DragLeave>>', self._on_drag_leave)
    
    def drop_target_register(self, *args):
        """Register as drop target (placeholder for actual DND implementation)"""
        # In a real implementation, this would use tkdnd or similar
        # For now, we'll provide alternative file selection methods
        pass
    
    def dnd_bind(self, *args):
        """Bind drag and drop events (placeholder)"""
        # Placeholder for actual DND binding
        pass
    
    def _on_drop(self, event):
        """Handle file drop event"""
        try:
            # In a real implementation, this would extract file paths from the event
            # For now, this is a placeholder
            files = []  # Would be extracted from event.data
            
            # Filter supported files
            supported_files = []
            for file_path in files:
                if self._is_supported_file(file_path):
                    supported_files.append(file_path)
            
            if supported_files:
                self.drop_callback(supported_files)
            
        except Exception as e:
            print(f"Drop error: {e}")
    
    def _on_drag_enter(self, event):
        """Handle drag enter event"""
        self.configure(style='Active.TFrame')
    
    def _on_drag_leave(self, event):
        """Handle drag leave event"""
        self.configure(style='TFrame')
    
    def _is_supported_file(self, file_path: str) -> bool:
        """Check if file is supported"""
        supported_extensions = ['.pdf', '.csv']
        _, ext = os.path.splitext(file_path.lower())
        return ext in supported_extensions
    
    def simulate_drop(self, files: List[str]):
        """Simulate a file drop (for testing or programmatic use)"""
        supported_files = [f for f in files if self._is_supported_file(f)]
        if supported_files:
            self.drop_callback(supported_files)


class FileListWidget(ttk.Frame):
    """Widget for displaying and managing selected files"""
    
    def __init__(self, parent):
        """Initialize file list widget"""
        super().__init__(parent)
        
        self.files = []
        
        # Create UI components
        self._create_ui()
    
    def _create_ui(self):
        """Create the file list UI"""
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(
            header_frame,
            text="Selected Files",
            font=('Arial', 12, 'bold')
        ).pack(side='left')
        
        self.count_label = ttk.Label(
            header_frame,
            text="(0 files)",
            font=('Arial', 10),
            foreground='gray'
        )
        self.count_label.pack(side='right')
        
        # File list with scrollbar
        list_frame = ttk.Frame(self)
        list_frame.pack(fill='both', expand=True)
        
        self.listbox = tk.Listbox(
            list_frame,
            selectmode='extended',
            font=('Consolas', 9)
        )
        
        scrollbar = ttk.Scrollbar(
            list_frame,
            orient='vertical',
            command=self.listbox.yview
        )
        
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        self.listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Context menu
        self._create_context_menu()
        
        # Bind events
        self.listbox.bind('<Button-3>', self._show_context_menu)  # Right click
        self.listbox.bind('<Double-Button-1>', self._on_double_click)  # Double click
    
    def _create_context_menu(self):
        """Create context menu for file list"""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Remove Selected", command=self._remove_selected)
        self.context_menu.add_command(label="Remove All", command=self._remove_all)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Show in Explorer", command=self._show_in_explorer)
    
    def _show_context_menu(self, event):
        """Show context menu"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def _on_double_click(self, event):
        """Handle double click on file item"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            file_path = self.files[index]
            self._open_file(file_path)
    
    def _remove_selected(self):
        """Remove selected files from list"""
        selection = self.listbox.curselection()
        if not selection:
            return
        
        # Remove from back to front to maintain indices
        for index in reversed(selection):
            del self.files[index]
            self.listbox.delete(index)
        
        self._update_count()
    
    def _remove_all(self):
        """Remove all files from list"""
        self.files.clear()
        self.listbox.delete(0, tk.END)
        self._update_count()
    
    def _show_in_explorer(self):
        """Show selected file in file explorer"""
        selection = self.listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        file_path = self.files[index]
        
        try:
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                subprocess.run(['explorer', '/select,', file_path])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['open', '-R', file_path])
            else:  # Linux
                subprocess.run(['xdg-open', os.path.dirname(file_path)])
        except Exception as e:
            print(f"Could not open file explorer: {e}")
    
    def _open_file(self, file_path: str):
        """Open file with default application"""
        try:
            import subprocess
            import platform
            
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['open', file_path])
            else:  # Linux
                subprocess.run(['xdg-open', file_path])
        except Exception as e:
            print(f"Could not open file: {e}")
    
    def add_files(self, file_paths: List[str]):
        """Add files to the list"""
        for file_path in file_paths:
            if file_path not in self.files:
                self.files.append(file_path)
                filename = os.path.basename(file_path)
                self.listbox.insert(tk.END, filename)
        
        self._update_count()
    
    def get_files(self) -> List[str]:
        """Get list of selected files"""
        return self.files.copy()
    
    def clear(self):
        """Clear all files"""
        self._remove_all()
    
    def _update_count(self):
        """Update file count display"""
        count = len(self.files)
        self.count_label.configure(text=f"({count} file{'s' if count != 1 else ''})")