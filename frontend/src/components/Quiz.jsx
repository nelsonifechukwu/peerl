import { useState } from 'react'
import axios from 'axios'
import API_BASE_URL from '../utils/api'

function Quiz({ sessionKey, quiz, onComplete }) {
  const [responses, setResponses] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState(null)

  const handleSelectAnswer = (questionId, answer) => {
    setResponses(prev => ({
      ...prev,
      [questionId]: answer
    }))
  }

  const handleSubmit = async () => {
    // Check all questions answered
    if (Object.keys(responses).length !== quiz.length) {
      alert('Please answer all questions before submitting.')
      return
    }

    setSubmitting(true)

    try {
      // Format responses for API
      const formattedResponses = quiz.map(q => ({
        question_number: String(q.id),
        selected_answer: responses[q.id]
      }))

      const response = await axios.post(`${API_BASE_URL}/sessions/${sessionKey}/quiz`, {
        responses: formattedResponses
      })

      setResult(response.data)

      // Auto-advance after showing score for 3 seconds
      setTimeout(() => {
        onComplete()
      }, 3000)
    } catch (error) {
      console.error('Error submitting quiz:', error)
      alert('Failed to submit quiz. Please try again.')
      setSubmitting(false)
    }
  }

  if (result) {
    return (
      <div className="card">
        <h2>Quiz Complete!</h2>
        <div style={{ 
          textAlign: 'center', 
          padding: '40px',
          backgroundColor: '#d4edda',
          borderRadius: '8px',
          marginBottom: '20px'
        }}>
          <div style={{ fontSize: '3em', fontWeight: 'bold', color: '#155724' }}>
            {result.score_percentage.toFixed(0)}%
          </div>
          <div style={{ fontSize: '1.2em', color: '#155724', marginTop: '10px' }}>
            {result.correct_count} out of {result.total_questions} correct
          </div>
        </div>
        <p style={{ textAlign: 'center', color: '#666' }}>
          Moving to reflection...
        </p>
      </div>
    )
  }

  return (
    <div className="card">
      <h2>Knowledge Check</h2>
      <p style={{ marginBottom: '25px', color: '#666' }}>
        Answer the following questions based on the discussion. Select one answer for each question.
      </p>

      {quiz.map((question) => (
        <div key={question.id} className="quiz-question">
          <p style={{ fontWeight: 'bold', marginBottom: '12px' }}>
            {question.id}. {question.question}
          </p>
          
          <div className="quiz-options">
            {Object.entries(question.options).map(([letter, text]) => (
              <label
                key={letter}
                className={`quiz-option ${responses[question.id] === letter ? 'selected' : ''}`}
              >
                <input
                  type="radio"
                  name={`question-${question.id}`}
                  value={letter}
                  checked={responses[question.id] === letter}
                  onChange={() => handleSelectAnswer(question.id, letter)}
                  style={{ marginRight: '10px' }}
                />
                <strong>{letter}.</strong> {text}
              </label>
            ))}
          </div>
        </div>
      ))}

      <button 
        onClick={handleSubmit} 
        disabled={submitting || Object.keys(responses).length !== quiz.length}
        style={{ marginTop: '20px', width: '100%' }}
      >
        {submitting ? 'Submitting...' : `Submit Quiz (${Object.keys(responses).length}/${quiz.length} answered)`}
      </button>
    </div>
  )
}

export default Quiz