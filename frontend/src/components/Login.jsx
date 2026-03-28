import { useState } from 'react'
import axios from 'axios'
import API_BASE_URL from '../utils/api'

function Login({ onLogin }) {
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!name.trim()) {
      setError('Please enter your name')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await axios.post(`${API_BASE_URL}/participants`, { name: name.trim() })
      onLogin(response.data)
    } catch (err) {
      setError('Failed to register. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <div className="card">
        <h1>Collaborative Learning Study</h1>
        <p style={{ marginBottom: '20px', color: '#666' }}>
          Welcome! This study investigates collaborative learning formats. 
          The session will take approximately 34 minutes.
        </p>

        <div className="info-box">
          <p><strong>Before you begin:</strong></p>
          <p>• You will participate in two discussion sessions on different topics</p>
          <p>• You will discuss with two other participants (who may include AI systems)</p>
          <p>• There are short quizzes and reflection questions</p>
          <p>• Your participation is voluntary and you can withdraw at any time</p>
        </div>

        <form onSubmit={handleSubmit}>
          <label htmlFor="name" style={{ display: 'block', marginBottom: '10px', fontWeight: 'bold' }}>
            Please enter your name to begin:
          </label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Your name"
            disabled={loading}
          />

          {error && (
            <p style={{ color: 'red', marginBottom: '15px' }}>{error}</p>
          )}

          <button type="submit" disabled={loading}>
            {loading ? 'Registering...' : 'Start Study'}
          </button>
        </form>

        <p style={{ marginTop: '20px', fontSize: '0.85em', color: '#999' }}>
          By participating, you confirm you are 18+ and have read the participant information sheet.
        </p>
      </div>
    </div>
  )
}

export default Login