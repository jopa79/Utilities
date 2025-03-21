import os
import sys
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread

def export_filenames_list(folder_path, output_file=None, status_callback=None):
    """
    Export a list of filenames from the specified folder to a text file.
    
    Args:
        folder_path (str): Path to the folder containing files
        output_file (str, optional): Path to output file. If None, a default name will be created.
        status_callback (function, optional): Callback for updating status
    
    Returns:
        str: Path to the created output file
    """
    try:
        # Update status
        if status_callback:
            status_callback("Verarbeite Verzeichnis...")
        
        # Validate folder exists
        if not os.path.exists(folder_path):
            if status_callback:
                status_callback("FEHLER: Verzeichnis nicht gefunden")
            return None
        
        if not os.path.isdir(folder_path):
            if status_callback:
                status_callback("FEHLER: Keine gültige Verzeichnis")
            return None
            
        # Get all files in the directory
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        if status_callback:
            status_callback(f"{len(files)} Dateien gefunden. Exportiere...")
        
        # Generate output filename if not provided
        if output_file is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = os.path.dirname(folder_path) if os.path.dirname(folder_path) else "."
            output_file = os.path.join(output_dir, f"filenames_list_{timestamp}.txt")
        
        # Write filenames to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Verzeichnis: {os.path.abspath(folder_path)}\n")
            f.write(f"Datum: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Anzahl Dateien: {len(files)}\n")
            f.write("\n=== DATEINAMEN ===\n\n")
            
            for filename in sorted(files):
                f.write(f"{filename}\n")
        
        if status_callback:
            status_callback(f"Export erfolgreich: {os.path.abspath(output_file)}")
        
        return os.path.abspath(output_file)
        
    except Exception as e:
        error_msg = f"FEHLER: Export fehlgeschlagen: {str(e)}"
        if status_callback:
            status_callback(error_msg)
        return None

class FilenamesExporterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Datei-Namen Exporter")
        self.root.geometry("600x400")
        self.root.minsize(500, 300)
        
        self.create_widgets()
        
        # Set default folder to script directory if run directly
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            default_dir = os.path.dirname(sys.executable)
        else:
            # Running as script
            default_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.folder_var.set(default_dir)
    
    def create_widgets(self):
        # Create frame for all controls
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Folder selection
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(folder_frame, text="Verzeichnis:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.folder_var = tk.StringVar()
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(folder_frame, text="Durchsuchen...", command=self.browse_folder)
        browse_btn.pack(side=tk.RIGHT)
        
        # Output file selection
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(output_frame, text="Ausgabedatei:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.output_var = tk.StringVar()
        output_entry = ttk.Entry(output_frame, textvariable=self.output_var)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.custom_output_btn = ttk.Button(output_frame, text="Durchsuchen...", command=self.browse_output)
        self.custom_output_btn.pack(side=tk.RIGHT)
        
        # Checkbox for auto-generating output name
        self.auto_output_var = tk.BooleanVar(value=True)
        auto_output_check = ttk.Checkbutton(
            main_frame, 
            text="Ausgabedateinamen automatisch generieren", 
            variable=self.auto_output_var,
            command=self.toggle_output_entry
        )
        auto_output_check.pack(anchor=tk.W, pady=(0, 10))
        
        # Initialize output entry state
        self.toggle_output_entry()
        
        # Export button
        self.export_btn = ttk.Button(main_frame, text="Dateinamen exportieren", command=self.start_export)
        self.export_btn.pack(pady=(0, 10))
        
        # Status area
        ttk.Label(main_frame, text="Status:").pack(anchor=tk.W)
        
        # Create a frame for the status text with a border
        status_frame = ttk.Frame(main_frame, borderwidth=1, relief="sunken")
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_text = tk.Text(status_frame, wrap=tk.WORD, height=8)
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        status_scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=status_scrollbar.set)
        
        self.status_text.configure(state="disabled")
        
        # Set initial status
        self.update_status("Bereit. Bitte wählen Sie ein Verzeichnis und klicken Sie auf 'Dateinamen exportieren'.")
    
    def toggle_output_entry(self):
        """Enable/disable output file entry based on checkbox"""
        if self.auto_output_var.get():
            self.output_var.set("")
            self.custom_output_btn.configure(state="disabled")
        else:
            self.custom_output_btn.configure(state="normal")
    
    def browse_folder(self):
        """Open file dialog to choose folder"""
        folder = filedialog.askdirectory(initialdir=self.folder_var.get() or os.getcwd())
        if folder:
            self.folder_var.set(folder)
    
    def browse_output(self):
        """Open file dialog to choose output file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialdir=os.path.dirname(self.output_var.get() or self.folder_var.get() or os.getcwd()),
            initialfile="filenames_list.txt"
        )
        if file_path:
            self.output_var.set(file_path)
    
    def update_status(self, message):
        """Update status text"""
        self.status_text.configure(state="normal")
        self.status_text.insert(tk.END, f"{datetime.datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.status_text.see(tk.END)
        self.status_text.configure(state="disabled")
        self.root.update_idletasks()
    
    def start_export(self):
        """Start the export process in a separate thread"""
        folder_path = self.folder_var.get().strip()
        
        if not folder_path:
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Verzeichnis aus.")
            return
        
        # Get output file path
        if self.auto_output_var.get():
            output_file = None
        else:
            output_file = self.output_var.get().strip()
            if not output_file:
                messagebox.showerror("Fehler", "Bitte wählen Sie eine Ausgabedatei oder aktivieren Sie die automatische Generierung.")
                return
        
        # Disable the export button during processing
        self.export_btn.configure(state="disabled")
        self.update_status(f"Starte Export aus Verzeichnis: {folder_path}")
        
        # Run export in a separate thread to keep GUI responsive
        export_thread = Thread(target=self.run_export, args=(folder_path, output_file))
        export_thread.daemon = True
        export_thread.start()
    
    def run_export(self, folder_path, output_file):
        """Run the export process"""
        try:
            result_path = export_filenames_list(folder_path, output_file, self.update_status)
            
            if result_path:
                # Use messagebox to show success and ask if user wants to open the file
                if messagebox.askyesno("Export erfolgreich", 
                                     f"Dateiliste wurde exportiert nach:\n{result_path}\n\nMöchten Sie die Datei öffnen?"):
                    self.open_file(result_path)
        except Exception as e:
            self.update_status(f"Fehler während des Exports: {str(e)}")
        
        # Re-enable the export button
        self.root.after(0, lambda: self.export_btn.configure(state="normal"))
    
    def open_file(self, file_path):
        """Open the exported file with the default application"""
        try:
            if sys.platform == 'win32':
                os.startfile(file_path)
            elif sys.platform == 'darwin':
                os.system(f'open "{file_path}"')
            else:
                os.system(f'xdg-open "{file_path}"')
        except Exception as e:
            self.update_status(f"Fehler beim Öffnen der Datei: {str(e)}")

def main():
    root = tk.Tk()
    app = FilenamesExporterGUI(root)
    
    # Set icon if available
    try:
        if getattr(sys, 'frozen', False):
            # Running as compiled exe
            basedir = os.path.dirname(sys.executable)
        else:
            # Running as script
            basedir = os.path.dirname(os.path.abspath(__file__))
        
        icon_path = os.path.join(basedir, "folder_icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except:
        pass  # Just ignore icon errors
    
    root.mainloop()

if __name__ == "__main__":
    main()
