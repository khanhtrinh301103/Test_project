// popup.js

// JavaScript to handle the popup
document.addEventListener('DOMContentLoaded', function () {
    const settingBtn = document.getElementById('setting-btn');
    const settingsPopup = document.getElementById('settings-popup');
    const saveBtn = document.getElementById('save-btn');
    const closeBtn = document.getElementById('close-btn'); // Nút đóng popup

    if (settingBtn && settingsPopup) {
        // Mở/Đóng popup khi nhấn vào nút Setting
        settingBtn.onclick = () => {
            if (settingsPopup.style.display === 'block') {
                settingsPopup.style.display = 'none'; // Đóng popup
            } else {
                settingsPopup.style.display = 'block'; // Mở popup
            }
        };

        // Đóng popup khi nhấn vào nút Save
        if (saveBtn) {
            saveBtn.onclick = () => {
                settingsPopup.style.display = 'none';
            };
        }

        // Đóng popup khi nhấn vào dấu X
        if (closeBtn) {
            closeBtn.onclick = () => {
                settingsPopup.style.display = 'none';
            };
        }

        // Đóng popup khi nhấn ra ngoài nội dung popup
        window.onclick = (event) => {
            if (event.target == settingsPopup) {
                settingsPopup.style.display = 'none';
            }
        };
    } else {
        console.error('Elements for popup not found.');
    }
});
