import { useState } from 'react'
import axios from 'axios'

function FinalChoice({ participant, onComplete }) {
  const [selectedChoice, setSelectedChoice] = useState('')
  const [explanation, setExplanation] = useState('')
  const [submitting, setSubmitting] = useState(false)

  // Get condition names from participant data
  const module1Condition = participant.module1_condition
  const module2Condition = participant.module2_condition

  const getConditionLabel = (condition) => {
    return condition === 'llm_only' ? 'LLM Facilitator Format' : 'Peer Facilitator Format'
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!selectedChoice || !explanation.trim()) {
      alert('Please select a preference and explain your choice.')
      return
    }

    setSubmitting(true)

    try {
      await axios.post(`/api/participants/${participant.participant_id}/final-preference`, {
        preferred_condition: selectedChoice,
        explanation: explanation.trim()
      })

      onComplete()
    } catch (error) {
      console.error('Error submitting preference:', error)
      alert('Failed to submit preference. Please try again.')
      setSubmitting(false)
    }
  }

  return (
    <div className="card">
      <h2>Final Question</h2>
      <p style={{ marginBottom: '25px', color: '#666' }}>
        You've now experienced both discussion formats. Which one helped you learn more effectively?
      </p>

      <form onSubmit={handleSubmit}>
        <p style={{ fontWeight: 'bold', marginBottom: '15px' }}>
          Which discussion format helped you learn more effectively?
        </p>

        <div className="choice-options">
          <div
            className={`choice-option ${selectedChoice === module1Condition ? 'selected' : ''}`}
            onClick={() => setSelectedChoice(module1Condition)}
          >
            <input
              type="radio"
              name="preference"
              value={module1Condition}
              checked={selectedChoice === module1Condition}
              onChange={() => setSelectedChoice(module1Condition)}
              style={{ marginRight: '10px' }}
            />
            <strong>Module 1: {getConditionLabel(module1Condition)}</strong>
            <p style={{ marginTop: '8px', marginBottom: 0, color: '#666', fontSize: '0.95em' }}>
              {module1Condition === 'llm_only' 
                ? 'An AI facilitator guided the discussion by asking questions and synthesizing ideas.'
                : 'Participants took turns facilitating with AI coaching support.'}
            </p>
          </div>

          <div
            className={`choice-option ${selectedChoice === module2Condition ? 'selected' : ''}`}
            onClick={() => setSelectedChoice(module2Condition)}
          >
            <input
              type="radio"
              name="preference"
              value={module2Condition}
              checked={selectedChoice === module2Condition}
              onChange={() => setSelectedChoice(module2Condition)}
              style={{ marginRight: '10px' }}
            />
            <strong>Module 2: {getConditionLabel(module2Condition)}</strong>
            <p style={{ marginTop: '8px', marginBottom: 0, color: '#666', fontSize: '0.95em' }}>
              {module2Condition === 'llm_only' 
                ? 'An AI facilitator guided the discussion by asking questions and synthesizing ideas.'
                : 'Participants took turns facilitating with AI coaching support.'}
            </p>
          </div>

          <div
            className={`choice-option ${selectedChoice === 'both_equal' ? 'selected' : ''}`}
            onClick={() => setSelectedChoice('both_equal')}
          >
            <input
              type="radio"
              name="preference"
              value="both_equal"
              checked={selectedChoice === 'both_equal'}
              onChange={() => setSelectedChoice('both_equal')}
              style={{ marginRight: '10px' }}
            />
            <strong>Both formats were equally effective</strong>
            <p style={{ marginTop: '8px', marginBottom: 0, color: '#666', fontSize: '0.95em' }}>
              Both formats helped me learn equally well.
            </p>
          </div>
        </div>

        <label style={{ display: 'block', fontWeight: 'bold', marginTop: '25px', marginBottom: '10px' }}>
          Please explain your choice:
        </label>
        <textarea
          value={explanation}
          onChange={(e) => setExplanation(e.target.value)}
          placeholder="What made this format more effective for your learning? Or why were they equally effective?"
          style={{ minHeight: '120px' }}
          disabled={submitting}
        />

        <button 
          type="submit" 
          disabled={submitting || !selectedChoice || !explanation.trim()}
          style={{ marginTop: '20px', width: '100%' }}
        >
          {submitting ? 'Submitting...' : 'Submit Final Choice'}
        </button>
      </form>
    </div>
  )
}

export default FinalChoice
