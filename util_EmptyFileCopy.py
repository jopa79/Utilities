import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading

class EmptyFileCopierGUI:
    def __init__(self, parent_frame):
        # Set padding and styling - reduce padding
        self.mainframe = ttk.LabelFrame(parent_frame, text="Empty File Copier", padding="5 5 5 5")
        self.mainframe.pack(fill=tk.X, padx=5, pady=2)
        
        # Variables
        self.source_dir = tk.StringVar()
        self.target_dir = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready to copy files")
        self.progress_var = tk.DoubleVar(value=0.0)
        
        # Create a frame for directory selection (side by side)
        dir_frame = ttk.Frame(self.mainframe)
        dir_frame.pack(fill=tk.X, padx=2, pady=2)
        
        # Source directory selection (left side) - more compact
        source_frame = ttk.Frame(dir_frame)
        source_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 2))
        
        ttk.Label(source_frame, text="Source Directory:", font=('Arial', 9)).pack(anchor=tk.W, pady=(0, 2))
        self.source_entry = ttk.Entry(source_frame, width=40, textvariable=self.source_dir)
        self.source_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(source_frame, text="Browse", command=self.browse_source, width=8).pack(side=tk.RIGHT, padx=(2, 0))
        
        # Target directory selection (right side) - more compact
        target_frame = ttk.Frame(dir_frame)
        target_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(2, 0))
        
        ttk.Label(target_frame, text="Target Directory:", font=('Arial', 9)).pack(anchor=tk.W, pady=(0, 2))
        self.target_entry = ttk.Entry(target_frame, width=40, textvariable=self.target_dir)
        self.target_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(target_frame, text="Browse", command=self.browse_target, width=8).pack(side=tk.RIGHT, padx=(2, 0))
        
        # Bottom frame with button, progress and status in a single row
        bottom_frame = ttk.Frame(self.mainframe)
        bottom_frame.pack(fill=tk.X, padx=2, pady=(2, 0))
        
        # Copy button - smaller
        self.copy_button = ttk.Button(bottom_frame, text="Create Empty Copies", command=self.start_copy, width=18)
        self.copy_button.pack(side=tk.LEFT, pady=2)
        
        # Progress bar - remove height parameter
        self.progress = ttk.Progressbar(bottom_frame, orient=tk.HORIZONTAL, length=100, 
                                       mode='determinate', variable=self.progress_var)
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)
        
        # Status label - on same row
        self.status_label = ttk.Label(bottom_frame, textvariable=self.status_text, font=('Arial', 9))
        self.status_label.pack(side=tk.RIGHT, pady=2)
    
    def browse_source(self):
        """Open a file dialog to select the source directory."""
        directory = filedialog.askdirectory()
        if directory:
            self.source_dir.set(directory)
    
    def browse_target(self):
        """Open a file dialog to select the target directory."""
        directory = filedialog.askdirectory()
        if directory:
            self.target_dir.set(directory)
    
    def update_status(self, message):
        """Update the status text."""
        self.status_text.set(message)
    
    def start_copy(self):
        """Start the copy process in a separate thread."""
        source = self.source_dir.get()
        target = self.target_dir.get()
        
        if not source or not target:
            messagebox.showwarning("Missing Information", 
                                  "Please select both source and target directories.")
            return
        
        if source == target:
            messagebox.showwarning("Invalid Selection", 
                                  "Source and target directories must be different.")
            return
        
        # Disable the copy button during processing
        self.copy_button.config(state=tk.DISABLED)
        
        # Run the copy process in a separate thread to keep UI responsive
        threading.Thread(target=self.create_empty_copies, 
                         args=(source, target), 
                         daemon=True).start()
    
    def create_empty_copies(self, source_dir, target_dir):
        """Creates empty copies of all files from source_dir in target_dir."""
        try:
            # Create target directory if it doesn't exist
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
                self.update_status(f"Created target directory: {target_dir}")
            
            # Get list of files in source directory (non-recursive)
            files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
            
            if not files:
                self.update_status(f"No files found in {source_dir}")
                return
            
            # Reset progress bar
            self.progress_var.set(0)
            total_files = len(files)
            
            # Create empty copies
            for i, filename in enumerate(files):
                source_path = os.path.join(source_dir, filename)
                target_path = os.path.join(target_dir, filename)
                
                # Create empty file with same name
                with open(target_path, 'w') as f:
                    pass  # Create empty file
                
                # Update progress
                progress_pct = ((i + 1) / total_files) * 100
                self.progress_var.set(progress_pct)
                self.update_status(f"Created: {filename} ({i+1}/{total_files})")
            
            # Final status update
            self.update_status(f"Completed! Created {len(files)} empty files in {target_dir}")
            messagebox.showinfo("Complete", f"Successfully created {len(files)} empty files.")
            
        except Exception as e:
            self.update_status(f"Error: {e}")
            messagebox.showerror("Error", str(e))
        
        finally:
            # Re-enable the copy button
            self.copy_button.config(state=tk.NORMAL) 
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Empty File Copier")
    root.geometry("800x200")
    app = EmptyFileCopierGUI(root)
    root.mainloop()