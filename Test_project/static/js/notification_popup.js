// notification_popup.js

document.addEventListener('DOMContentLoaded', function () {
    const notificationBtn = document.getElementById('notification-btn'); // Nút Notification
    const notificationPopup = document.getElementById('notification-popup-container'); // Popup của Notification
    const notificationCloseBtn = document.getElementById('notification-close-btn'); // Nút đóng trong popup

    // Mở/Đóng popup khi nhấn vào nút Notification
    if (notificationBtn && notificationPopup) {
        notificationBtn.onclick = () => {
            if (notificationPopup.style.display === 'block') {
                notificationPopup.style.display = 'none'; // Đóng popup
            } else {
                notificationPopup.style.display = 'block'; // Mở popup
            }
        };

        // Đóng popup khi nhấn vào nút X (Close)
        if (notificationCloseBtn) {
            notificationCloseBtn.onclick = () => {
                notificationPopup.style.display = 'none';
            };
        }

        // Đóng popup khi nhấn ra ngoài nội dung popup
        window.onclick = (event) => {
            if (event.target == notificationPopup) {
                notificationPopup.style.display = 'none';
            }
        };
    } else {
        console.error('Elements for notification popup not found.');
    }
});
