document.addEventListener('DOMContentLoaded', function () {
    const chatbotBtn = document.getElementById('chatbot-open-btn'); // Nút mở bot chat
    const chatbotPopup = document.getElementById('chatbot-popup-container'); // Popup của bot chat
    const chatbotCloseBtn = document.getElementById('chatbot-close-btn'); // Nút đóng bot chat
    const chatbotForm = document.getElementById('chatbot-form'); // Form để gửi câu hỏi
    const chatbotInput = document.getElementById('chatbot-input'); // Input nơi người dùng nhập câu hỏi
    const chatbotMessages = document.getElementById('chatbot-messages'); // Khu vực hiển thị tin nhắn

    let isFirstOpen = true; // Cờ để kiểm tra xem popup đã mở lần đầu chưa

    // Mở/đóng popup khi nhấn vào nút chat bot
    if (chatbotBtn && chatbotPopup) {
        chatbotBtn.onclick = () => {
            if (chatbotPopup.style.display === 'block') {
                chatbotPopup.style.display = 'none'; // Đóng popup
            } else {
                chatbotPopup.style.display = 'block'; // Mở popup

                // Hiển thị tin nhắn chào mừng khi chat bot mở lần đầu tiên
                if (isFirstOpen) {
                    chatbotMessages.innerHTML += `<div class="bot-message">hello, weather gpt free to ask!</div>`;
                    chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Cuộn xuống cuối khung tin nhắn
                    isFirstOpen = false; // Đặt cờ thành false để không hiển thị câu chào lần sau
                }
            }
        };
    }

    // Đóng popup khi nhấn vào nút X
    if (chatbotCloseBtn) {
        chatbotCloseBtn.onclick = () => {
            chatbotPopup.style.display = 'none';
        };
    }

    // Xử lý sự kiện khi người dùng gửi câu hỏi
    if (chatbotForm) {
        chatbotForm.addEventListener('submit', function (e) {
            e.preventDefault(); // Ngăn việc reload trang khi form được submit

            const userInput = chatbotInput.value; // Lấy câu hỏi từ input của người dùng

            // Hiển thị tin nhắn của người dùng trên giao diện với hiệu ứng
            const userMessage = document.createElement('div');
            userMessage.classList.add('user-message');
            userMessage.classList.add('message-slide-in-right'); // Thêm lớp để có hiệu ứng
            userMessage.innerHTML = userInput;
            chatbotMessages.appendChild(userMessage);

            // Hiển thị hiệu ứng typing của chatbot
            const typingIndicator = document.createElement('div');
            typingIndicator.classList.add('typing-indicator');
            typingIndicator.innerText = 'Bot is typing...';
            chatbotMessages.appendChild(typingIndicator);

            chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Tự động cuộn xuống cuối cuộc trò chuyện

            // Gửi câu hỏi của người dùng đến backend
            fetch('/chatbot', { // Đảm bảo route Flask là '/chatbot'
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userInput }) // Gửi câu hỏi dưới dạng JSON
            })
            .then(response => response.json()) // Nhận phản hồi từ backend
            .then(data => {
                // Xóa typing indicator khi nhận phản hồi từ bot
                typingIndicator.remove();

                // Hiển thị phản hồi từ bot với hiệu ứng
                const botMessage = document.createElement('div');
                botMessage.classList.add('bot-message');
                botMessage.classList.add('message-slide-in-left'); // Thêm lớp để có hiệu ứng
                botMessage.innerHTML = data.response;
                chatbotMessages.appendChild(botMessage);

                chatbotInput.value = ''; // Xóa nội dung trong input sau khi gửi
                chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Tự động cuộn xuống cuối cuộc trò chuyện
            })
            .catch(error => {
                console.error('Error:', error);
                typingIndicator.remove();
            });
        });
    }
});
