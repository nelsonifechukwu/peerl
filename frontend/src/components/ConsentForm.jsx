import { useState } from 'react'

function ConsentForm({ onConsent }) {
  const [consents, setConsents] = useState({
    readInfo: false,
    askedQuestions: false,
    voluntary: false,
    dataStorage: false,
    agreeParticipate: false
  })

  const handleCheckbox = (key) => {
    setConsents(prev => ({
      ...prev,
      [key]: !prev[key]
    }))
  }

  const allChecked = Object.values(consents).every(val => val === true)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (allChecked) {
      onConsent()
    }
  }

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: '800px', margin: '20px auto' }}>
        {/* Header */}
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '20px',
          borderBottom: '2px solid #007bff',
          paddingBottom: '15px'
        }}>
          <h1 style={{ margin: 0, fontSize: '1.5em' }}>Participant Information Sheet</h1>
          <img 
            src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/University_of_Cambridge_logo.svg/200px-University_of_Cambridge_logo.svg.png" 
            alt="University of Cambridge"
            style={{ height: '50px' }}
          />
        </div>

        <p style={{ 
          fontStyle: 'italic', 
          color: '#666',
          marginBottom: '20px'
        }}>
          A study investigating Improving Peer-Learning by Rotating Student Facilitators with LLM Support.
        </p>

        <p style={{ marginBottom: '20px', lineHeight: '1.6' }}>
          Thank you for your interest in this study. Before you decide to take part, it is important for you to 
          understand why the research is being done and what it will involve. Please take time to read the following 
          information carefully and discuss it with others if you wish. The study organiser is available if there is 
          anything that is not clear or if you would like more information. Take time to decide whether or not you wish 
          to take part.
        </p>

        {/* Purpose of the study */}
        <h2 style={{ fontSize: '1.1em', marginTop: '25px', marginBottom: '10px' }}>Purpose of the study</h2>
        <p style={{ marginBottom: '20px', lineHeight: '1.6' }}>
          This study investigates how different types of facilitation affect collaborative learning outcomes. You will 
          participate in two 12-minute discussion sessions on related educational topics, experiencing both LLM-facilitated 
          discussion and peer-facilitated discussion with LLM coaching support. Each session will be followed by a 
          brief quiz and reflection. The entire study takes approximately 34 minutes to complete.
        </p>

        {/* Numbered sections */}
        <div style={{ marginBottom: '20px' }}>
          <p style={{ marginBottom: '10px', lineHeight: '1.6' }}>
            <strong>1. Why have I been invited?</strong> You have been invited because you are a university student 
            (age 18+) with access to an internet-connected device. No prior expertise in the discussion topics is required.
          </p>

          <p style={{ marginBottom: '10px', lineHeight: '1.6' }}>
            <strong>2. Do I have to take part?</strong> No, participation is entirely voluntary. If you do decide to 
            take part, you can still withdraw from the study at any time, without giving any reasons.
          </p>

          <p style={{ marginBottom: '10px', lineHeight: '1.6' }}>
            <strong>3. Who is organising the study?</strong> Nelson Elijah and Dr John Dudley are organising the 
            research study. They are based in the Engineering Department at the University of Cambridge.
          </p>

          <p style={{ marginBottom: '10px', lineHeight: '1.6' }}>
            <strong>4. What will happen during the study?</strong> You will join a chat interface where you will 
            discuss educational topics with two other participants (who are actually AI bots, though you won't know 
            this initially—I'm being explicit to call John's attention). You will experience two different discussion 
            formats: one where an LLM facilitates the discussion, and another where participants take turns facilitating 
            with LLM coaching.
          </p>

          <p style={{ marginBottom: '10px', lineHeight: '1.6' }}>
            <strong>5. What are the possible risks of taking part?</strong> This study poses minimal risk. You will 
            engage in educational discussions on neutral topics with no academic consequences. You may experience minor 
            discomfort if you feel uncertain about contributing to discussions, but facilitators (whether human or LLM) 
            are designed to encourage participation in a supportive way. The 34-minute time commitment is modest. (You 
            will interact with AI bots that you initially believe are human participants—this temporary deception is 
            necessary for study validity and will be fully explained in a debrief immediately after the session, at 
            which point you can choose to withdraw your data, —I'm being explicit to call John's attention.)
          </p>

          <p style={{ marginBottom: '10px', lineHeight: '1.6' }}>
            <strong>6. What happens at the end of the study?</strong> At the end of the study there will be a chance 
            for you to ask any questions that you may have.
          </p>

          <p style={{ marginBottom: '10px', lineHeight: '1.6' }}>
            <strong>7. What will happen to the study results?</strong> The anonymised results will be written up and 
            published in academic papers and presented at research meetings.
          </p>

          <p style={{ marginBottom: '10px', lineHeight: '1.6' }}>
            <strong>8. Anonymity – will I be identified in any publications resulting from the study?</strong> The data 
            will be anonymised and any references to the data will be done so that you are not identifiable.
          </p>

          <p style={{ marginBottom: '10px', lineHeight: '1.6' }}>
            <strong>9. What if there is a problem?</strong> If you have a concern about any aspect of this study, you 
            should ask to speak to the study organiser who will do their best to answer your questions.
          </p>

          <p style={{ marginBottom: '10px', lineHeight: '1.6' }}>
            <strong>10. Who has reviewed the study?</strong> The Department of Engineering Ethics Committee has reviewed 
            this study through the light-touch review process.
          </p>
        </div>

        {/* Contact Information */}
        <div style={{ 
          backgroundColor: '#f8f9fa', 
          padding: '15px', 
          borderRadius: '5px',
          marginBottom: '30px'
        }}>
          <h3 style={{ fontSize: '1em', marginTop: 0, marginBottom: '10px' }}>Contact Information</h3>
          <p style={{ margin: '5px 0' }}>Dr John Dudley</p>
          <p style={{ margin: '5px 0' }}>jd590@cam.ac.uk</p>
          <p style={{ margin: '5px 0' }}>University of Cambridge</p>
        </div>

        {/* Consent Form Section */}
        <div style={{ 
          borderTop: '2px solid #007bff', 
          paddingTop: '20px',
          marginTop: '30px'
        }}>
          <h2 style={{ fontSize: '1.3em', marginBottom: '15px' }}>Participant Consent Form</h2>
          
          <p style={{ 
            fontStyle: 'italic', 
            color: '#666',
            marginBottom: '20px'
          }}>
            A study investigating Improving Peer-Learning by Rotating Student Facilitators with LLM Support.
          </p>

          <p style={{ marginBottom: '15px' }}>
            <strong>Name of Principal Investigator:</strong> Dr John Dudley
          </p>

          <p style={{ marginBottom: '20px' }}>
            Please tick all the boxes that apply:
          </p>

          <form onSubmit={handleSubmit}>
            {/* Checkbox 1 */}
            <label style={{ 
              display: 'flex', 
              alignItems: 'flex-start',
              marginBottom: '15px',
              cursor: 'pointer'
            }}>
              <input 
                type="checkbox"
                checked={consents.readInfo}
                onChange={() => handleCheckbox('readInfo')}
                style={{ 
                  marginRight: '10px', 
                  marginTop: '3px',
                  cursor: 'pointer',
                  width: '18px',
                  height: '18px'
                }}
              />
              <span style={{ lineHeight: '1.5' }}>
                I confirm that I have read and understand the Participant Information Sheet.
              </span>
            </label>

            {/* Checkbox 2 */}
            <label style={{ 
              display: 'flex', 
              alignItems: 'flex-start',
              marginBottom: '15px',
              cursor: 'pointer'
            }}>
              <input 
                type="checkbox"
                checked={consents.askedQuestions}
                onChange={() => handleCheckbox('askedQuestions')}
                style={{ 
                  marginRight: '10px', 
                  marginTop: '3px',
                  cursor: 'pointer',
                  width: '18px',
                  height: '18px'
                }}
              />
              <span style={{ lineHeight: '1.5' }}>
                I have had the opportunity to ask questions and have had these answered satisfactorily.
              </span>
            </label>

            {/* Checkbox 3 */}
            <label style={{ 
              display: 'flex', 
              alignItems: 'flex-start',
              marginBottom: '15px',
              cursor: 'pointer'
            }}>
              <input 
                type="checkbox"
                checked={consents.voluntary}
                onChange={() => handleCheckbox('voluntary')}
                style={{ 
                  marginRight: '10px', 
                  marginTop: '3px',
                  cursor: 'pointer',
                  width: '18px',
                  height: '18px'
                }}
              />
              <span style={{ lineHeight: '1.5' }}>
                I understand that my participation is voluntary and that I am free to withdraw at any time 
                without giving a reason.
              </span>
            </label>

            {/* Checkbox 4 */}
            <label style={{ 
              display: 'flex', 
              alignItems: 'flex-start',
              marginBottom: '15px',
              cursor: 'pointer'
            }}>
              <input 
                type="checkbox"
                checked={consents.dataStorage}
                onChange={() => handleCheckbox('dataStorage')}
                style={{ 
                  marginRight: '10px', 
                  marginTop: '3px',
                  cursor: 'pointer',
                  width: '18px',
                  height: '18px'
                }}
              />
              <span style={{ lineHeight: '1.5' }}>
                I agree that data gathered in this study may be stored anonymously and securely, and 
                may be used for future research.
              </span>
            </label>

            {/* Checkbox 5 */}
            <label style={{ 
              display: 'flex', 
              alignItems: 'flex-start',
              marginBottom: '25px',
              cursor: 'pointer'
            }}>
              <input 
                type="checkbox"
                checked={consents.agreeParticipate}
                onChange={() => handleCheckbox('agreeParticipate')}
                style={{ 
                  marginRight: '10px', 
                  marginTop: '3px',
                  cursor: 'pointer',
                  width: '18px',
                  height: '18px'
                }}
              />
              <span style={{ lineHeight: '1.5' }}>
                I agree to take part in this study.
              </span>
            </label>

            {/* Submit Button */}
            <button 
              type="submit"
              disabled={!allChecked}
              style={{
                opacity: allChecked ? 1 : 0.5,
                cursor: allChecked ? 'pointer' : 'not-allowed'
              }}
            >
              Begin Study
            </button>

            {!allChecked && (
              <p style={{ 
                marginTop: '10px', 
                color: '#dc3545', 
                fontSize: '0.9em',
                textAlign: 'center'
              }}>
                Please check all boxes to continue
              </p>
            )}
          </form>
        </div>
      </div>
    </div>
  )
}

export default ConsentForm