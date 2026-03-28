"""
Platform Testing Script
Run this to verify your platform works correctly before the study

Usage:
    python test_platform.py

This script will:
1. Check backend is running
2. Test API endpoints
3. Simulate a complete session
4. Verify data logging
5. Export test data
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"  # Change to deployed URL when testing production

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.RESET}")

def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.RESET}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.RESET}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.RESET}")

def test_backend_health():
    """Test 1: Backend is running"""
    print("\n" + "="*60)
    print("TEST 1: Backend Health Check")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print_success("Backend is running")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Cannot connect to backend: {e}")
        print_info("Make sure backend is running: uvicorn main:app --reload")
        return False

def test_participant_creation():
    """Test 2: Participant registration"""
    print("\n" + "="*60)
    print("TEST 2: Participant Registration")
    print("="*60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/participants",
            json={"name": "Test Participant"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Created participant: {data['participant_id']}")
            print_info(f"  Assigned to Group {data['group_number']}")
            print_info(f"  Module 1: {data['module1_condition']} ({data['module1_topic']})")
            print_info(f"  Module 2: {data['module2_condition']} ({data['module2_topic']})")
            return data
        else:
            print_error(f"Failed to create participant: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error creating participant: {e}")
        return None

def test_session_start(participant_id):
    """Test 3: Session initialization"""
    print("\n" + "="*60)
    print("TEST 3: Session Initialization")
    print("="*60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/sessions/start",
            params={
                "participant_id": participant_id,
                "module_number": 1
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Session started successfully")
            print_info(f"  Session Key: {data['session_key']}")
            print_info(f"  Condition: {data['condition']}")
            print_info(f"  Topic: {data['topic']}")
            return data
        else:
            print_error(f"Failed to start session: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error starting session: {e}")
        return None

def test_content_retrieval(topic):
    """Test 4: Content loading"""
    print("\n" + "="*60)
    print("TEST 4: Content Retrieval")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/content/{topic}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Content loaded successfully")
            print_info(f"  Title: {data['title']}")
            print_info(f"  Priming text length: {len(data['priming_text'])} chars")
            print_info(f"  Challenge question length: {len(data['challenge_question'])} chars")
            print_info(f"  Quiz questions: {len(data['quiz'])}")
            return data
        else:
            print_error(f"Failed to load content: {response.text}")
            return None
    except Exception as e:
        print_error(f"Error loading content: {e}")
        return None

def test_message_sending(session_key):
    """Test 5: Chat messaging"""
    print("\n" + "="*60)
    print("TEST 5: Chat Messaging")
    print("="*60)
    
    messages = [
        "I think eager evaluation makes sense when you'll use all the data.",
        "But lazy evaluation saves memory when you only need a fraction.",
        "The tradeoff is upfront cost versus ongoing cost per access."
    ]
    
    try:
        for i, msg in enumerate(messages, 1):
            response = requests.post(
                f"{BASE_URL}/api/sessions/{session_key}/messages",
                json={"content": msg}
            )
            
            if response.status_code == 200:
                print_success(f"Message {i}/3 sent")
            else:
                print_error(f"Message {i} failed: {response.text}")
                return False
            
            time.sleep(1)  # Space out messages
        
        print_success("All messages sent successfully")
        
        # Retrieve messages
        response = requests.get(f"{BASE_URL}/api/sessions/{session_key}/messages")
        if response.status_code == 200:
            messages = response.json()
            print_info(f"  Retrieved {len(messages)} messages (including participant + bots)")
            return True
        else:
            print_error("Failed to retrieve messages")
            return False
            
    except Exception as e:
        print_error(f"Error in messaging: {e}")
        return False

def test_quiz_submission(session_key, quiz):
    """Test 6: Quiz submission"""
    print("\n" + "="*60)
    print("TEST 6: Quiz Submission")
    print("="*60)
    
    try:
        # Submit quiz (answer all with correct answers for testing)
        responses = [
            {"question_number": q["id"], "selected_answer": q["correct"]}
            for q in quiz
        ]
        
        response = requests.post(
            f"{BASE_URL}/api/sessions/{session_key}/quiz",
            json={"responses": responses}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Quiz submitted successfully")
            print_info(f"  Score: {data['score_percentage']:.0f}%")
            print_info(f"  Correct: {data['correct_count']}/{data['total_questions']}")
            return True
        else:
            print_error(f"Failed to submit quiz: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error submitting quiz: {e}")
        return False

def test_reflection_submission(session_key):
    """Test 7: Reflection submission"""
    print("\n" + "="*60)
    print("TEST 7: Reflection Submission")
    print("="*60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/sessions/{session_key}/reflection",
            json={
                "effectiveness_text": "The discussion format was very effective for understanding the concepts.",
                "helpful_aspects_text": "I found the peer questions most helpful, and the challenge scenario made it concrete."
            }
        )
        
        if response.status_code == 200:
            print_success("Reflection submitted successfully")
            return True
        else:
            print_error(f"Failed to submit reflection: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error submitting reflection: {e}")
        return False

def test_final_preference(participant_id):
    """Test 8: Final preference submission"""
    print("\n" + "="*60)
    print("TEST 8: Final Preference Submission")
    print("="*60)
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/participants/{participant_id}/final-preference",
            json={
                "preferred_condition": "llm_only",
                "explanation": "The LLM facilitator kept the discussion focused and asked good probing questions."
            }
        )
        
        if response.status_code == 200:
            print_success("Final preference submitted successfully")
            return True
        else:
            print_error(f"Failed to submit preference: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error submitting preference: {e}")
        return False

def test_data_export():
    """Test 9: Data export"""
    print("\n" + "="*60)
    print("TEST 9: Data Export")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/data/export")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Data exported successfully")
            print_info(f"  Participants: {len(data['participants'])}")
            print_info(f"  Sessions: {len(data['sessions'])}")
            print_info(f"  Messages: {len(data['messages'])}")
            print_info(f"  Quiz Responses: {len(data['quiz_responses'])}")
            print_info(f"  Reflections: {len(data['reflections'])}")
            print_info(f"  Preferences: {len(data['final_preferences'])}")
            
            # Save to file
            filename = f"test_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print_success(f"Data saved to: {filename}")
            return True
        else:
            print_error(f"Failed to export data: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error exporting data: {e}")
        return False

def run_all_tests():
    """Run complete test suite"""
    print("\n" + "="*60)
    print("PEER LEARNING PLATFORM - AUTOMATED TESTS")
    print("="*60)
    print_info(f"Testing backend at: {BASE_URL}")
    print_info(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": 9
    }
    
    # Test 1: Backend health
    if not test_backend_health():
        print_error("\nBackend not running. Stopping tests.")
        return
    results["passed"] += 1
    
    # Test 2: Participant creation
    participant = test_participant_creation()
    if participant:
        results["passed"] += 1
    else:
        results["failed"] += 1
        print_error("\nCannot proceed without participant. Stopping tests.")
        return
    
    # Test 3: Session start
    session = test_session_start(participant['participant_id'])
    if session:
        results["passed"] += 1
    else:
        results["failed"] += 1
        print_error("\nCannot proceed without session. Stopping tests.")
        return
    
    # Test 4: Content retrieval
    content = test_content_retrieval(session['topic'])
    if content:
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 5: Message sending
    if test_message_sending(session['session_key']):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 6: Quiz submission
    if content and test_quiz_submission(session['session_key'], content['quiz']):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 7: Reflection submission
    if test_reflection_submission(session['session_key']):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 8: Final preference
    if test_final_preference(participant['participant_id']):
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Test 9: Data export
    if test_data_export():
        results["passed"] += 1
    else:
        results["failed"] += 1
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Total tests: {results['total']}")
    print_success(f"Passed: {results['passed']}")
    if results['failed'] > 0:
        print_error(f"Failed: {results['failed']}")
    
    if results['passed'] == results['total']:
        print_success("\n🎉 ALL TESTS PASSED! Platform is ready for deployment.")
    else:
        print_warning(f"\n⚠️  {results['failed']} test(s) failed. Review errors above.")
    
    print_info(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    run_all_tests()
