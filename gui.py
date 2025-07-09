import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
import threading
import datetime
from database import CheckInDatabase
from barcode_scanner import BarcodeScanner

class CheckInGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LSMAC Member Check-In System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database and scanner
        self.db = CheckInDatabase()
        self.scanner = BarcodeScanner()
        
        # GUI variables
        self.current_member = None
        self.is_scanning = False
        self.camera_frame = None
        
        self.setup_gui()
        self.update_date_display()
        
    def setup_gui(self):
        """Setup the main GUI layout"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=10, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="LSMAC Member Check-In System", 
                              font=('Arial', 20, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Date display
        self.date_label = tk.Label(self.root, text="", font=('Arial', 14), bg='#f0f0f0')
        self.date_label.pack(pady=5)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left panel - Camera and scanning
        left_panel = tk.Frame(main_frame, bg='#f0f0f0', width=600)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Camera frame
        self.camera_container = tk.Frame(left_panel, bg='black', height=400)
        self.camera_container.pack(fill='x', pady=5)
        self.camera_container.pack_propagate(False)
        
        self.camera_label = tk.Label(self.camera_container, text="Camera not started", 
                                   bg='black', fg='white', font=('Arial', 12))
        self.camera_label.pack(expand=True)
        
        # Camera controls
        camera_controls = tk.Frame(left_panel, bg='#f0f0f0')
        camera_controls.pack(fill='x', pady=5)
        
        self.start_camera_btn = tk.Button(camera_controls, text="Start Camera", 
                                        command=self.start_camera, bg='#27ae60', fg='white',
                                        font=('Arial', 10, 'bold'), padx=20, pady=5)
        self.start_camera_btn.pack(side='left', padx=5)
        
        self.scan_btn = tk.Button(camera_controls, text="Start Scanning", 
                                command=self.toggle_scanning, bg='#3498db', fg='white',
                                font=('Arial', 10, 'bold'), padx=20, pady=5, state='disabled')
        self.scan_btn.pack(side='left', padx=5)
        
        # Member info display
        member_frame = tk.LabelFrame(left_panel, text="Member Information", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0')
        member_frame.pack(fill='x', pady=10)
        
        self.member_info = tk.Text(member_frame, height=8, font=('Arial', 10), 
                                 state='disabled', bg='white')
        self.member_info.pack(fill='x', padx=10, pady=10)
        
        # Check-in button
        self.checkin_btn = tk.Button(left_panel, text="Check In Member", 
                                   command=self.check_in_member, bg='#e74c3c', fg='white',
                                   font=('Arial', 12, 'bold'), padx=30, pady=10, state='disabled')
        self.checkin_btn.pack(pady=10)
        
        # Right panel - Today's check-ins
        right_panel = tk.Frame(main_frame, bg='#f0f0f0', width=400)
        right_panel.pack(side='right', fill='both', padx=(5, 0))
        
        # Today's check-ins
        checkins_frame = tk.LabelFrame(right_panel, text="Today's Check-Ins", 
                                     font=('Arial', 12, 'bold'), bg='#f0f0f0')
        checkins_frame.pack(fill='both', expand=True)
        
        # Treeview for check-ins
        columns = ('Name', 'Member ID', 'Time')
        self.checkins_tree = ttk.Treeview(checkins_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.checkins_tree.heading(col, text=col)
            self.checkins_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(checkins_frame, orient='vertical', command=self.checkins_tree.yview)
        self.checkins_tree.configure(yscrollcommand=scrollbar.set)
        
        self.checkins_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Admin buttons
        admin_frame = tk.Frame(right_panel, bg='#f0f0f0')
        admin_frame.pack(fill='x', pady=10)
        
        tk.Button(admin_frame, text="Add Member", command=self.add_member_dialog,
                bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'), padx=15, pady=5).pack(fill='x', pady=2)
        
        tk.Button(admin_frame, text="View History", command=self.view_history_dialog,
                bg='#f39c12', fg='white', font=('Arial', 10, 'bold'), padx=15, pady=5).pack(fill='x', pady=2)
        
        tk.Button(admin_frame, text="Refresh List", command=self.refresh_checkins,
                bg='#34495e', fg='white', font=('Arial', 10, 'bold'), padx=15, pady=5).pack(fill='x', pady=2)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                            relief='sunken', anchor='w', bg='#ecf0f1')
        status_bar.pack(side='bottom', fill='x')
        
    def update_date_display(self):
        """Update the date display"""
        current_date = datetime.date.today().strftime("%A, %B %d, %Y")
        self.date_label.config(text=f"Date: {current_date}")
        self.root.after(60000, self.update_date_display)  # Update every minute
        
    def start_camera(self):
        """Start the camera"""
        if self.scanner.start_camera():
            self.camera_label.config(text="Camera started successfully")
            self.scan_btn.config(state='normal')
            self.start_camera_btn.config(state='disabled')
            self.status_var.set("Camera started")
            self.update_camera_feed()
        else:
            messagebox.showerror("Error", "Failed to start camera. Please check if camera is connected.")
            
    def update_camera_feed(self):
        """Update the camera feed display"""
        if self.scanner.camera and self.scanner.camera.isOpened():
            frame = self.scanner.get_frame()
            if frame is not None:
                # Convert frame to PIL Image
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame_rgb)
                
                # Resize to fit the container
                container_width = self.camera_container.winfo_width()
                container_height = self.camera_container.winfo_height()
                
                if container_width > 1 and container_height > 1:
                    pil_image = pil_image.resize((container_width, container_height), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(pil_image)
                    
                    self.camera_label.config(image=photo, text="")
                    self.camera_label.image = photo  # Keep a reference
                
        self.root.after(50, self.update_camera_feed)  # Update every 50ms
        
    def toggle_scanning(self):
        """Toggle barcode scanning on/off"""
        if not self.is_scanning:
            self.scanner.start_continuous_scanning(self.on_barcode_scanned)
            self.scan_btn.config(text="Stop Scanning", bg='#e74c3c')
            self.is_scanning = True
            self.status_var.set("Scanning for barcodes...")
        else:
            self.scanner.stop_continuous_scanning()
            self.scan_btn.config(text="Start Scanning", bg='#3498db')
            self.is_scanning = False
            self.status_var.set("Scanning stopped")
            
    def on_barcode_scanned(self, barcode_data):
        """Callback when a barcode is scanned"""
        self.root.after(0, lambda: self.process_barcode(barcode_data))
        
    def process_barcode(self, barcode_data):
        """Process the scanned barcode"""
        self.status_var.set(f"Scanned: {barcode_data}")
        
        # Get member information
        member = self.db.get_member(barcode_data)
        if member:
            self.current_member = member
            self.display_member_info(member)
            self.checkin_btn.config(state='normal')
        else:
            self.current_member = None
            self.member_info.config(state='normal')
            self.member_info.delete(1.0, tk.END)
            self.member_info.insert(1.0, f"Member ID: {barcode_data}\n\nMember not found in database.\nPlease add this member first.")
            self.member_info.config(state='disabled')
            self.checkin_btn.config(state='disabled')
            
    def display_member_info(self, member):
        """Display member information in the text area"""
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
        
        # Check if already checked in today
        if self.db.has_checked_in_today(member_id):
            info_text += "⚠️ Already checked in today!"
        else:
            info_text += "✅ Ready to check in"
            
        self.member_info.insert(1.0, info_text)
        self.member_info.config(state='disabled')
        
    def check_in_member(self):
        """Check in the current member"""
        if not self.current_member:
            messagebox.showwarning("Warning", "No member selected for check-in")
            return
            
        member_id = self.current_member[0]
        
        if self.db.has_checked_in_today(member_id):
            messagebox.showinfo("Info", f"{self.current_member[1]} has already checked in today!")
            return
            
        if self.db.record_check_in(member_id):
            messagebox.showinfo("Success", f"{self.current_member[1]} checked in successfully!")
            self.refresh_checkins()
            self.process_barcode(member_id)  # Refresh member info
            self.status_var.set(f"Check-in recorded for {self.current_member[1]}")
        else:
            messagebox.showerror("Error", "Failed to record check-in")
            
    def add_member_dialog(self):
        """Dialog to add a new member"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Member")
        dialog.geometry("400x300")
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
            else:
                messagebox.showerror("Error", "Member ID already exists")
                
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Save", command=save_member, 
                bg='#27ae60', fg='white', padx=20).pack(side='left', padx=5)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy,
                bg='#95a5a6', fg='white', padx=20).pack(side='left', padx=5)
        
    def view_history_dialog(self):
        """Dialog to view member check-in history"""
        member_id = simpledialog.askstring("View History", "Enter Member ID:")
        if not member_id:
            return
            
        history = self.db.get_member_check_in_history(member_id)
        if not history:
            messagebox.showinfo("History", "No check-in history found for this member")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Check-in History - {member_id}")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        
        # History list
        columns = ('Date', 'Time')
        history_tree = ttk.Treeview(dialog, columns=columns, show='headings', height=15)
        
        for col in columns:
            history_tree.heading(col, text=col)
            history_tree.column(col, width=200)
            
        for date, time in history:
            history_tree.insert('', 'end', values=(date, time))
            
        history_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
    def refresh_checkins(self):
        """Refresh the today's check-ins list"""
        # Clear existing items
        for item in self.checkins_tree.get_children():
            self.checkins_tree.delete(item)
            
        # Get today's check-ins
        today = datetime.date.today().isoformat()
        checkins = self.db.get_check_ins_for_date(today)
        
        for name, member_id, time in checkins:
            self.checkins_tree.insert('', 'end', values=(name, member_id, time))
            
        self.status_var.set(f"Refreshed check-ins list - {len(checkins)} check-ins today")
        
    def on_closing(self):
        """Handle application closing"""
        if self.is_scanning:
            self.scanner.stop_continuous_scanning()
        self.scanner.stop_camera()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = CheckInGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 