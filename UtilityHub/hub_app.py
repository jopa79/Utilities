import os
import sys
import importlib.util
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import inspect
import threading

class UtilityHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Utility Hub")
        self.root.geometry("800x600")
        
        # Create main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create left panel for utility list
        left_frame = ttk.LabelFrame(main_frame, text="Available Utilities")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        
        # Create scrollable list for utilities
        self.utility_listbox = tk.Listbox(left_frame, width=30)
        self.utility_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.utility_listbox.bind('<<ListboxSelect>>', self.on_utility_select)
        
        # Create right panel for utility details and execution
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create info frame
        info_frame = ttk.LabelFrame(right_frame, text="Utility Information")
        info_frame.pack(fill=tk.X, expand=False, padx=5, pady=5)
        
        # Utility name and description
        self.utility_name = ttk.Label(info_frame, text="", font=("TkDefaultFont", 12, "bold"))
        self.utility_name.pack(anchor=tk.W, padx=5, pady=2)
        
        self.utility_desc = ttk.Label(info_frame, text="", wraplength=500)
        self.utility_desc.pack(anchor=tk.W, padx=5, pady=2)
        
        # Function selection
        func_frame = ttk.LabelFrame(right_frame, text="Available Functions")
        func_frame.pack(fill=tk.X, expand=False, padx=5, pady=5)
        
        self.func_combobox = ttk.Combobox(func_frame, state="readonly")
        self.func_combobox.pack(fill=tk.X, padx=5, pady=5)
        self.func_combobox.bind("<<ComboboxSelected>>", self.on_function_select)
        
        # Parameter input frame
        self.param_frame = ttk.LabelFrame(right_frame, text="Parameters")
        self.param_frame.pack(fill=tk.X, expand=False, padx=5, pady=5)
        
        # Execute button
        self.execute_button = ttk.Button(right_frame, text="Execute", command=self.execute_function)
        self.execute_button.pack(padx=5, pady=5)
        
        # Output console
        console_frame = ttk.LabelFrame(right_frame, text="Output Console")
        console_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.console = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Redirect stdout to the console
        self.original_stdout = sys.stdout
        
        # Initialize variables
        self.utils = {}
        self.current_util = None
        self.current_func = None
        self.param_widgets = []
        
        # Load utilities
        self.load_utilities()
    
    def load_utilities(self):
        """Search for and load all Python scripts that start with 'util'"""
        try:
            # Get the current directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Find all Python files that start with "util"
            util_files = [f for f in os.listdir(current_dir) 
                          if f.startswith("util") and f.endswith(".py")]
            
            if not util_files:
                self.console.insert(tk.END, "No utility scripts found in current directory.\n")
                self.console.see(tk.END)
                return
            
            # Load each utility module
            for file in util_files:
                module_name = os.path.splitext(file)[0]
                
                try:
                    # Load the module
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(current_dir, file))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Get module description (docstring)
                    description = module.__doc__ or "No description available"
                    
                    # Find all callable, non-internal functions in the module
                    functions = {}
                    for name, obj in inspect.getmembers(module):
                        if inspect.isfunction(obj) and not name.startswith('_'):
                            functions[name] = obj
                    
                    if functions:
                        self.utils[module_name] = {
                            'module': module,
                            'description': description,
                            'functions': functions
                        }
                        self.utility_listbox.insert(tk.END, module_name)
                
                except Exception as e:
                    self.console.insert(tk.END, f"Error loading {file}: {str(e)}\n")
                    self.console.see(tk.END)
            
            self.console.insert(tk.END, f"Loaded {len(self.utils)} utility modules.\n")
            self.console.see(tk.END)
            
        except Exception as e:
            self.console.insert(tk.END, f"Error scanning for utilities: {str(e)}\n")
            self.console.see(tk.END)
    
    def on_utility_select(self, event):
        """Handle selection of a utility from the list"""
        selection = self.utility_listbox.curselection()
        if not selection:
            return
        
        util_name = self.utility_listbox.get(selection[0])
        self.current_util = self.utils.get(util_name)
        
        if self.current_util:
            # Update utility info
            self.utility_name.config(text=util_name)
            self.utility_desc.config(text=self.current_util['description'])
            
            # Update function dropdown
            self.func_combobox['values'] = list(self.current_util['functions'].keys())
            if self.func_combobox['values']:
                self.func_combobox.current(0)
                self.on_function_select(None)
            else:
                self.clear_param_frame()
                self.current_func = None
    
    def on_function_select(self, event):
        """Handle selection of a function from the dropdown"""
        func_name = self.func_combobox.get()
        if func_name and self.current_util:
            self.current_func = self.current_util['functions'].get(func_name)
            self.update_param_frame()
    
    def update_param_frame(self):
        """Update parameter input fields based on the selected function"""
        self.clear_param_frame()
        
        if not self.current_func:
            return
        
        # Get function signature
        sig = inspect.signature(self.current_func)
        
        # Create input fields for each parameter
        for param_name, param in sig.parameters.items():
            if param_name == 'self':  # Skip self parameter for methods
                continue
                
            frame = ttk.Frame(self.param_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Parameter label
            label = ttk.Label(frame, text=f"{param_name}:")
            label.pack(side=tk.LEFT, padx=5)
            
            # Default value (if any)
            default_value = "" if param.default == inspect.Parameter.empty else str(param.default)
            
            # Create appropriate input widget based on parameter type annotation
            if param.annotation != inspect.Parameter.empty:
                if param.annotation == bool:
                    var = tk.BooleanVar(value=default_value == "True")
                    widget = ttk.Checkbutton(frame, variable=var)
                    widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
                    self.param_widgets.append((param_name, var, 'bool'))
                elif param.annotation == int:
                    var = tk.StringVar(value=default_value)
                    widget = ttk.Spinbox(frame, from_=-1000, to=1000, textvariable=var)
                    widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
                    self.param_widgets.append((param_name, var, 'int'))
                elif param.annotation == float:
                    var = tk.StringVar(value=default_value)
                    widget = ttk.Spinbox(frame, from_=-1000.0, to=1000.0, increment=0.1, textvariable=var)
                    widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
                    self.param_widgets.append((param_name, var, 'float'))
                else:  # Default to string for other types
                    var = tk.StringVar(value=default_value)
                    widget = ttk.Entry(frame, textvariable=var)
                    widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
                    self.param_widgets.append((param_name, var, 'str'))
            else:
                # No type annotation, default to string
                var = tk.StringVar(value=default_value)
                widget = ttk.Entry(frame, textvariable=var)
                widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.param_widgets.append((param_name, var, 'str'))
    
    def clear_param_frame(self):
        """Clear all widgets from the parameter frame"""
        # Destroy all widgets in the parameter frame
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        
        # Clear the parameter widgets list
        self.param_widgets = []
    
    def execute_function(self):
        """Execute the selected function with the provided parameters"""
        if not self.current_func:
            messagebox.showwarning("Warning", "No function selected")
            return
        
        # Build parameters dictionary
        params = {}
        for param_name, var, param_type in self.param_widgets:
            # Convert the value to the appropriate type
            value = var.get()
            if param_type == 'int':
                try:
                    value = int(value)
                except ValueError:
                    self.console.insert(tk.END, f"Error: Parameter '{param_name}' must be an integer\n")
                    self.console.see(tk.END)
                    return
            elif param_type == 'float':
                try:
                    value = float(value)
                except ValueError:
                    self.console.insert(tk.END, f"Error: Parameter '{param_name}' must be a float\n")
                    self.console.see(tk.END)
                    return
            elif param_type == 'bool':
                value = bool(value)
            
            params[param_name] = value
        
        # Clear console
        self.console.delete(1.0, tk.END)
        
        # Custom stdout to redirect output to the console
        class ConsoleOutput:
            def __init__(self, console):
                self.console = console
            
            def write(self, text):
                self.console.insert(tk.END, text)
                self.console.see(tk.END)
                self.console.update_idletasks()
            
            def flush(self):
                pass
        
        # Redirect stdout
        sys.stdout = ConsoleOutput(self.console)
        
        # Execute function in a separate thread to prevent GUI freezing
        def run_function():
            try:
                self.execute_button.config(state=tk.DISABLED)
                
                # Execute the function with the provided parameters
                result = self.current_func(**params)
                
                # Print the result if any
                if result is not None:
                    print(f"\nResult: {result}")
                
                print("\nExecution completed.")
            except Exception as e:
                print(f"\nError during execution: {str(e)}")
            finally:
                sys.stdout = self.original_stdout
                self.execute_button.config(state=tk.NORMAL)
        
        # Start the execution thread
        threading.Thread(target=run_function, daemon=True).start()
        
def main():
    root = tk.Tk()
    app = UtilityHub(root)
    root.mainloop()

if __name__ == "__main__":
    main()