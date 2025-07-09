#!/usr/bin/env python3
"""
LSMAC System Launcher
Choose between Member Check-In System and QR Code Generator
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

class SystemLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("LSMAC System Launcher")
        self.root.geometry("500x400")
        self.root.configure(bg='#2c3e50')
        
        # Center the window
        self.center_window()
        
        self.setup_gui()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_gui(self):
        """Setup the launcher GUI"""
        # Main title
        title_label = tk.Label(self.root, text="LSMAC Management System", 
                              font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=30)
        
        # Subtitle
        subtitle_label = tk.Label(self.root, text="Choose an application to launch", 
                                 font=('Arial', 14), fg='#ecf0f1', bg='#2c3e50')
        subtitle_label.pack(pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=40)
        
        # Check-in System button
        checkin_btn = tk.Button(button_frame, text="Member Check-In System", 
                              command=self.launch_checkin, 
                              bg='#27ae60', fg='white', font=('Arial', 16, 'bold'),
                              width=25, height=2, relief='raised', bd=3)
        checkin_btn.pack(pady=15)
        
        # QR Generator button
        qr_btn = tk.Button(button_frame, text="QR Code Generator", 
                          command=self.launch_qr_generator,
                          bg='#3498db', fg='white', font=('Arial', 16, 'bold'),
                          width=25, height=2, relief='raised', bd=3)
        qr_btn.pack(pady=15)
        
        # Test System button
        test_btn = tk.Button(button_frame, text="Test System", 
                           command=self.test_system,
                           bg='#f39c12', fg='white', font=('Arial', 12, 'bold'),
                           width=20, height=1, relief='raised', bd=2)
        test_btn.pack(pady=10)
        
        # Exit button
        exit_btn = tk.Button(self.root, text="Exit", 
                           command=self.root.quit,
                           bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                           width=15, height=1, relief='raised', bd=2)
        exit_btn.pack(pady=20)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Ready", 
                                   font=('Arial', 10), fg='#bdc3c7', bg='#2c3e50')
        self.status_label.pack(side='bottom', pady=10)
        
    def launch_checkin(self):
        """Launch the Member Check-In System"""
        try:
            self.status_label.config(text="Launching Check-In System...")
            self.root.update()
            
            # Check if main.py exists
            if not os.path.exists("main.py"):
                messagebox.showerror("Error", "Check-in system not found. Please ensure main.py exists.")
                return
            
            # Launch the check-in system
            subprocess.Popen([sys.executable, "main.py"])
            self.status_label.config(text="Check-In System launched successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Check-In System: {e}")
            self.status_label.config(text="Error launching Check-In System")
    
    def launch_qr_generator(self):
        """Launch the QR Code Generator"""
        try:
            self.status_label.config(text="Launching QR Code Generator...")
            self.root.update()
            
            # Check if qr_generator.py exists
            if not os.path.exists("qr_generator.py"):
                messagebox.showerror("Error", "QR Generator not found. Please ensure qr_generator.py exists.")
                return
            
            # Launch the QR generator
            subprocess.Popen([sys.executable, "qr_generator.py"])
            self.status_label.config(text="QR Code Generator launched successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch QR Code Generator: {e}")
            self.status_label.config(text="Error launching QR Code Generator")
    
    def test_system(self):
        """Run system tests"""
        try:
            self.status_label.config(text="Running system tests...")
            self.root.update()
            
            # Check if test_system.py exists
            if not os.path.exists("test_system.py"):
                messagebox.showerror("Error", "Test script not found. Please ensure test_system.py exists.")
                return
            
            # Run the test script
            result = subprocess.run([sys.executable, "test_system.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                messagebox.showinfo("Test Results", "System tests completed successfully!\n\nCheck the terminal for detailed results.")
                self.status_label.config(text="System tests completed successfully")
            else:
                messagebox.showwarning("Test Results", "Some tests failed.\n\nCheck the terminal for detailed results.")
                self.status_label.config(text="Some tests failed")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run system tests: {e}")
            self.status_label.config(text="Error running tests")

def main():
    root = tk.Tk()
    app = SystemLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main() 