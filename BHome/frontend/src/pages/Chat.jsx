import React from 'react'
import './pages.css'

export default function Chat({ conversation = {}, messages = [] }) {
  return (
    <main className="page chat-page">
      <header className="chat-header">
        <h2>{conversation.title || `Conversation ${conversation.id || ''}`}</h2>
      </header>
      <section className="chat-messages">
        {messages.length === 0 ? (
          <p className="muted">No messages</p>
        ) : (
          messages.map((m) => (
            <div key={m.id} className="message-item">
              <strong>{m.sender?.username || 'User'}:</strong> {m.content}
            </div>
          ))
        )}
      </section>
      <footer className="chat-input">
        <input placeholder="Type a message (presentation only)" />
        <button>Send</button>
      </footer>
    </main>
  )
}
