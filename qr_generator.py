import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import qrcode
from PIL import Image, ImageTk
import os
import datetime
import sqlite3
from database import CheckInDatabase
import requests

SUPABASE_URL = "https://xbqunvlxqvpmacjcrasc.supabase.co"
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhicXVudmx4cXZwbWFjamNyYXNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMjQ0MjUsImV4cCI6MjA2NzYwMDQyNX0.DcGWWatFg2faO6g7iBEiyjKb4pxlKwHrya005nZ4Pns"
headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def get_or_create_member(member_id, name, email, phone, member_since):
    # Check if member exists
    r = requests.get(f"{SUPABASE_URL}/rest/v1/members?member_id=eq.{member_id}", headers=headers)
    if r.status_code == 200 and r.json():
        return r.json()[0]  # Return existing member
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
        try:
            return r.json()[0]
        except Exception as e:
            print("Response content:", r.text)
            raise Exception(f"Failed to parse response JSON: {e}")
    else:
        print("Error response:", r.status_code, r.text)
        raise Exception(f"Failed to create member: {r.text}")

def fetch_all_members():
    response = requests.get(f"{SUPABASE_URL}/rest/v1/members?select=member_id,name,email,phone,member_since", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching members:", response.status_code, response.text)
        return []

class QRCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("LSMAC QR Codes")
        self.root.geometry("950x700")
        self.root.configure(bg="#181A1B")  # dark background
        try:
            # App icon (window/taskbar): LOGO4.png
            self.icon_img = Image.open("LOGO4.png")
            self.icon_img = self.icon_img.resize((60, 60), Image.LANCZOS)
            self.icon_tk = ImageTk.PhotoImage(self.icon_img)
            self.root.iconphoto(True, self.icon_tk)
            # Centered logo: LOGO3.png
            self.logo_img = Image.open("LOGO3.png")
            self.logo_img = self.logo_img.resize((60, 60), Image.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(self.logo_img)
        except Exception:
            self.logo_tk = None
        # QR code variables
        self.current_qr_image = None
        self.current_member_id = None
        self.members = []
        self.setup_gui()
        self.load_members()

    def setup_gui(self):
        # Top bar with centered logo and title (compact)
        topbar = tk.Frame(self.root, bg="#181A1B", height=80)
        topbar.pack(fill="x", padx=0, pady=0)
        topbar.pack_propagate(False)
        if self.logo_tk:
            wide_logo_img = self.logo_img.resize((120, 30), Image.LANCZOS)
            self.wide_logo_tk = ImageTk.PhotoImage(wide_logo_img)
            logo_label = tk.Label(topbar, image=self.wide_logo_tk, bg="#181A1B")
            logo_label.pack(side="top", anchor="center", pady=(5, 0))
        title_label = tk.Label(topbar, text="QR Codes", font=("Segoe UI", 22, "bold"), fg="#ffffff", bg="#181A1B")
        title_label.pack(side="top", anchor="center", pady=(2, 6))

        # Main content frame
        main_frame = tk.Frame(self.root, bg="#181A1B")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left panel (member selection/info only)
        left_panel = tk.Frame(main_frame, bg="#23272A", width=320, bd=0, relief="flat")
        left_panel.pack(side="left", fill="y", padx=(0, 16), pady=0)
        left_panel.pack_propagate(False)

        # Member management
        management_frame = tk.LabelFrame(left_panel, text="Member Management", font=("Segoe UI", 11, "bold"), fg="#0074D9", bg="#23272A", bd=0, relief="flat", labelanchor="n")
        management_frame.pack(fill="x", pady=(10, 6), padx=0)
        mgmt_button_frame = tk.Frame(management_frame, bg="#23272A")
        mgmt_button_frame.pack(fill="x", padx=8, pady=6)
        tk.Button(mgmt_button_frame, text="Add", command=self.add_member_dialog, bg="#0074D9", fg="white", font=("Segoe UI", 10, "bold"), bd=0, relief="flat", activebackground="#005fa3", activeforeground="white", width=8).pack(side="left", padx=2)
        tk.Button(mgmt_button_frame, text="Edit", command=self.edit_member_dialog, bg="#FF4136", fg="white", font=("Segoe UI", 10, "bold"), bd=0, relief="flat", activebackground="#b82a1c", activeforeground="white", width=8).pack(side="left", padx=2)
        tk.Button(mgmt_button_frame, text="Remove", command=self.remove_member_dialog, bg="#111111", fg="#FF4136", font=("Segoe UI", 10, "bold"), bd=0, relief="flat", activebackground="#333", activeforeground="#FF4136", width=8).pack(side="left", padx=2)

        # Member selection
        member_frame = tk.LabelFrame(left_panel, text="Select Member", font=("Segoe UI", 11, "bold"), fg="#0074D9", bg="#23272A", bd=0, relief="flat", labelanchor="n")
        member_frame.pack(fill="x", pady=(0, 6), padx=0)
        search_frame = tk.Frame(member_frame, bg="#23272A")
        search_frame.pack(fill="x", padx=8, pady=6)
        tk.Label(search_frame, text="Search:", bg="#23272A", fg="#ffffff", font=("Segoe UI", 9)).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_members)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=18, font=("Segoe UI", 9), bg="#181A1B", fg="#ffffff", insertbackground="#ffffff", relief="flat")
        search_entry.pack(side="left", padx=5)
        list_frame = tk.Frame(member_frame, bg="#23272A")
        list_frame.pack(fill='both', expand=True, padx=8, pady=6)
        columns = ('Name', 'Member ID', 'Email')
        self.members_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10, style="Custom.Treeview")
        for col in columns:
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=90)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=scrollbar.set)
        self.members_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        self.members_tree.bind('<<TreeviewSelect>>', self.on_member_select)
        # Style for Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview", background="#23272A", fieldbackground="#23272A", foreground="#ffffff", rowheight=26, borderwidth=0, font=("Segoe UI", 9))
        style.map("Custom.Treeview", background=[('selected', '#0074D9')], foreground=[('selected', '#ffffff')])
        # Member info
        info_frame = tk.LabelFrame(left_panel, text="Member Information", font=("Segoe UI", 11, "bold"), fg="#0074D9", bg="#23272A", bd=0, relief="flat", labelanchor="n")
        info_frame.pack(fill='x', pady=6, padx=0)
        self.member_info = tk.Text(info_frame, height=6, font=("Segoe UI", 9), state='disabled', bg='#181A1B', fg="#ffffff", relief="flat", wrap="word")
        self.member_info.pack(fill='x', padx=8, pady=8)

        # Right panel
        right_panel = tk.Frame(main_frame, bg="#23272A", bd=0, relief="flat")
        right_panel.pack(side='left', fill='both', expand=True, padx=(0, 0), pady=0)
        # QR code preview
        qr_frame = tk.LabelFrame(right_panel, text="QR Code Preview", font=("Segoe UI", 11, "bold"), fg="#0074D9", bg="#23272A", bd=0, relief="flat", labelanchor="n")
        qr_frame.pack(fill='both', expand=True, padx=0, pady=(10, 6))
        self.qr_display = tk.Label(qr_frame, text="Select a member to generate QR code", bg='#181A1B', fg='gray', font=("Segoe UI", 13, "bold"), relief="flat")
        self.qr_display.pack(expand=True, padx=20, pady=20)
        # QR code options box (compact, visually distinct)
        options_box = tk.Frame(right_panel, bg="#181A1B", bd=1, relief="groove", highlightbackground="#0074D9", highlightthickness=1)
        options_box.pack(fill='x', pady=(0, 8), padx=0)
        tk.Label(options_box, text="QR Code Options", bg="#181A1B", fg="#0074D9", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=(6, 2))
        tk.Label(options_box, text="QR Size:", bg="#181A1B", fg="#ffffff", font=("Segoe UI", 9)).grid(row=1, column=0, sticky="e", padx=6, pady=4)
        self.size_var = tk.StringVar(value="10")
        size_combo = ttk.Combobox(options_box, textvariable=self.size_var, values=["5", "8", "10", "12", "15"], width=8, font=("Segoe UI", 9))
        size_combo.grid(row=1, column=1, sticky="w", padx=2, pady=4)
        tk.Label(options_box, text="Border:", bg="#181A1B", fg="#ffffff", font=("Segoe UI", 9)).grid(row=1, column=2, sticky="e", padx=6, pady=4)
        self.border_var = tk.StringVar(value="4")
        border_combo = ttk.Combobox(options_box, textvariable=self.border_var, values=["2", "4", "6", "8"], width=8, font=("Segoe UI", 9))
        border_combo.grid(row=1, column=3, sticky="w", padx=2, pady=4)
        # Action buttons (side by side)
        button_box = tk.Frame(right_panel, bg="#23272A")
        button_box.pack(fill='x', pady=(0, 10), padx=0)
        btn_style = {"font": ("Segoe UI", 10, "bold"), "bd": 0, "relief": "flat", "height": 2, "width": 16}
        tk.Button(button_box, text="Generate QR Code", command=self.generate_qr, bg="#0074D9", fg='white', activebackground="#005fa3", activeforeground="white", **btn_style).pack(side='left', padx=6)
        tk.Button(button_box, text="Save QR Code", command=self.save_qr, bg="#ffffff", fg='#0074D9', activebackground="#e6e6e6", activeforeground="#0074D9", **btn_style).pack(side='left', padx=6)
        tk.Button(button_box, text="Print QR Code", command=self.print_qr, bg="#FF4136", fg='white', activebackground="#b82a1c", activeforeground="white", **btn_style).pack(side='left', padx=6)
        tk.Button(button_box, text="Refresh Members", command=self.load_members, bg="#23272A", fg='#0074D9', activebackground="#181A1B", activeforeground="#0074D9", **btn_style).pack(side='left', padx=6)
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief='flat', anchor='w', bg='#181A1B', fg='#0074D9', font=("Segoe UI", 9, "bold"))
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

            try:
                # Get current date for member_since
                current_date = datetime.date.today().strftime('%Y-%m-%d')
                member_data = get_or_create_member(member_id, name, email, phone, current_date)

                messagebox.showinfo("Success", "Member added successfully!")
                dialog.destroy()
                self.load_members()  # Refresh the list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add member: {e}")

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

        # Get current member info from loaded members
        member = None
        for m in self.members:
            if m.get('member_id') == self.current_member_id:
                member = m
                break

        if not member:
            messagebox.showerror("Error", "Member not found")
            return

        member_id = member.get('member_id')
        name = member.get('name', '')
        email = member.get('email', '')
        phone = member.get('phone', '')

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
                # Update member in Supabase
                response = requests.patch(
                    f"{SUPABASE_URL}/rest/v1/members?member_id=eq.{member_id}",
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
                    self.load_members()  # Refresh the list
                    self.on_member_select(None)  # Refresh member info display
                else:
                    print("Error response:", response.status_code, response.text)
                    messagebox.showerror("Error", f"Failed to update member: {response.text}")

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
        member = None
        for m in self.members:
            if m.get('member_id') == self.current_member_id:
                member = m
                break

        if not member:
            messagebox.showerror("Error", "Member not found")
            return

        member_id = member.get('member_id')
        name = member.get('name', '')

        # Confirmation dialog
        result = messagebox.askyesno("Confirm Removal",
                                   f"Are you sure you want to remove this member?\n\n"
                                   f"Member ID: {member_id}\n"
                                   f"Name: {name}\n\n"
                                   f"This action cannot be undone and will also remove all check-in history.")

        if result:
            try:
                # Remove member from Supabase
                response = requests.delete(
                    f"{SUPABASE_URL}/rest/v1/members?member_id=eq.{member_id}",
                    headers=headers
                )

                if response.status_code in (200, 204):
                    messagebox.showinfo("Success", f"Member '{name}' has been removed successfully!")
                    self.current_member_id = None
                    self.current_qr_image = None
                    self.qr_display.config(image='', text="Select a member to generate QR code")
                    self.member_info.config(state='normal')
                    self.member_info.delete(1.0, tk.END)
                    self.member_info.config(state='disabled')
                    self.load_members()  # Refresh the list
                else:
                    print("Error response:", response.status_code, response.text)
                    messagebox.showerror("Error", f"Failed to remove member: {response.text}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove member: {e}")

    def load_members(self):
        try:
            self.members = fetch_all_members()
            print("Fetched members:", self.members)  # Debug print
            # Clear existing items
            for item in self.members_tree.get_children():
                self.members_tree.delete(item)
            # Insert members into the Treeview
            for member in self.members:
                self.members_tree.insert('', 'end', values=(member.get('name', ''), member.get('member_id', ''), member.get('email', '')))

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

        try:
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

        # Find member in loaded members
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
            # Get QR code options
            size = int(self.size_var.get())
            border = int(self.border_var.get())

            # Get member info from loaded members
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

            # Add data (Supabase member_id)
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