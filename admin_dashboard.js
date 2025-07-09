document.addEventListener('DOMContentLoaded', function() {
    // Global variables
    let currentDate = new Date().toISOString().split('T')[0];

    const SUPABASE_URL = "https://xbqunvlxqvpmacjcrasc.supabase.co";
    const API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhicXVudmx4cXZwbWFjamNyYXNjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMjQ0MjUsImV4cCI6MjA2NzYwMDQyNX0.DcGWWatFg2faO6g7iBEiyjKb4pxlKwHrya005nZ4Pns";
    const headers = {
      "apikey": API_KEY,
      "Authorization": `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
      "Prefer": "return=representation"
    };

    // Initialize dashboard
    // Check authentication
    if (sessionStorage.getItem('adminSession') !== 'true') {
        window.location.href = 'admin_login.html';
        return;
    }

    // Set admin name
    const adminName = 'Admin';
    document.getElementById('adminName').textContent = adminName;

    // Load data
    loadData();
    
    // Set current date
    document.getElementById('dateSelect').value = currentDate;
    document.getElementById('selectedDate').textContent = formatDate(currentDate);
    
    // Load initial data
    loadCheckinsForDate();
    populateMemberSelect();

    // Load data from localStorage
    function loadData() {
        try {
            // Remove all local checkinHistory and memberDatabase logic
        } catch (error) {
            console.error('Error loading data:', error);
            showStatus('memberStatus', 'Error loading data', 'error');
        }
    }

    // Remove all local checkinHistory and memberDatabase logic
    // --- Supabase-based check-in history ---
    // Fetch check-ins for a given date and join with members
    async function loadCheckinsForDate() {
        const selectedDate = document.getElementById('dateSelect').value;
        document.getElementById('selectedDate').textContent = formatDate(selectedDate);
        const checkinList = document.getElementById('checkinList');
        // Fetch check-ins for the date
        const res = await fetch(`${SUPABASE_URL}/rest/v1/checkins?checkin_date=eq.${selectedDate}&select=*,member:members(*)`, { headers });
        const checkins = await res.json();
        if (!checkins.length) {
            checkinList.innerHTML = '<p style="text-align: center; color: #6c757d; padding: 20px;">No check-ins for selected date</p>';
            return;
        }
        checkinList.innerHTML = '';
        checkins.forEach(checkin => {
            const member = checkin.member;
            const item = document.createElement('div');
            item.className = 'checkin-item';
            const info = document.createElement('div');
            info.className = 'checkin-info';
            const name = document.createElement('div');
            name.className = 'checkin-name';
            name.textContent = member.name;
            const details = document.createElement('div');
            details.className = 'checkin-details';
            details.textContent = member.member_id + ' • ' + member.email;
            info.appendChild(name);
            info.appendChild(details);
            item.appendChild(info);
            // Actions
            const actions = document.createElement('div');
            actions.className = 'checkin-actions';
            const removeBtn = document.createElement('button');
            removeBtn.className = 'btn btn-danger';
            removeBtn.textContent = 'Remove';
            removeBtn.onclick = function() { removeCheckin(member.member_id, selectedDate); };
            actions.appendChild(removeBtn);
            item.appendChild(actions);
            checkinList.appendChild(item);
        });
    }

    // Fetch all members from Supabase
    async function fetchAllMembers() {
        const res = await fetch(`${SUPABASE_URL}/rest/v1/members?select=*`, { headers });
        return await res.json();
    }

    // Populate member select dropdown from Supabase
    async function populateMemberSelect() {
        const memberSelect = document.getElementById('memberSelect');
        memberSelect.innerHTML = '<option value="">Select a member...</option>';
        const members = await fetchAllMembers();
        members.forEach(member => {
            const option = document.createElement('option');
            option.value = member.member_id;
            option.textContent = member.name + ' (' + member.member_id + ')';
            memberSelect.appendChild(option);
        });
    }

    // Manual check-in using Supabase
    window.manualCheckin = async function() {
        const memberId = document.getElementById('memberSelect').value;
        const selectedDate = document.getElementById('dateSelect').value;
        if (!memberId) {
            showStatus('manualCheckinStatus', 'Please select a member', 'error');
            return;
        }
        // Check if already checked in
        const res = await fetch(`${SUPABASE_URL}/rest/v1/checkins?member_id=eq.${memberId}&checkin_date=eq.${selectedDate}`, { headers });
        const checkins = await res.json();
        if (checkins.length) {
            showStatus('manualCheckinStatus', 'Already checked in for ' + formatDate(selectedDate), 'warning');
            return;
        }
        // Insert check-in
        await fetch(`${SUPABASE_URL}/rest/v1/checkins`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ member_id: memberId, checkin_date: selectedDate })
        });
        loadCheckinsForDate();
        showStatus('manualCheckinStatus', 'Checked in successfully for ' + formatDate(selectedDate), 'success');
        document.getElementById('memberSelect').value = '';
    }

    // Remove check-in using Supabase
    async function removeCheckin(memberId, date) {
        if (confirm('Are you sure you want to remove this check-in?')) {
            await fetch(`${SUPABASE_URL}/rest/v1/checkins?member_id=eq.${memberId}&checkin_date=eq.${date}`, {
                method: 'DELETE',
                headers
            });
            loadCheckinsForDate();
            showStatus('manualCheckinStatus', 'Check-in removed successfully', 'success');
        }
    }

    // Generate unique member ID using Supabase
    async function generateMemberId() {
        let memberId;
        let exists = true;
        while (exists) {
            memberId = 'M' + Math.random().toString(36).substr(2, 6).toUpperCase();
            const res = await fetch(`${SUPABASE_URL}/rest/v1/members?member_id=eq.${memberId}`, { headers });
            const data = await res.json();
            exists = data.length > 0;
        }
        return memberId;
    }

    // Generate QR code
    function generateQRCode(memberId) {
        var qrContainer = document.getElementById('qrCode');
        qrContainer.innerHTML = '';
        var canvas = document.createElement('canvas');
        qrContainer.appendChild(canvas);
        QRCode.toCanvas(canvas, memberId, { width: 200, margin: 2 }, function (error) {
            if (error) {
                console.error('Error generating QR code:', error);
            }
        fetch('https://lsmac-log-in.onrender.com/generate_qr', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ member_id: memberId })
        })
        .then(response => response.blob())
        .then(blob => {
            var qrContainer = document.getElementById('qrCode');
            qrContainer.innerHTML = '';
            var img = document.createElement('img');
            img.src = URL.createObjectURL(blob);
            img.alt = 'QR Code';
            img.style.width = '200px';
            img.style.height = '200px';
            qrContainer.appendChild(img);
        })
        .catch(error => {
            console.error('Error generating QR code:', error);
        });
    }

    // Print QR code (fetch member from Supabase)
    window.printQRCode = async function() {
        const memberId = document.getElementById('generatedMemberId').textContent;
        const res = await fetch(`${SUPABASE_URL}/rest/v1/members?member_id=eq.${memberId}`, { headers });
        const data = await res.json();
        const member = data[0];
        if (!member) return;
        const printWindow = window.open('', '_blank');
        printWindow.document.write('<html><head><title>QR Code - ' + member.name + '</title>');
        printWindow.document.write('<style>body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }</style>');
        printWindow.document.write('</head><body>');
        printWindow.document.write('<h1>LSMAC Member QR Code</h1>');
        printWindow.document.write('<h2>' + member.name + '</h2>');
        printWindow.document.write('<p><strong>Member ID:</strong> ' + member.member_id + '</p>');
        printWindow.document.write('<p><strong>Email:</strong> ' + member.email + '</p>');
        printWindow.document.write('<p><strong>Phone:</strong> ' + member.phone + '</p>');
        printWindow.document.write('<p><strong>Member Since:</strong> ' + member.member_since + '</p>');
        printWindow.document.write('<div id="qrCanvas"></div>');
        printWindow.document.write('<script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js"><\/script>');
        printWindow.document.write('<script>QRCode.toCanvas(document.getElementById("qrCanvas"), "' + memberId + '", {width: 300, margin: 2});<\/script>');
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
    }

    // View members modal
    window.openViewMembersModal = function() {
        document.getElementById('viewMembersModal').style.display = 'block';
        loadMembersList();
    }

    window.closeViewMembersModal = function() {
        document.getElementById('viewMembersModal').style.display = 'none';
    }

    // Load members list
    function loadMembersList() {
        const membersList = document.getElementById('membersList');
        membersList.innerHTML = '<p style="text-align: center; color: #6c757d; padding: 20px;">Loading...</p>';
        fetchAllMembers().then(members => {
            if (!members.length) {
                membersList.innerHTML = '<p style="text-align: center; color: #6c757d; padding: 20px;">No members found</p>';
                return;
            }
            membersList.innerHTML = '';
            members.forEach(member => {
                const item = document.createElement('div');
                item.className = 'checkin-item';
                const info = document.createElement('div');
                info.className = 'checkin-info';
                const name = document.createElement('div');
                name.className = 'checkin-name';
                name.textContent = member.name;
                const details = document.createElement('div');
                details.className = 'checkin-details';
                details.textContent = member.member_id + ' • ' + member.email + ' • ' + member.phone;
                info.appendChild(name);
                info.appendChild(details);
                item.appendChild(info);
                // Actions
                const actions = document.createElement('div');
                actions.className = 'checkin-actions';
                // Edit button
                const editBtn = document.createElement('button');
                editBtn.className = 'btn btn-primary';
                editBtn.textContent = 'Edit';
                editBtn.onclick = function() { openEditMemberModal(member); };
                actions.appendChild(editBtn);
                // Delete button
                const deleteBtn = document.createElement('button');
                deleteBtn.className = 'btn btn-danger';
                deleteBtn.textContent = 'Delete';
                deleteBtn.onclick = function() { deleteMember(member); };
                actions.appendChild(deleteBtn);
                item.appendChild(actions);
                membersList.appendChild(item);
            });
        });
    }

    // Open Edit Member Modal
    function openEditMemberModal(member) {
        document.getElementById('editMemberId').value = member.id;
        document.getElementById('editMemberName').value = member.name;
        document.getElementById('editMemberEmail').value = member.email || '';
        document.getElementById('editMemberPhone').value = member.phone || '';
        document.getElementById('editMemberSince').value = member.member_since || '';
        document.getElementById('editMemberModal').style.display = 'block';
    }

    document.getElementById('closeEditMemberModalBtn').onclick = function() {
        document.getElementById('editMemberModal').style.display = 'none';
    };

    document.getElementById('editMemberForm').onsubmit = async function(e) {
        e.preventDefault();
        const id = document.getElementById('editMemberId').value;
        const name = document.getElementById('editMemberName').value;
        const email = document.getElementById('editMemberEmail').value;
        const phone = document.getElementById('editMemberPhone').value;
        const member_since = document.getElementById('editMemberSince').value;
        await fetch(`${SUPABASE_URL}/rest/v1/members?id=eq.${id}`, {
            method: 'PATCH',
            headers,
            body: JSON.stringify({ name, email, phone, member_since })
        });
        document.getElementById('editMemberModal').style.display = 'none';
        loadMembersList();
    };

    // Delete member
    async function deleteMember(member) {
        if (!confirm(`Are you sure you want to delete ${member.name}? This action cannot be undone.`)) return;
        await fetch(`${SUPABASE_URL}/rest/v1/members?id=eq.${member.id}`, {
            method: 'DELETE',
            headers
        });
        loadMembersList();
    }

    // Export data from Supabase as CSV
    window.exportData = async function() {
        try {
            const members = await fetchAllMembers();
            
            // Create CSV header
            const csvHeader = 'Member ID,Name,Email,Phone,Member Since,Classes,Last Check-in\n';
            
            // Create CSV rows
            const csvRows = members.map(member => {
                return `"${member.member_id}","${member.name || ''}","${member.email || ''}","${member.phone || ''}","${member.member_since || ''}","${member.classes || 0}","${member.last_checkin || ''}"`;
            }).join('\n');
            
            // Combine header and rows
            const csvContent = csvHeader + csvRows;
            
            // Create and download CSV file
            const dataBlob = new Blob([csvContent], {type: 'text/csv;charset=utf-8;'});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = 'lsmac_members_export_' + currentDate + '.csv';
            link.click();
            showStatus('memberStatus', 'Data exported successfully as CSV', 'success');
        } catch (error) {
            console.error('Error exporting data:', error);
            showStatus('memberStatus', 'Error exporting data', 'error');
        }
    }

    // Show status message
    function showStatus(elementId, message, type) {
        const statusElement = document.getElementById(elementId);
        statusElement.textContent = message;
        statusElement.className = 'status ' + type;
        statusElement.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            statusElement.style.display = 'none';
        }, 5000);
    }

    // Format date
    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            weekday: 'long', 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
    }

    // Logout
    window.logout = function() {
        sessionStorage.removeItem('adminSession');
        window.location.href = 'admin_login.html';
    }

    // Close modals when clicking outside
    window.onclick = function(event) {
        const viewModal = document.getElementById('viewMembersModal');
        
        if (event.target === viewModal) {
            viewModal.style.display = 'none';
        }
    };

    // Attach button event listeners at the end to ensure all functions are defined
    var viewBtn = document.getElementById('viewAllMembersBtn');
    if (viewBtn) {
        viewBtn.addEventListener('click', function() {
            document.getElementById('viewMembersModal').style.display = 'block';
            loadMembersList();
        });
    }
    var exportBtn = document.getElementById('exportDataBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', exportData);
    }
    var closeBtn = document.getElementById('closeViewMembersModalBtn');
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            document.getElementById('viewMembersModal').style.display = 'none';
        });
    }
}); 