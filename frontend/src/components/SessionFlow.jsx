import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'
import API_BASE_URL from '../utils/api'
import Chat from './Chat'
import Quiz from './Quiz'
import Reflection from './Reflection'
import FinalChoice from './FinalChoice'

function SessionFlow({ participant, moduleNumber, onModuleComplete }) {
  const [phase, setPhase] = useState('intro')
  const [sessionData, setSessionData] = useState(null)
  const [content, setContent] = useState(null)
  const [timeRemaining, setTimeRemaining] = useState(60)
  const [loading, setLoading] = useState(true)

  // CRITICAL FIX: Reset phase when module number changes
  useEffect(() => {
    console.log('=== Module number changed to:', moduleNumber, '===')
    setPhase('intro')
    setLoading(true)
  }, [moduleNumber])

  // Get session configuration and content
  useEffect(() => {
    const initSession = async () => {
      try {
        console.log('Initializing session for module', moduleNumber)
        
        const sessionResponse = await axios.post(`${API_BASE_URL}/sessions/start`, null, {
          params: {
            participant_id: participant.participant_id,
            module_number: moduleNumber
          }
        })
        
        setSessionData(sessionResponse.data)
        console.log('Session data:', sessionResponse.data)

        const contentResponse = await axios.get(`${API_BASE_URL}/content/${sessionResponse.data.topic}`)
        setContent(contentResponse.data)
        console.log('Content loaded for topic:', sessionResponse.data.topic)

        setLoading(false)
      } catch (error) {
        console.error('Session init error:', error)
        alert('Failed to start session. Please refresh and try again.')
      }
    }

    initSession()
  }, [participant, moduleNumber])

  // Phase completion handler wrapped in useCallback
  const handlePhaseComplete = useCallback(() => {
    console.log('=== handlePhaseComplete called ===')
    console.log('Current phase:', phase)
    console.log('Module number:', moduleNumber)
    
    if (phase === 'intro') {
      // Use your test timings - keep them short for testing!
      const primingTime = sessionData?.condition === 'llm_only' ? 10 : 10
      console.log('Starting priming phase with', primingTime, 'seconds')
      setTimeRemaining(primingTime)
      setPhase('priming')
    } else if (phase === 'priming') {
      // Use your test timings
      const discussionTime = sessionData?.condition === 'llm_only' ? 60 : 65
      console.log('Starting discussion phase with', discussionTime, 'seconds')
      setTimeRemaining(discussionTime)
      setPhase('discussion')
    } else if (phase === 'discussion') {
      console.log('Moving to quiz')
      setPhase('quiz')
    } else if (phase === 'quiz') {
      console.log('Moving to reflection')
      setPhase('reflection')
    } else if (phase === 'reflection') {
      if (moduleNumber === 1) {
        console.log('=== Module 1 complete - Starting rest break ===')
        setPhase('rest')
        setTimeRemaining(60)
      } else {
        console.log('=== Module 2 complete - Moving to final choice ===')
        setPhase('final_choice')
      }
    } else if (phase === 'rest') {
      console.log('=== Rest complete - Calling onModuleComplete to start Module 2 ===')
      console.log('Current moduleNumber:', moduleNumber)
      onModuleComplete()
    } else if (phase === 'final_choice') {
      console.log('=== Final choice complete - Study done ===')
      onModuleComplete()
    }
  }, [phase, moduleNumber, sessionData, onModuleComplete])

  // Timer countdown
  useEffect(() => {
    // Phases that don't use timer auto-advance
    if (phase === 'intro' || phase === 'quiz' || phase === 'reflection' || phase === 'final_choice') {
      return
    }

    // If there's time remaining, count down
    if (timeRemaining > 0) {
      const timer = setTimeout(() => {
        setTimeRemaining(prev => prev - 1)
      }, 1000)
      return () => clearTimeout(timer)
    }
    
    // When timer hits 0, advance
    if (timeRemaining === 0) {
      console.log(`=== Timer expired for phase: ${phase} ===`)
      handlePhaseComplete()
    }
  }, [timeRemaining, phase, handlePhaseComplete])

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  if (loading) {
    return (
      <div className="container">
        <div className="card">
          <div className="loading">Loading session...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      {/* Timer (shown during timed phases) */}
      {(phase === 'priming' || phase === 'discussion' || phase === 'rest') && (
        <div className="timer">
          <div>Time Remaining</div>
          <div style={{ fontSize: '1.5em', marginTop: '5px' }}>{formatTime(timeRemaining)}</div>
          <div className="progress">
            Module {moduleNumber}/2 - {phase === 'rest' ? 'Rest' : phase}
          </div>
        </div>
      )}

      {/* Intro Phase */}
      {phase === 'intro' && (
        <div className="card">
          <h1>Module {moduleNumber}: {content.title}</h1>
          
          <div className="info-box">
            <p><strong>Welcome to Module {moduleNumber}!</strong></p>
            <p>In this module, you'll:</p>
            <ul style={{ marginLeft: '20px', marginTop: '10px' }}>
              <li>Read a brief introduction to the topic (2-3 minutes)</li>
              <li>Discuss a challenge question with two other participants ({sessionData.condition === 'llm_only' ? '8' : '9'} minutes)</li>
              <li>Complete a short quiz (2 minutes)</li>
              <li>Reflect on your experience (2 minutes)</li>
            </ul>
          </div>

          <h2 style={{ marginTop: '25px' }}>Challenge Question for This Discussion:</h2>
          <div style={{ 
            padding: '20px', 
            backgroundColor: '#f8f9fa', 
            borderLeft: '4px solid #007bff',
            marginBottom: '20px',
            whiteSpace: 'pre-wrap'
          }}>
            {content.challenge_question}
          </div>

          <button onClick={handlePhaseComplete}>
            Begin Module {moduleNumber}
          </button>
        </div>
      )}

      {/* Priming Phase */}
      {phase === 'priming' && (
        <div className="card">
          <h2>{content.title}</h2>
          <div style={{ 
            whiteSpace: 'pre-wrap',
            lineHeight: '1.6',
            fontSize: '1.05em',
            marginBottom: '20px'
          }}>
            {content.priming_text}
          </div>
          
          <p style={{ color: '#666', fontStyle: 'italic' }}>
            Read the above carefully. The discussion will begin automatically when time expires.
          </p>
        </div>
      )}

      {/* Discussion Phase */}
      {phase === 'discussion' && (
        <Chat
          sessionKey={sessionData.session_key}
          participantName={participant.name}
          condition={sessionData.condition}
          challengeQuestion={content.challenge_question}
          timeRemaining={timeRemaining}
        />
      )}

      {/* Quiz Phase */}
      {phase === 'quiz' && (
        <Quiz
          sessionKey={sessionData.session_key}
          quiz={content.quiz}
          onComplete={handlePhaseComplete}
        />
      )}

      {/* Reflection Phase */}
      {phase === 'reflection' && (
        <Reflection
          sessionKey={sessionData.session_key}
          onComplete={handlePhaseComplete}
        />
      )}

      {/* Rest Phase */}
      {phase === 'rest' && (
        <div className="card">
          <h2>Rest Break</h2>
          <p style={{ marginBottom: '15px' }}>
            Great work! You've completed Module 1. Take a 1-minute break before Module 2.
          </p>
          <p style={{ color: '#666' }}>
            Module 2 will begin automatically when time expires.
          </p>
          
          {/* Emergency manual override button */}
          {timeRemaining === 0 && (
            <button 
              onClick={() => {
                console.log('Manual continue button clicked')
                handlePhaseComplete()
              }}
              style={{ 
                marginTop: '20px',
                backgroundColor: '#28a745'
              }}
            >
              Continue to Module 2 →
            </button>
          )}
        </div>
      )}

      {/* Final Choice Phase */}
      {phase === 'final_choice' && (
        <FinalChoice
          participant={participant}
          onComplete={handlePhaseComplete}
        />
      )}
    </div>
  )
}

export default SessionFlow