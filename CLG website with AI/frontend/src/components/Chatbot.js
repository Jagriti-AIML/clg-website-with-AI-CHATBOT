import React, { useState, useEffect, useRef } from 'react';
// import './Chatbot.css'; // Don't forget to create a CSS file for styling

function Chatbot() {
    const [messages, setMessages] = useState([
        { sender: 'AI', text: "Hello! I'm your AI College Assistant. Ask me about admissions, courses, or fees!" }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSend = async (e) => {
        e.preventDefault();
        const userQuery = input.trim();
        if (userQuery === '' || isLoading) return;

        // 1. Display User Message Immediately
        const newUserMessage = { sender: 'User', text: userQuery };
        setMessages((prev) => [...prev, newUserMessage]);
        setInput('');
        setIsLoading(true);

        try {
            // 2. Call the Django API
            const response = await fetch('http://127.0.0.1:8000/api/chat/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userQuery })
            });

            if (!response.ok) {
                throw new Error('Chatbot API network response was not ok.');
            }

            const data = await response.json();
            
            // 3. Display AI Response
            const newAIMessage = { sender: 'AI', text: data.response };
            setMessages((prev) => [...prev, newAIMessage]);

        } catch (error) {
            console.error('Chatbot API Error:', error);
            const errorMessage = { sender: 'AI', text: "I'm sorry, I'm experiencing technical difficulties. Please check your network or try again." };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chatbot-container">
            <h3>🎓 AI Assistant</h3>
            <div className="chat-window">
                {messages.map((msg, index) => (
                    <div key={index} className={`message-bubble ${msg.sender.toLowerCase()}`}>
                        <strong>{msg.sender}:</strong> {msg.text}
                    </div>
                ))}
                {isLoading && (
                    <div className="message-bubble ai loading">
                        <strong>AI:</strong> Typing...
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>
            <form className="chat-input-form" onSubmit={handleSend}>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a question about the college..."
                    disabled={isLoading}
                />
                <button type="submit" disabled={isLoading}>
                    {isLoading ? 'Sending...' : 'Send'}
                </button>
            </form>
        </div>
    );
}

export default Chatbot;