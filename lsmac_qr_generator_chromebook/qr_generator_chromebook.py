#!/usr/bin/env python3
"""
LSMAC QR Generator - Chrome OS Compatible Version
Runs on Chromebook's Linux environment
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import qrcode
from PIL import Image, ImageTk
import os
import datetime
import requests
import json
import subprocess
import sys

# Supabase configuration
SUPABASE_URL = "https://xbqunvlxqvpmacjcrasc.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhicXVudmx4cXZwbWFjamNyYXNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMjQ0MjUsImV4cCI6MjA2NzYwMDQyNX0.DcGWWatFg2faO6g7iBEiyjKb4pxlKwHrya005nZ4Pns"

headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def get_or_create_member(member_id, name, email, phone, member_since):
    """Create or get member from Supabase"""
    try:
        # Check if member exists
        r = requests.get(f"{SUPABASE_URL}/rest/v1/members?member_id=eq.{member_id}", headers=headers)
        if r.status_code == 200 and r.json():
            return r.json()[0]
        
        # Create member
        data = {
            "member_id": member_id,
            "name": name,
            "email": email,
            "phone": phone,
            "member_since": member_since
        }
        r = requests.post(f"{SUPABASE_URL}/rest/v1/members", headers=headers, json=data)
        if r.status_code in (200, 201):
            return r.json()[0]
        else:
            raise Exception(f"Failed to create member: {r.text}")
    except Exception as e:
        raise Exception(f"Database error: {e}")

def fetch_all_members():
    """Fetch all members from Supabase"""
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/members?select=member_id,name,email,phone,member_since", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error fetching members:", response.status_code, response.text)
            return []
    except Exception as e:
        print("Error:", e)
        return []

def get_downloads_folder():
    """Get the Downloads folder path for Chrome OS"""
    # Try to get Downloads folder from environment
    downloads = os.path.expanduser("~/Downloads")
    if not os.path.exists(downloads):
        # Create Downloads folder if it doesn't exist
        os.makedirs(downloads, exist_ok=True)
    return downloads

class ChromeOSQRGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("LSMAC QR Codes - Chrome OS")
        self.root.geometry("1000x700")
        
        # Chrome OS specific styling
        self.root.configure(bg="#f8f9fa")
        
        # QR code variables
        self.current_qr_image = None
        self.current_member_id = None
        self.members = []
        
        self.setup_gui()
        self.load_members()

    def setup_gui(self):
        """Setup the GUI for Chrome OS"""
        # Main container
        main_frame = tk.Frame(self.root, bg="#f8f9fa")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg="#0074D9", height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="LSMAC QR Code Generator", 
                              font=("Arial", 24, "bold"), fg="white", bg="#0074D9")
        title_label.pack(expand=True)

        # Content area
        content_frame = tk.Frame(main_frame, bg="#f8f9fa")
        content_frame.pack(fill="both", expand=True)

        # Left panel - Member management
        left_panel = tk.Frame(content_frame, bg="white", relief="solid", bd=1)
        left_panel.pack(side="left", fill="y", padx=(0, 10))

        # Member management section
        mgmt_frame = tk.LabelFrame(left_panel, text="Member Management", 
                                  font=("Arial", 12, "bold"), bg="white")
        mgmt_frame.pack(fill="x", padx=10, pady=10)

        # Buttons
        btn_frame = tk.Frame(mgmt_frame, bg="white")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="Add Member", command=self.add_member_dialog,
                 bg="#0074D9", fg="white", font=("Arial", 10, "bold"),
                 relief="flat", padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Edit Member", command=self.edit_member_dialog,
                 bg="#FF4136", fg="white", font=("Arial", 10, "bold"),
                 relief="flat", padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Delete Member", command=self.delete_member_dialog,
                 bg="#111111", fg="white", font=("Arial", 10, "bold"),
                 relief="flat", padx=20, pady=5).pack(side="left", padx=5)

        # Search section
        search_frame = tk.LabelFrame(left_panel, text="Search Members", 
                                   font=("Arial", 12, "bold"), bg="white")
        search_frame.pack(fill="x", padx=10, pady=10)

        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_members)
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                              font=("Arial", 10), relief="solid", bd=1)
        search_entry.pack(fill="x", padx=10, pady=10)

        # Member list
        list_frame = tk.LabelFrame(left_panel, text="Members", 
                                 font=("Arial", 12, "bold"), bg="white")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview for members
        columns = ('Name', 'Member ID', 'Email')
        self.members_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=scrollbar.set)
        
        self.members_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.members_tree.bind('<<TreeviewSelect>>', self.on_member_select)

        # Right panel - QR code
        right_panel = tk.Frame(content_frame, bg="white", relief="solid", bd=1)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        # Member info
        info_frame = tk.LabelFrame(right_panel, text="Member Information", 
                                 font=("Arial", 12, "bold"), bg="white")
        info_frame.pack(fill="x", padx=10, pady=10)

        self.member_info = tk.Text(info_frame, height=6, font=("Arial", 10), 
                                 state='disabled', bg='#f8f9fa', relief="solid", bd=1)
        self.member_info.pack(fill="x", padx=10, pady=10)

        # QR code display
        qr_frame = tk.LabelFrame(right_panel, text="QR Code", 
                               font=("Arial", 12, "bold"), bg="white")
        qr_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.qr_display = tk.Label(qr_frame, text="Select a member to generate QR code", 
                                  bg='#f8f9fa', fg='gray', font=("Arial", 12, "bold"))
        self.qr_display.pack(expand=True, padx=20, pady=20)

        # QR code options
        options_frame = tk.LabelFrame(right_panel, text="QR Code Options", 
                                    font=("Arial", 12, "bold"), bg="white")
        options_frame.pack(fill="x", padx=10, pady=10)

        # Size and border controls
        controls_frame = tk.Frame(options_frame, bg="white")
        controls_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(controls_frame, text="Size:", bg="white", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.size_var = tk.StringVar(value="10")
        size_combo = ttk.Combobox(controls_frame, textvariable=self.size_var, 
                                 values=["5", "8", "10", "12", "15"], width=10)
        size_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(controls_frame, text="Border:", bg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5)
        self.border_var = tk.StringVar(value="4")
        border_combo = ttk.Combobox(controls_frame, textvariable=self.border_var, 
                                   values=["2", "4", "6", "8"], width=10)
        border_combo.grid(row=0, column=3, padx=5, pady=5)

        # Action buttons
        action_frame = tk.Frame(right_panel, bg="white")
        action_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(action_frame, text="Generate QR Code", command=self.generate_qr,
                 bg="#0074D9", fg="white", font=("Arial", 10, "bold"),
                 relief="flat", padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(action_frame, text="Save QR Code", command=self.save_qr,
                 bg="#2ECC40", fg="white", font=("Arial", 10, "bold"),
                 relief="flat", padx=20, pady=5).pack(side="left", padx=5)
        
        tk.Button(action_frame, text="Print QR Code", command=self.print_qr,
                 bg="#FF4136", fg="white", font=("Arial", 10, "bold"),
                 relief="flat", padx=20, pady=5).pack(side="left", padx=5)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                            relief='flat', anchor='w', bg='#e9ecef', 
                            font=("Arial", 9, "bold"))
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
        tk.Label(dialog, text="Member ID:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        member_id_entry = tk.Entry(dialog, width=30, font=("Arial", 10))
        member_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Name:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        name_entry = tk.Entry(dialog, width=30, font=("Arial", 10))
        name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Email:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        email_entry = tk.Entry(dialog, width=30, font=("Arial", 10))
        email_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Phone:", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=5, sticky='w')
        phone_entry = tk.Entry(dialog, width=30, font=("Arial", 10))
        phone_entry.grid(row=3, column=1, padx=10, pady=5)

        def save_member():
            member_id = member_id_entry.get().strip()
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()

            if not member_id or not name:
                messagebox.showerror("Error", "Member ID and Name are required")
                return

            try:
                current_date = datetime.date.today().strftime('%Y-%m-%d')
                member_data = get_or_create_member(member_id, name, email, phone, current_date)
                messagebox.showinfo("Success", "Member added successfully!")
                dialog.destroy()
                self.load_members()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add member: {e}")

        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="Save", command=save_member,
                bg='#27ae60', fg='white', padx=20, font=("Arial", 10)).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                bg='#95a5a6', fg='white', padx=20, font=("Arial", 10)).pack(side='left', padx=5)

    def edit_member_dialog(self):
        """Dialog to edit an existing member"""
        if not self.current_member_id:
            messagebox.showwarning("Warning", "Please select a member to edit")
            return

        # Get current member info
        member = None
        for m in self.members:
            if m.get('member_id') == self.current_member_id:
                member = m
                break

        if not member:
            messagebox.showerror("Error", "Member not found")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Member - {member.get('name', '')}")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()

        # Form fields
        tk.Label(dialog, text="Member ID:", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        member_id_entry = tk.Entry(dialog, width=30, font=("Arial", 10))
        member_id_entry.insert(0, member.get('member_id', ''))
        member_id_entry.config(state='readonly')
        member_id_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Name:", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        name_entry = tk.Entry(dialog, width=30, font=("Arial", 10))
        name_entry.insert(0, member.get('name', ''))
        name_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Email:", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky='w')
        email_entry = tk.Entry(dialog, width=30, font=("Arial", 10))
        email_entry.insert(0, member.get('email', ''))
        email_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Phone:", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=5, sticky='w')
        phone_entry = tk.Entry(dialog, width=30, font=("Arial", 10))
        phone_entry.insert(0, member.get('phone', ''))
        phone_entry.grid(row=3, column=1, padx=10, pady=5)

        def update_member():
            new_name = name_entry.get().strip()
            new_email = email_entry.get().strip()
            new_phone = phone_entry.get().strip()

            if not new_name:
                messagebox.showerror("Error", "Name is required")
                return

            try:
                # Update member in Supabase
                response = requests.patch(
                    f"{SUPABASE_URL}/rest/v1/members?member_id=eq.{member.get('member_id')}",
                    headers=headers,
                    json={
                        "name": new_name,
                        "email": new_email,
                        "phone": new_phone
                    }
                )

                if response.status_code in (200, 204):
                    messagebox.showinfo("Success", "Member updated successfully!")
                    dialog.destroy()
                    self.load_members()
                else:
                    messagebox.showerror("Error", f"Failed to update member: {response.text}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update member: {e}")

        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="Update", command=update_member,
                bg='#f39c12', fg='white', padx=20, font=("Arial", 10)).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                bg='#95a5a6', fg='white', padx=20, font=("Arial", 10)).pack(side='left', padx=5)

    def delete_member_dialog(self):
        """Dialog to delete a member"""
        if not self.current_member_id:
            messagebox.showwarning("Warning", "Please select a member to delete")
            return

        member = None
        for m in self.members:
            if m.get('member_id') == self.current_member_id:
                member = m
                break

        if not member:
            messagebox.showerror("Error", "Member not found")
            return

        result = messagebox.askyesno("Confirm Delete",
                                   f"Are you sure you want to delete {member.get('name')}?")

        if result:
            try:
                response = requests.delete(
                    f"{SUPABASE_URL}/rest/v1/members?member_id=eq.{member.get('member_id')}",
                    headers=headers
                )

                if response.status_code in (200, 204):
                    messagebox.showinfo("Success", f"Member '{member.get('name')}' deleted successfully!")
                    self.current_member_id = None
                    self.current_qr_image = None
                    self.qr_display.config(image='', text="Select a member to generate QR code")
                    self.member_info.config(state='normal')
                    self.member_info.delete(1.0, tk.END)
                    self.member_info.config(state='disabled')
                    self.load_members()
                else:
                    messagebox.showerror("Error", f"Failed to delete member: {response.text}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete member: {e}")

    def load_members(self):
        """Load members from database"""
        try:
            self.members = fetch_all_members()
            
            # Clear existing items
            for item in self.members_tree.get_children():
                self.members_tree.delete(item)
            
            # Insert members into the Treeview
            for member in self.members:
                self.members_tree.insert('', 'end', values=(
                    member.get('name', ''),
                    member.get('member_id', ''),
                    member.get('email', '')
                ))

            self.status_var.set(f"Loaded {len(self.members)} members")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load members: {e}")
            self.status_var.set("Error loading members")

    def filter_members(self, *args):
        """Filter members based on search text"""
        search_text = self.search_var.get().lower()

        # Clear current display
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)

        # Filter from loaded members
        filtered_members = []
        for member in self.members:
            if (search_text in member.get('name', '').lower() or
                search_text in member.get('member_id', '').lower() or
                search_text in member.get('email', '').lower()):
                filtered_members.append(member)

        # Add filtered results
        for member in filtered_members:
            self.members_tree.insert('', 'end', values=(
                member.get('name', ''),
                member.get('member_id', ''),
                member.get('email', '')
            ))

    def on_member_select(self, event):
        """Handle member selection"""
        selection = self.members_tree.selection()
        if not selection:
            return

        item = self.members_tree.item(selection[0])
        member_id = item['values'][1]

        selected_member = None
        for member in self.members:
            if member.get('member_id') == member_id:
                selected_member = member
                break

        if selected_member:
            self.current_member_id = member_id
            self.display_member_info(selected_member)
            self.status_var.set(f"Selected: {selected_member.get('name', '')}")

    def display_member_info(self, member):
        """Display member information"""
        self.member_info.config(state='normal')
        self.member_info.delete(1.0, tk.END)

        info_text = f"Member ID: {member.get('member_id', '')}\n"
        info_text += f"Name: {member.get('name', '')}\n"
        if member.get('email'):
            info_text += f"Email: {member.get('email')}\n"
        if member.get('phone'):
            info_text += f"Phone: {member.get('phone')}\n"
        info_text += f"Member Since: {member.get('member_since', '')}\n\n"
        info_text += "Click 'Generate QR Code' to create a QR code for this member."

        self.member_info.insert(1.0, info_text)
        self.member_info.config(state='disabled')

    def generate_qr(self):
        """Generate QR code for selected member"""
        if not self.current_member_id:
            messagebox.showwarning("Warning", "Please select a member first")
            return

        try:
            size = int(self.size_var.get())
            border = int(self.border_var.get())

            member_data = None
            for member in self.members:
                if member.get('member_id') == self.current_member_id:
                    member_data = member
                    break

            if not member_data:
                messagebox.showerror("Error", "Member not found in database.")
                return

            member_id = member_data.get('member_id')

            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=size,
                border=border
            )

            qr.add_data(member_id)
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
            self.qr_display.image = photo

            # Store original image for saving
            self.current_qr_image = qr_image

            self.status_var.set(f"QR code generated for {self.current_member_id}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {e}")
            self.status_var.set("Error generating QR code")

    def save_qr(self):
        """Save QR code to Downloads folder"""
        if not self.current_qr_image:
            messagebox.showwarning("Warning", "Please generate a QR code first")
            return

        if not self.current_member_id:
            messagebox.showwarning("Warning", "No member selected")
            return

        try:
            # Get Downloads folder
            downloads_folder = get_downloads_folder()
            filename = f"QR_{self.current_member_id}_{datetime.date.today().strftime('%Y%m%d')}.png"
            filepath = os.path.join(downloads_folder, filename)

            # Save the image
            self.current_qr_image.save(filepath)
            messagebox.showinfo("Success", f"QR code saved to Downloads folder:\n{filename}")
            self.status_var.set(f"QR code saved: {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save QR code: {e}")
            self.status_var.set("Error saving QR code")

    def print_qr(self):
        """Print QR code using Chrome OS printing"""
        if not self.current_qr_image:
            messagebox.showwarning("Warning", "Please generate a QR code first")
            return

        try:
            # Save temporary file
            downloads_folder = get_downloads_folder()
            temp_file = os.path.join(downloads_folder, f"temp_qr_{self.current_member_id}.png")
            self.current_qr_image.save(temp_file)

            # Open with Chrome OS file viewer (which has print option)
            if sys.platform == "linux":
                subprocess.run(["xdg-open", temp_file])
            else:
                os.startfile(temp_file)

            self.status_var.set("QR code opened for printing")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open QR code for printing: {e}")
            self.status_var.set("Error opening for print")

def main():
    """Main function"""
    root = tk.Tk()
    app = ChromeOSQRGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 