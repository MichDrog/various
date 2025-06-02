import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime

class SaveUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Saving System")
        
        # Initialize settings
        self.settings_file = "saveui_settings.json"
        self.settings = {
            "source_path": "",
            "destination_path": "",
            "save_slots": {}
        }
        
        # Load settings from JSON
        self.load_settings()
        
        # Create UI elements
        self.create_widgets()
    
    def create_widgets(self):
        # Main label
        tk.Label(self.root, text="Advanced Saving System", font=("Arial", 16)).pack(pady=10)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.path_tab = ttk.Frame(self.notebook)
        self.save_tab = ttk.Frame(self.notebook)
        self.load_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.path_tab, text="Paths")
        self.notebook.add(self.save_tab, text="Save Game")
        self.notebook.add(self.load_tab, text="Load Game")
        
        # Paths Tab
        self.create_paths_tab()
        # Save Tab
        self.create_save_tab()
        # Load Tab
        self.create_load_tab()
    
    def create_paths_tab(self):
        # Source Path
        source_frame = tk.Frame(self.path_tab)
        source_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Label(source_frame, text="Source Path:").pack(side=tk.LEFT)
        self.source_entry = tk.Entry(source_frame, width=50)
        self.source_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.source_entry.insert(0, self.settings["source_path"])
        
        tk.Button(source_frame, text="Browse", command=self.browse_source).pack(side=tk.LEFT, padx=5)
        tk.Button(source_frame, text="Save", command=lambda: self.save_path("source")).pack(side=tk.LEFT)
        
        # Destination Path
        dest_frame = tk.Frame(self.path_tab)
        dest_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Label(dest_frame, text="Destination Path:").pack(side=tk.LEFT)
        self.dest_entry = tk.Entry(dest_frame, width=50)
        self.dest_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.dest_entry.insert(0, self.settings["destination_path"])
        
        tk.Button(dest_frame, text="Browse", command=self.browse_destination).pack(side=tk.LEFT, padx=5)
        tk.Button(dest_frame, text="Save", command=lambda: self.save_path("destination")).pack(side=tk.LEFT)
    
    def create_save_tab(self):
        # Save Name Entry
        name_frame = tk.Frame(self.save_tab)
        name_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(name_frame, text="Save Name:").pack(side=tk.LEFT)
        self.save_name_entry = tk.Entry(name_frame, width=40)
        self.save_name_entry.pack(side=tk.LEFT, padx=5)
        
        # Slot Selection
        slot_frame = tk.Frame(self.save_tab)
        slot_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Label(slot_frame, text="Slot:").pack(side=tk.LEFT)
        self.save_slot_var = tk.StringVar()
        self.save_slot_combobox = ttk.Combobox(slot_frame, textvariable=self.save_slot_var, width=10)
        self.save_slot_combobox['values'] = list(range(1, 11))
        self.save_slot_combobox.current(0)
        self.save_slot_combobox.pack(side=tk.LEFT, padx=5)
        
        # Save Button
        tk.Button(self.save_tab, text="Save Game", command=self.save_game, width=20).pack(pady=10)
        
        # Existing Saves Frame
        existing_frame = tk.LabelFrame(self.save_tab, text="Existing Saves")
        existing_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Treeview for existing saves
        columns = ("slot", "name", "date")
        self.save_tree = ttk.Treeview(existing_frame, columns=columns, show="headings")
        
        self.save_tree.heading("slot", text="Slot")
        self.save_tree.heading("name", text="Save Name")
        self.save_tree.heading("date", text="Date")
        
        self.save_tree.column("slot", width=50, anchor=tk.CENTER)
        self.save_tree.column("name", width=150)
        self.save_tree.column("date", width=120)
        
        self.save_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Delete Button
        del_button_frame = tk.Frame(existing_frame)
        del_button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(del_button_frame, text="Delete Selected Save", 
                command=self.delete_save, width=20).pack(side=tk.RIGHT)
        
        # Populate existing saves
        self.update_save_tree()
    
    def create_load_tab(self):
        # Treeview for loadable saves
        columns = ("slot", "name", "date")
        self.load_tree = ttk.Treeview(self.load_tab, columns=columns, show="headings")
        
        self.load_tree.heading("slot", text="Slot")
        self.load_tree.heading("name", text="Save Name")
        self.load_tree.heading("date", text="Date")
        
        self.load_tree.column("slot", width=50, anchor=tk.CENTER)
        self.load_tree.column("name", width=150)
        self.load_tree.column("date", width=120)
        
        self.load_tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Button Frame
        button_frame = tk.Frame(self.load_tab)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Load Button
        tk.Button(button_frame, text="Load Selected Save", 
                command=self.load_game, width=20).pack(side=tk.LEFT)
        
        # Delete Button
        tk.Button(button_frame, text="Delete Selected Save", 
                command=self.delete_save, width=20).pack(side=tk.RIGHT)
        
        # Populate loadable saves
        self.update_load_tree()
    
    def browse_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_entry.delete(0, tk.END)
            self.source_entry.insert(0, path)
    
    def browse_destination(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, path)
    
    def save_path(self, path_type):
        if path_type == "source":
            self.settings["source_path"] = self.source_entry.get()
        else:
            self.settings["destination_path"] = self.dest_entry.get()
        
        self.save_settings()
        messagebox.showinfo("Success", f"{path_type.capitalize()} path saved!")
    
    def load_settings(self):
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as f:
                    self.settings = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {str(e)}")
    
    def save_settings(self):
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def validate_paths(self):
        if not self.settings["source_path"] or not self.settings["destination_path"]:
            messagebox.showerror("Error", "Both source and destination paths must be set!")
            return False
        
        if not os.path.exists(self.settings["source_path"]):
            messagebox.showerror("Error", "Source path does not exist!")
            return False
        
        if not os.path.exists(self.settings["destination_path"]):
            messagebox.showerror("Error", "Destination path does not exist!")
            return False
        
        return True
    
    def update_save_tree(self):
        # Clear existing items
        for item in self.save_tree.get_children():
            self.save_tree.delete(item)
        
        # Add current saves
        for slot, save_info in self.settings["save_slots"].items():
            self.save_tree.insert("", tk.END, values=(
                slot,
                save_info.get("name", "Unnamed"),
                save_info.get("date", "Unknown")
            ))
    
    def update_load_tree(self):
        # Clear existing items
        for item in self.load_tree.get_children():
            self.load_tree.delete(item)
        
        # Check if destination path exists
        dest_path = self.settings.get("destination_path", "")
        if not dest_path or not os.path.exists(dest_path):
            return
        
        # Look for save slots in destination
        for slot in range(1, 11):
            slot_path = os.path.join(dest_path, f"slot_{slot}")
            if os.path.exists(slot_path):
                # Try to read the save info
                info_path = os.path.join(slot_path, "save_info.json")
                if os.path.exists(info_path):
                    try:
                        with open(info_path, "r") as f:
                            save_info = json.load(f)
                        self.load_tree.insert("", tk.END, values=(
                            slot,
                            save_info.get("name", "Unnamed"),
                            save_info.get("date", "Unknown")
                        ))
                    except:
                        pass
    
    def get_selected_slot(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            return None
        item = tree.item(selected_item[0])
        return item['values'][0]
    
    def delete_save(self):
        # Determine which tree is active based on current tab
        current_tab = self.notebook.index(self.notebook.select())
        
        if current_tab == 1:  # Save tab
            tree = self.save_tree
        elif current_tab == 2:  # Load tab
            tree = self.load_tree
        else:
            return
        
        slot = self.get_selected_slot(tree)
        if slot is None:
            messagebox.showerror("Error", "No save selected!")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", f"Delete save in slot {slot}?"):
            return
        
        try:
            dest_path = self.settings["destination_path"]
            slot_dir = os.path.join(dest_path, f"slot_{slot}")
            
            if os.path.exists(slot_dir):
                shutil.rmtree(slot_dir)
                
                # Update settings if this was a known save
                if str(slot) in self.settings["save_slots"]:
                    del self.settings["save_slots"][str(slot)]
                    self.save_settings()
                
                # Update UI
                self.update_save_tree()
                self.update_load_tree()
                
                messagebox.showinfo("Success", f"Save in slot {slot} deleted!")
            else:
                messagebox.showerror("Error", f"No save found in slot {slot}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete save: {str(e)}")
    
    def save_game(self):
        if not self.validate_paths():
            return
        
        slot = self.save_slot_var.get()
        save_name = self.save_name_entry.get().strip() or f"Save {slot}"
        
        try:
            source = self.settings["source_path"]
            dest = self.settings["destination_path"]
            
            # Create slot directory
            slot_dir = os.path.join(dest, f"slot_{slot}")
            os.makedirs(slot_dir, exist_ok=True)
            
            # Copy SaveData files
            for file in ["SaveData.json", "SaveData.json.backup"]:
                src_file = os.path.join(source, file)
                if os.path.exists(src_file):
                    shutil.copy2(src_file, slot_dir)
            
            # Copy Games folder
            games_src = os.path.join(source, "Games")
            games_dest = os.path.join(slot_dir, "Games")
            
            if os.path.exists(games_src):
                if os.path.exists(games_dest):
                    shutil.rmtree(games_dest)
                shutil.copytree(games_src, games_dest)
            
            # Save metadata
            save_info = {
                "name": save_name,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "slot": slot
            }
            
            with open(os.path.join(slot_dir, "save_info.json"), "w") as f:
                json.dump(save_info, f, indent=4)
            
            # Update settings
            self.settings["save_slots"][slot] = save_info
            self.save_settings()
            
            # Update UI
            self.update_save_tree()
            self.update_load_tree()
            
            messagebox.showinfo("Success", f"Game saved to slot {slot} successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save game: {str(e)}")
    
    def load_game(self):
        if not self.validate_paths():
            return
        
        slot = self.get_selected_slot(self.load_tree)
        if slot is None:
            messagebox.showerror("Error", "No save selected!")
            return
        
        try:
            source = self.settings["source_path"]
            dest = self.settings["destination_path"]
            slot_dir = os.path.join(dest, f"slot_{slot}")
            
            # Verify slot exists
            if not os.path.exists(slot_dir):
                messagebox.showerror("Error", f"Save slot {slot} not found!")
                return
            
            # Copy SaveData files from slot to source
            for file in ["SaveData.json", "SaveData.json.backup"]:
                src_file = os.path.join(slot_dir, file)
                if os.path.exists(src_file):
                    shutil.copy2(src_file, source)
            
            # Copy Games folder from slot to source
            games_src = os.path.join(slot_dir, "Games")
            games_dest = os.path.join(source, "Games")
            
            if os.path.exists(games_src):
                if os.path.exists(games_dest):
                    shutil.rmtree(games_dest)
                shutil.copytree(games_src, games_dest)
            
            messagebox.showinfo("Success", f"Game loaded from slot {slot} successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load game: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("650x550")
    app = SaveUI(root)
    root.mainloop()