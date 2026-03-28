import { useState } from 'react'
import Login from './components/Login'
import SessionFlow from './components/SessionFlow'

function App() {
  const [participant, setParticipant] = useState(null)
  const [currentModule, setCurrentModule] = useState(1)
  const [studyComplete, setStudyComplete] = useState(false)

  const handleLogin = (participantData) => {
    setParticipant(participantData)
  }

  const handleModuleComplete = () => {
    if (currentModule === 1) {
      setCurrentModule(2)
    } else {
      setStudyComplete(true)
    }
  }

  if (studyComplete) {
    return (
      <div className="container">
        <div className="card">
          <h1>Study Complete!</h1>
          <h2>Debrief Information</h2>
          
          <div className="info-box">
            <p><strong>Important Information:</strong></p>
            <p>During this study, the two other participants you interacted with (Alex and Jordan) were actually AI bots programmed to simulate peer learner behavior.</p>
          </div>

          <p style={{ marginBottom: '15px' }}>
            This deception was necessary to ensure study feasibility - recruiting 48 participants for genuine three-person groups would have exceeded available resources. The bots were designed to behave realistically based on research on collaborative learning.
          </p>

          <p style={{ marginBottom: '15px' }}>
            All other aspects of the study were as described. The LLM facilitator and LLM coaching were real AI systems, and your learning outcomes were genuinely measured.
          </p>

          <p style={{ marginBottom: '20px', fontWeight: 'bold' }}>
            You have the right to withdraw your data from this study without penalty.
          </p>

          <p style={{ marginBottom: '15px' }}>
            If you consent to your data being used for this research now that you understand the full study design, please confirm below:
          </p>

          <button onClick={() => window.location.href = '/'}>
            I consent to my data being used
          </button>

          <p style={{ marginTop: '20px', fontSize: '0.9em', color: '#666' }}>
            Thank you for participating! If you have questions, please contact the researcher.
          </p>
        </div>
      </div>
    )
  }

  if (!participant) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <SessionFlow
      participant={participant}
      moduleNumber={currentModule}
      onModuleComplete={handleModuleComplete}
    />
  )
}

export default App
