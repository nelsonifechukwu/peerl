import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import API_BASE_URL from '../utils/api'

function Chat({ sessionKey, participantName, condition, challengeQuestion, timeRemaining }) {
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState('')
  const [sending, setSending] = useState(false)
  const [currentAnchor, setCurrentAnchor] = useState(null)
  const [isParticipantAnchor, setIsParticipantAnchor] = useState(false)
  const [coaching, setCoaching] = useState(null)
  
  const chatEndRef = useRef(null)
  const pollInterval = useRef(null)

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Poll for new messages
  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/sessions/${sessionKey}/messages`)
        console.log(`Fetched ${response.data.length} messages`)  // Add this
        setMessages(response.data)
      } catch (error) {
        console.error('Error fetching messages:', error)
      }
    }

    // Initial fetch
    fetchMessages()

    // Poll every 2 seconds
    pollInterval.current = setInterval(fetchMessages, 2000)

    return () => {
      if (pollInterval.current) {
        clearInterval(pollInterval.current)
      }
    }
  }, [sessionKey])

  // Handle rotating anchor
  useEffect(() => {
    if (condition !== 'rotating_anchor') return

    // Check if it's time to rotate (every 3 minutes = 180 seconds)
    const discussionTime = 540 // 9 minutes total
    const elapsed = discussionTime - timeRemaining
    const rotationNumber = Math.floor(elapsed / 180)

    // Rotate if needed
    if (rotationNumber > 0 && rotationNumber <= 2) {
      rotateAnchor()
    }
  }, [timeRemaining, condition])

  const rotateAnchor = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/sessions/${sessionKey}/rotate-anchor`)
      
      if (response.data.anchor_rotation_complete) {
        return
      }

      setCurrentAnchor(response.data.current_anchor)
      setIsParticipantAnchor(response.data.is_participant_anchor)

      // If participant is now anchor, fetch coaching
      if (response.data.is_participant_anchor) {
        fetchCoaching()
      }
    } catch (error) {
      console.error('Error rotating anchor:', error)
    }
  }

  const fetchCoaching = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/sessions/${sessionKey}/coaching`)
      setCoaching(response.data.coaching)
    } catch (error) {
      console.error('Error fetching coaching:', error)
    }
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    
    if (!newMessage.trim() || sending) return

    setSending(true)

    try {
      await axios.post(`${API_BASE_URL}/sessions/${sessionKey}/messages`, {
        content: newMessage.trim()
      })
      
      setNewMessage('')
      
      // If participant is anchor, get new coaching
      if (isParticipantAnchor) {
        setTimeout(fetchCoaching, 1000)
      }
    } catch (error) {
      console.error('Error sending message:', error)
      alert('Failed to send message. Please try again.')
    } finally {
      setSending(false)
    }
  }

  const renderMessage = (msg) => {
    const isParticipant = msg.sender_type === 'participant'
    const isPrivate = msg.is_private
    const isLLM = msg.sender_type.includes('llm')

    return (
      <div
        key={msg.id}
        className={`message ${isParticipant ? 'participant' : isLLM ? 'llm' : 'bot'} ${isPrivate ? 'private' : ''}`}
      >
        <div className="message-sender">
          {msg.sender}
          {msg.sender === currentAnchor && condition === 'rotating_anchor' && (
            <span className="anchor-badge">FACILITATOR</span>
          )}
          {isPrivate && <span style={{ marginLeft: '8px', fontSize: '0.85em' }}>(Private Coaching)</span>}
        </div>
        <div className="message-content">{msg.content}</div>
      </div>
    )
  }

  return (
    <div className="card">
      <h2>
        Discussion: {challengeQuestion.split('\n')[0]}
        {isParticipantAnchor && (
          <span className="anchor-badge" style={{ marginLeft: '15px' }}>
            YOU ARE FACILITATING
          </span>
        )}
      </h2>

      {condition === 'rotating_anchor' && currentAnchor && (
        <div className="info-box" style={{ marginBottom: '15px' }}>
          <p>
            <strong>Current Facilitator:</strong> {currentAnchor}
            {isParticipantAnchor && ' (You!)'}
          </p>
          <p style={{ fontSize: '0.9em', marginTop: '5px' }}>
            The facilitator role rotates every 3 minutes. {isParticipantAnchor ? 'Use the coaching suggestions below to guide the discussion.' : 'Respond to the facilitator\'s prompts and contribute to the discussion.'}
          </p>
        </div>
      )}

      {isParticipantAnchor && coaching && (
        <div style={{ 
          backgroundColor: '#fff3cd', 
          border: '2px solid #ffc107',
          borderRadius: '8px',
          padding: '15px',
          marginBottom: '15px'
        }}>
          <strong>💡 Coaching Suggestion:</strong>
          <p style={{ marginTop: '8px', marginBottom: 0 }}>{coaching}</p>
        </div>
      )}

      <div className="chat-container">
        {messages.length === 0 && (
          <p style={{ textAlign: 'center', color: '#999', padding: '20px' }}>
            Discussion starting... Post your initial thoughts on the challenge question!
          </p>
        )}
        
        {messages.map(renderMessage)}
        <div ref={chatEndRef} />
      </div>

      <form onSubmit={handleSendMessage}>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder={isParticipantAnchor ? "Guide the discussion..." : "Type your message..."}
          disabled={sending}
          style={{ marginBottom: '10px' }}
        />
        <button type="submit" disabled={sending || !newMessage.trim()}>
          {sending ? 'Sending...' : 'Send'}
        </button>
      </form>

      <p style={{ marginTop: '15px', fontSize: '0.9em', color: '#666' }}>
        Discussion will end automatically when time expires. Keep contributing!
      </p>
    </div>
  )
}

export default Chat