import React from 'react'
import './pages.css'

export default function Conversations({ conversations = [] }) {
  return (
    <main className="page conversations-page">
      <h1>Conversations</h1>
      {conversations.length === 0 ? (
        <p>No conversations yet.</p>
      ) : (
        <ul className="conversation-list">
          {conversations.map((c) => (
            <li key={c.id} className="conversation-item">
              {c.title || `Conversation ${c.id}`}
            </li>
          ))}
        </ul>
      )}
    </main>
  )
}
