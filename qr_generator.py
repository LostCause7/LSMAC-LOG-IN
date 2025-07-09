import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import qrcode
from PIL import Image, ImageTk
import os
import datetime
import sqlite3
from database import CheckInDatabase

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("LSMAC Member QR Code Generator")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database
        self.db = CheckInDatabase()
        
        # QR code variables
        self.current_qr_image = None
        self.current_member_id = None
        
        self.setup_gui()
        self.load_members()
        
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="LSMAC Member QR Code Generator", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Member selection and management
        left_panel = tk.Frame(main_frame, bg='#f0f0f0', width=350)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Member management frame
        management_frame = tk.LabelFrame(left_panel, text="Member Management", 
                                       font=('Arial', 12, 'bold'), bg='#f0f0f0')
        management_frame.pack(fill='x', pady=5)
        
        # Management buttons
        mgmt_button_frame = tk.Frame(management_frame, bg='#f0f0f0')
        mgmt_button_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(mgmt_button_frame, text="Add Member", command=self.add_member_dialog,
                bg='#27ae60', fg='white', font=('Arial', 10, 'bold'), 
                padx=10, pady=3).pack(side='left', padx=2)
        
        tk.Button(mgmt_button_frame, text="Edit Member", command=self.edit_member_dialog,
                bg='#f39c12', fg='white', font=('Arial', 10, 'bold'), 
                padx=10, pady=3).pack(side='left', padx=2)
        
        tk.Button(mgmt_button_frame, text="Remove Member", command=self.remove_member_dialog,
                bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'), 
                padx=10, pady=3).pack(side='left', padx=2)
        
        # Member selection frame
        member_frame = tk.LabelFrame(left_panel, text="Select Member", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0')
        member_frame.pack(fill='x', pady=5)
        
        # Search box
        search_frame = tk.Frame(member_frame, bg='#f0f0f0')
        search_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(search_frame, text="Search:", bg='#f0f0f0').pack(side='left')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_members)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side='left', padx=5)
        
        # Members list
        list_frame = tk.Frame(member_frame, bg='#f0f0f0')
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview for members
        columns = ('Name', 'Member ID', 'Email')
        self.members_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=scrollbar.set)
        
        self.members_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind selection event
        self.members_tree.bind('<<TreeviewSelect>>', self.on_member_select)
        
        # Member info frame
        info_frame = tk.LabelFrame(left_panel, text="Member Information", 
                                 font=('Arial', 12, 'bold'), bg='#f0f0f0')
        info_frame.pack(fill='x', pady=10)
        
        self.member_info = tk.Text(info_frame, height=6, font=('Arial', 10), 
                                 state='disabled', bg='white')
        self.member_info.pack(fill='x', padx=10, pady=10)
        
        # Control buttons
        button_frame = tk.Frame(left_panel, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=10)
        
        tk.Button(button_frame, text="Generate QR Code", command=self.generate_qr,
                bg='#27ae60', fg='white', font=('Arial', 10, 'bold'), 
                padx=15, pady=5).pack(fill='x', pady=2)
        
        tk.Button(button_frame, text="Save QR Code", command=self.save_qr,
                bg='#3498db', fg='white', font=('Arial', 10, 'bold'), 
                padx=15, pady=5).pack(fill='x', pady=2)
        
        tk.Button(button_frame, text="Print QR Code", command=self.print_qr,
                bg='#f39c12', fg='white', font=('Arial', 10, 'bold'), 
                padx=15, pady=5).pack(fill='x', pady=2)
        
        tk.Button(button_frame, text="Refresh Members", command=self.load_members,
                bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'), 
                padx=15, pady=5).pack(fill='x', pady=2)
        
        # Right panel - QR code display
        right_panel = tk.Frame(main_frame, bg='#f0f0f0')
        right_panel.pack(side='right', fill='both', expand=True)
        
        # QR code display frame
        qr_frame = tk.LabelFrame(right_panel, text="QR Code Preview", 
                               font=('Arial', 12, 'bold'), bg='#f0f0f0')
        qr_frame.pack(fill='both', expand=True)
        
        # QR code display area
        self.qr_display = tk.Label(qr_frame, text="Select a member to generate QR code", 
                                 bg='white', fg='gray', font=('Arial', 12))
        self.qr_display.pack(expand=True, padx=20, pady=20)
        
        # QR code options frame
        options_frame = tk.LabelFrame(right_panel, text="QR Code Options", 
                                    font=('Arial', 12, 'bold'), bg='#f0f0f0')
        options_frame.pack(fill='x', pady=10)
        
        # Size options
        size_frame = tk.Frame(options_frame, bg='#f0f0f0')
        size_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(size_frame, text="QR Size:", bg='#f0f0f0').pack(side='left')
        self.size_var = tk.StringVar(value="10")
        size_combo = ttk.Combobox(size_frame, textvariable=self.size_var, 
                                values=["5", "8", "10", "12", "15"], width=10)
        size_combo.pack(side='left', padx=5)
        
        # Border options
        border_frame = tk.Frame(options_frame, bg='#f0f0f0')
        border_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(border_frame, text="Border:", bg='#f0f0f0').pack(side='left')
        self.border_var = tk.StringVar(value="4")
        border_combo = ttk.Combobox(border_frame, textvariable=self.border_var, 
                                  values=["2", "4", "6", "8"], width=10)
        border_combo.pack(side='left', padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                            relief='sunken', anchor='w', bg='#ecf0f1')
        status_bar.pack(side='bottom', fill='x')
        
    def add_member_dialog(self):
        """Dialog to add a new member"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Member")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Form fields
        tk.Label(dialog, text="Member ID:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        member_id_entry = tk.Entry(dialog, width=30)
        member_id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Name:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        email_entry = tk.Entry(dialog, width=30)
        email_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Phone:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        phone_entry = tk.Entry(dialog, width=30)
        phone_entry.grid(row=3, column=1, padx=10, pady=5)
        
        def save_member():
            member_id = member_id_entry.get().strip()
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if not member_id or not name:
                messagebox.showerror("Error", "Member ID and Name are required")
                return
                
            if self.db.add_member(member_id, name, email, phone):
                messagebox.showinfo("Success", "Member added successfully!")
                dialog.destroy()
                self.load_members()  # Refresh the list
            else:
                messagebox.showerror("Error", "Member ID already exists")
                
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Save", command=save_member, 
                bg='#27ae60', fg='white', padx=20).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                bg='#95a5a6', fg='white', padx=20).pack(side='left', padx=5)
    
    def edit_member_dialog(self):
        """Dialog to edit an existing member"""
        if not self.current_member_id:
            messagebox.showwarning("Warning", "Please select a member to edit")
            return
        
        # Get current member info
        member = self.db.get_member(self.current_member_id)
        if not member:
            messagebox.showerror("Error", "Member not found")
            return
        
        member_id, name, email, phone, created_date = member
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Member - {name}")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Form fields
        tk.Label(dialog, text="Member ID:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        member_id_entry = tk.Entry(dialog, width=30)
        member_id_entry.insert(0, member_id)
        member_id_entry.config(state='readonly')  # Don't allow editing member ID
        member_id_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Name:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        name_entry = tk.Entry(dialog, width=30)
        name_entry.insert(0, name)
        name_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        email_entry = tk.Entry(dialog, width=30)
        email_entry.insert(0, email or '')
        email_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Phone:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        phone_entry = tk.Entry(dialog, width=30)
        phone_entry.insert(0, phone or '')
        phone_entry.grid(row=3, column=1, padx=10, pady=5)
        
        def update_member():
            new_name = name_entry.get().strip()
            new_email = email_entry.get().strip()
            new_phone = phone_entry.get().strip()
            
            if not new_name:
                messagebox.showerror("Error", "Name is required")
                return
            
            try:
                # Update member in database
                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE members 
                        SET name = ?, email = ?, phone = ?
                        WHERE member_id = ?
                    ''', (new_name, new_email, new_phone, member_id))
                    conn.commit()
                
                messagebox.showinfo("Success", "Member updated successfully!")
                dialog.destroy()
                self.load_members()  # Refresh the list
                self.on_member_select(None)  # Refresh member info display
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update member: {e}")
                
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Update", command=update_member, 
                bg='#f39c12', fg='white', padx=20).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                bg='#95a5a6', fg='white', padx=20).pack(side='left', padx=5)
    
    def remove_member_dialog(self):
        """Dialog to remove a member"""
        if not self.current_member_id:
            messagebox.showwarning("Warning", "Please select a member to remove")
            return
        
        # Get member info for confirmation
        member = self.db.get_member(self.current_member_id)
        if not member:
            messagebox.showerror("Error", "Member not found")
            return
        
        member_id, name, email, phone, created_date = member
        
        # Confirmation dialog
        result = messagebox.askyesno("Confirm Removal", 
                                   f"Are you sure you want to remove this member?\n\n"
                                   f"Member ID: {member_id}\n"
                                   f"Name: {name}\n\n"
                                   f"This action cannot be undone and will also remove all check-in history.")
        
        if result:
            try:
                # Remove member and all associated check-ins
                with sqlite3.connect(self.db.db_path) as conn:
                    cursor = conn.cursor()
                    # First remove check-ins
                    cursor.execute('DELETE FROM check_ins WHERE member_id = ?', (member_id,))
                    # Then remove member
                    cursor.execute('DELETE FROM members WHERE member_id = ?', (member_id,))
                    conn.commit()
                
                messagebox.showinfo("Success", f"Member '{name}' has been removed successfully!")
                self.current_member_id = None
                self.current_qr_image = None
                self.qr_display.config(image='', text="Select a member to generate QR code")
                self.member_info.config(state='normal')
                self.member_info.delete(1.0, tk.END)
                self.member_info.config(state='disabled')
                self.load_members()  # Refresh the list
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove member: {e}")
        
    def load_members(self):
        """Load all members from database"""
        # Clear existing items
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        
        try:
            # Get all members from database
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT name, member_id, email, phone, created_date
                    FROM members
                    ORDER BY name
                ''')
                members = cursor.fetchall()
            
            # Add to treeview
            for name, member_id, email, phone, created_date in members:
                self.members_tree.insert('', 'end', values=(name, member_id, email or ''))
            
            self.status_var.set(f"Loaded {len(members)} members")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load members: {e}")
            self.status_var.set("Error loading members")
    
    def filter_members(self, *args):
        """Filter members based on search text"""
        search_text = self.search_var.get().lower()
        
        # Clear current display
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        
        try:
            # Get filtered members
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT name, member_id, email, phone, created_date
                    FROM members
                    WHERE LOWER(name) LIKE ? OR LOWER(member_id) LIKE ? OR LOWER(email) LIKE ?
                    ORDER BY name
                ''', (f'%{search_text}%', f'%{search_text}%', f'%{search_text}%'))
                members = cursor.fetchall()
            
            # Add filtered results
            for name, member_id, email, phone, created_date in members:
                self.members_tree.insert('', 'end', values=(name, member_id, email or ''))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to filter members: {e}")
    
    def on_member_select(self, event):
        """Handle member selection"""
        selection = self.members_tree.selection()
        if not selection:
            return
        
        # Get selected member
        item = self.members_tree.item(selection[0])
        member_id = item['values'][1]
        
        # Get full member info
        member = self.db.get_member(member_id)
        if member:
            self.current_member_id = member_id
            self.display_member_info(member)
            self.status_var.set(f"Selected: {member[1]}")
    
    def display_member_info(self, member):
        """Display member information"""
        member_id, name, email, phone, created_date = member
        
        self.member_info.config(state='normal')
        self.member_info.delete(1.0, tk.END)
        
        info_text = f"Member ID: {member_id}\n"
        info_text += f"Name: {name}\n"
        if email:
            info_text += f"Email: {email}\n"
        if phone:
            info_text += f"Phone: {phone}\n"
        info_text += f"Member Since: {created_date}\n\n"
        info_text += "Click 'Generate QR Code' to create a QR code for this member."
        
        self.member_info.insert(1.0, info_text)
        self.member_info.config(state='disabled')
    
    def generate_qr(self):
        """Generate QR code for selected member"""
        if not self.current_member_id:
            messagebox.showwarning("Warning", "Please select a member first")
            return
        
        try:
            # Get QR code options
            size = int(self.size_var.get())
            border = int(self.border_var.get())
            
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=size,
                border=border
            )
            
            # Add data
            qr.add_data(self.current_member_id)
            qr.make(fit=True)
            
            # Create image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Resize for display
            display_size = 300
            qr_image_resized = qr_image.resize((display_size, display_size), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(qr_image_resized)
            
            # Update display
            self.qr_display.config(image=photo, text="")
            self.qr_display.image = photo  # Keep reference
            
            # Store original image for saving
            self.current_qr_image = qr_image
            
            self.status_var.set(f"QR code generated for {self.current_member_id}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {e}")
            self.status_var.set("Error generating QR code")
    
    def save_qr(self):
        """Save QR code to file"""
        if not self.current_qr_image:
            messagebox.showwarning("Warning", "Please generate a QR code first")
            return
        
        if not self.current_member_id:
            messagebox.showwarning("Warning", "No member selected")
            return
        
        try:
            # Get save location
            filename = f"QR_{self.current_member_id}_{datetime.date.today().strftime('%Y%m%d')}.png"
            filepath = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialname=filename
            )
            
            if filepath:
                # Save the image
                self.current_qr_image.save(filepath)
                messagebox.showinfo("Success", f"QR code saved to:\n{filepath}")
                self.status_var.set(f"QR code saved: {os.path.basename(filepath)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save QR code: {e}")
            self.status_var.set("Error saving QR code")
    
    def print_qr(self):
        """Print QR code"""
        if not self.current_qr_image:
            messagebox.showwarning("Warning", "Please generate a QR code first")
            return
        
        try:
            # Create a temporary file for printing
            temp_file = f"temp_qr_{self.current_member_id}.png"
            self.current_qr_image.save(temp_file)
            
            # Open with default image viewer (which usually has print option)
            os.startfile(temp_file)
            
            self.status_var.set("QR code opened for printing")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open QR code for printing: {e}")
            self.status_var.set("Error opening for print")

def main():
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 