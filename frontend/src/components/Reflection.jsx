import { useState } from 'react'
import axios from 'axios'

function Reflection({ sessionKey, onComplete }) {
  const [effectivenessText, setEffectivenessText] = useState('')
  const [helpfulAspectsText, setHelpfulAspectsText] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!effectivenessText.trim() || !helpfulAspectsText.trim()) {
      alert('Please answer both reflection questions.')
      return
    }

    setSubmitting(true)

    try {
      await axios.post(`/api/sessions/${sessionKey}/reflection`, {
        effectiveness_text: effectivenessText.trim(),
        helpful_aspects_text: helpfulAspectsText.trim()
      })

      onComplete()
    } catch (error) {
      console.error('Error submitting reflection:', error)
      alert('Failed to submit reflection. Please try again.')
      setSubmitting(false)
    }
  }

  return (
    <div className="card">
      <h2>Reflection</h2>
      <p style={{ marginBottom: '25px', color: '#666' }}>
        Please reflect on your experience in this module. Your honest feedback helps us understand what works best for learning.
      </p>

      <form onSubmit={handleSubmit}>
        <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '10px' }}>
          1. How effectively did this discussion format help you understand the topic?
        </label>
        <textarea
          value={effectivenessText}
          onChange={(e) => setEffectivenessText(e.target.value)}
          placeholder="Share your thoughts on how effective this format was for learning..."
          style={{ minHeight: '120px' }}
          disabled={submitting}
        />

        <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '10px', marginTop: '20px' }}>
          2. What aspects were most or least helpful for your learning?
        </label>
        <textarea
          value={helpfulAspectsText}
          onChange={(e) => setHelpfulAspectsText(e.target.value)}
          placeholder="What worked well? What could be improved?"
          style={{ minHeight: '120px' }}
          disabled={submitting}
        />

        <button 
          type="submit" 
          disabled={submitting || !effectivenessText.trim() || !helpfulAspectsText.trim()}
          style={{ marginTop: '20px', width: '100%' }}
        >
          {submitting ? 'Submitting...' : 'Submit Reflection'}
        </button>
      </form>
    </div>
  )
}

export default Reflection
