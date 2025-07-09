document.addEventListener('DOMContentLoaded', function() {
    // Global variables
    let memberDatabase = {};
    let checkinHistory = {};
    let currentDate = new Date().toISOString().split('T')[0];

    // Initialize dashboard
    // Check authentication
    if (sessionStorage.getItem('adminLoggedIn') !== 'true') {
        window.location.href = 'admin_login.html';
        return;
    }

    // Set admin name
    const adminName = sessionStorage.getItem('adminUsername') || 'Admin';
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
            const savedMembers = localStorage.getItem('lsmac_members');
            const savedHistory = localStorage.getItem('lsmac_history');
            
            if (savedMembers) {
                memberDatabase = JSON.parse(savedMembers);
            }

            if (savedHistory) {
                checkinHistory = JSON.parse(savedHistory);
            }
        } catch (error) {
            console.error('Error loading data:', error);
            showStatus('memberStatus', 'Error loading data', 'error');
        }
    }

    // Save data to localStorage
    function saveData() {
        try {
            localStorage.setItem('lsmac_members', JSON.stringify(memberDatabase));
            localStorage.setItem('lsmac_history', JSON.stringify(checkinHistory));
        } catch (error) {
            console.error('Error saving data:', error);
            showStatus('memberStatus', 'Error saving data', 'error');
        }
    }

    // Load check-ins for selected date
    function loadCheckinsForDate() {
        const selectedDate = document.getElementById('dateSelect').value;
        document.getElementById('selectedDate').textContent = formatDate(selectedDate);
        
        const checkinList = document.getElementById('checkinList');
        const checkinsForDate = [];

        // Get all members who checked in on the selected date
        for (const memberId in checkinHistory) {
            if (checkinHistory[memberId].includes(selectedDate)) {
                const member = memberDatabase[memberId];
                if (member) {
                    checkinsForDate.push({
                        member: member,
                        checkinDate: selectedDate
                    });
                }
            }
        }

        if (checkinsForDate.length === 0) {
            checkinList.innerHTML = '<p style="text-align: center; color: #6c757d; padding: 20px;">No check-ins for selected date</p>';
            return;
        }

        // Clear the list
        checkinList.innerHTML = '';
        
        // Add each check-in item
        for (let i = 0; i < checkinsForDate.length; i++) {
            const checkin = checkinsForDate[i];
            const item = document.createElement('div');
            item.className = 'checkin-item';
            
            const info = document.createElement('div');
            info.className = 'checkin-info';
            
            const name = document.createElement('div');
            name.className = 'checkin-name';
            name.textContent = checkin.member.name;
            
            const details = document.createElement('div');
            details.className = 'checkin-details';
            details.textContent = checkin.member.id + ' • ' + checkin.member.email;
            
            info.appendChild(name);
            info.appendChild(details);
            
            const actions = document.createElement('div');
            actions.className = 'checkin-actions';
            
            const viewBtn = document.createElement('button');
            viewBtn.className = 'btn btn-warning';
            viewBtn.textContent = 'View QR';
            viewBtn.onclick = function() { viewMemberQR(checkin.member.id); };
            
            const removeBtn = document.createElement('button');
            removeBtn.className = 'btn btn-danger';
            removeBtn.textContent = 'Remove';
            removeBtn.onclick = function() { removeCheckin(checkin.member.id, selectedDate); };
            
            actions.appendChild(viewBtn);
            actions.appendChild(removeBtn);
            
            item.appendChild(info);
            item.appendChild(actions);
            
            checkinList.appendChild(item);
        }
    }

    // Populate member select dropdown
    function populateMemberSelect() {
        const memberSelect = document.getElementById('memberSelect');
        memberSelect.innerHTML = '<option value="">Select a member...</option>';
        
        for (const memberId in memberDatabase) {
            const member = memberDatabase[memberId];
            const option = document.createElement('option');
            option.value = memberId;
            option.textContent = member.name + ' (' + member.id + ')';
            memberSelect.appendChild(option);
        }
    }

    // Manual check-in
    window.manualCheckin = function() {
        const memberId = document.getElementById('memberSelect').value;
        const selectedDate = document.getElementById('dateSelect').value;
        
        if (!memberId) {
            showStatus('manualCheckinStatus', 'Please select a member', 'error');
            return;
        }

        const member = memberDatabase[memberId];
        if (!member) {
            showStatus('manualCheckinStatus', 'Member not found', 'error');
            return;
        }

        // Check if already checked in
        if (checkinHistory[memberId] && checkinHistory[memberId].includes(selectedDate)) {
            showStatus('manualCheckinStatus', member.name + ' has already checked in on ' + formatDate(selectedDate), 'warning');
            return;
        }

        // Record check-in
        if (!checkinHistory[memberId]) {
            checkinHistory[memberId] = [];
        }
        checkinHistory[memberId].push(selectedDate);

        // Save data
        saveData();

        // Update display
        loadCheckinsForDate();
        showStatus('manualCheckinStatus', member.name + ' checked in successfully for ' + formatDate(selectedDate), 'success');

        // Clear selection
        document.getElementById('memberSelect').value = '';
    }

    // Remove check-in
    function removeCheckin(memberId, date) {
        if (confirm('Are you sure you want to remove this check-in?')) {
            if (checkinHistory[memberId]) {
                checkinHistory[memberId] = checkinHistory[memberId].filter(d => d !== date);
                if (checkinHistory[memberId].length === 0) {
                    delete checkinHistory[memberId];
                }
            }
            
            saveData();
            loadCheckinsForDate();
            showStatus('manualCheckinStatus', 'Check-in removed successfully', 'success');
        }
    }

    // Add new member
    window.openAddMemberModal = function() {
        document.getElementById('addMemberModal').style.display = 'block';
        document.getElementById('addMemberForm').reset();
        document.getElementById('qrContainer').style.display = 'none';
    }

    window.closeAddMemberModal = function() {
        document.getElementById('addMemberModal').style.display = 'none';
    }

    // Handle add member form submission
    document.getElementById('addMemberForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const name = document.getElementById('memberName').value;
        const email = document.getElementById('memberEmail').value;
        const phone = document.getElementById('memberPhone').value;
        const memberSince = document.getElementById('memberSince').value;

        // Generate unique member ID
        const memberId = generateMemberId();
        
        // Add member to database
        memberDatabase[memberId] = {
            id: memberId,
            name: name,
            email: email,
            phone: phone,
            memberSince: memberSince
        };

        // Save data
        saveData();

        // Generate QR code
        generateQRCode(memberId);
        
        // Show QR code
        document.getElementById('generatedMemberId').textContent = memberId;
        document.getElementById('qrContainer').style.display = 'block';
        
        // Update member select
        populateMemberSelect();
        
        showStatus('memberStatus', 'Member ' + name + ' added successfully with ID: ' + memberId, 'success');
    });

    // Generate unique member ID
    function generateMemberId() {
        let memberId;
        do {
            memberId = 'M' + Math.random().toString(36).substr(2, 6).toUpperCase();
        } while (memberDatabase[memberId]);
        return memberId;
    }

    // Generate QR code
    function generateQRCode(memberId) {
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

    // Print QR code
    window.printQRCode = function() {
        const memberId = document.getElementById('generatedMemberId').textContent;
        const member = memberDatabase[memberId];
        
        const printWindow = window.open('', '_blank');
        printWindow.document.write('<html><head><title>QR Code - ' + member.name + '</title>');
        printWindow.document.write('<style>body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }</style>');
        printWindow.document.write('</head><body>');
        printWindow.document.write('<h1>LSMAC Member QR Code</h1>');
        printWindow.document.write('<h2>' + member.name + '</h2>');
        printWindow.document.write('<p><strong>Member ID:</strong> ' + member.id + '</p>');
        printWindow.document.write('<p><strong>Email:</strong> ' + member.email + '</p>');
        printWindow.document.write('<p><strong>Phone:</strong> ' + member.phone + '</p>');
        printWindow.document.write('<p><strong>Member Since:</strong> ' + member.memberSince + '</p>');
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
        
        if (Object.keys(memberDatabase).length === 0) {
            membersList.innerHTML = '<p style="text-align: center; color: #6c757d; padding: 20px;">No members found</p>';
            return;
        }

        // Clear the list
        membersList.innerHTML = '';
        
        // Add each member
        const members = Object.values(memberDatabase);
        for (let i = 0; i < members.length; i++) {
            const member = members[i];
            const item = document.createElement('div');
            item.className = 'checkin-item';
            
            const info = document.createElement('div');
            info.className = 'checkin-info';
            
            const name = document.createElement('div');
            name.className = 'checkin-name';
            name.textContent = member.name;
            
            const details = document.createElement('div');
            details.className = 'checkin-details';
            details.textContent = member.id + ' • ' + member.email + ' • ' + member.phone;
            
            info.appendChild(name);
            info.appendChild(details);
            
            const actions = document.createElement('div');
            actions.className = 'checkin-actions';
            
            const viewBtn = document.createElement('button');
            viewBtn.className = 'btn btn-warning';
            viewBtn.textContent = 'View QR';
            viewBtn.onclick = function() { viewMemberQR(member.id); };
            
            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'btn btn-danger';
            deleteBtn.textContent = 'Delete';
            deleteBtn.onclick = function() { deleteMember(member.id); };
            
            actions.appendChild(viewBtn);
            actions.appendChild(deleteBtn);
            
            item.appendChild(info);
            item.appendChild(actions);
            
            membersList.appendChild(item);
        }
    }

    // View member QR code
    window.viewMemberQR = function(memberId) {
        const member = memberDatabase[memberId];
        if (!member) return;

        const printWindow = window.open('', '_blank');
        printWindow.document.write('<html><head><title>QR Code - ' + member.name + '</title>');
        printWindow.document.write('<style>body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }</style>');
        printWindow.document.write('</head><body>');
        printWindow.document.write('<h1>LSMAC Member QR Code</h1>');
        printWindow.document.write('<h2>' + member.name + '</h2>');
        printWindow.document.write('<p><strong>Member ID:</strong> ' + member.id + '</p>');
        printWindow.document.write('<p><strong>Email:</strong> ' + member.email + '</p>');
        printWindow.document.write('<p><strong>Phone:</strong> ' + member.phone + '</p>');
        printWindow.document.write('<p><strong>Member Since:</strong> ' + member.memberSince + '</p>');
        printWindow.document.write('<div id="qrCanvas"></div>');
        printWindow.document.write('<script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.3/build/qrcode.min.js"><\/script>');
        printWindow.document.write('<script>QRCode.toCanvas(document.getElementById("qrCanvas"), "' + memberId + '", {width: 300, margin: 2});<\/script>');
        printWindow.document.write('</body></html>');
        printWindow.document.close();
    }

    // Delete member
    function deleteMember(memberId) {
        const member = memberDatabase[memberId];
        if (!member) return;

        if (confirm('Are you sure you want to delete ' + member.name + '? This action cannot be undone.')) {
            delete memberDatabase[memberId];
            delete checkinHistory[memberId];
            
            saveData();
            loadMembersList();
            populateMemberSelect();
            loadCheckinsForDate();
            
            showStatus('memberStatus', 'Member ' + member.name + ' deleted successfully', 'success');
        }
    }

    // Export data
    window.exportData = function() {
        try {
            const exportData = {
                members: memberDatabase,
                history: checkinHistory,
                exportDate: new Date().toISOString()
            };
            
            const dataStr = JSON.stringify(exportData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = 'lsmac_admin_export_' + currentDate + '.json';
            link.click();
            
            showStatus('memberStatus', 'Data exported successfully', 'success');
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
        sessionStorage.removeItem('adminLoggedIn');
        sessionStorage.removeItem('adminUsername');
        window.location.href = 'index.html';
    }

    // Close modals when clicking outside
    window.onclick = function(event) {
        const addModal = document.getElementById('addMemberModal');
        const viewModal = document.getElementById('viewMembersModal');
        
        if (event.target === addModal) {
            closeAddMemberModal();
        }
        if (event.target === viewModal) {
            closeViewMembersModal();
        }
    };
}); 
