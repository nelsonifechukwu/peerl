# STUDY EXECUTION CHECKLIST

**Use this checklist when running your actual study**

---

## PRE-STUDY PREPARATION

### Ethics & Documentation
- [ ] Ethics approval obtained from Cambridge review board
- [ ] Participant Information Sheet printed/ready
- [ ] Consent forms printed/ready  
- [ ] Demographic questionnaire printed/ready
- [ ] Debrief statement prepared

### Technical Setup
- [ ] Backend tested and running smoothly
- [ ] Frontend tested on multiple devices/browsers
- [ ] OpenAI API key has sufficient credits ($20+ recommended)
- [ ] Database backup system in place
- [ ] Network/WiFi stable and tested

### Content Review
- [ ] Priming texts reviewed for clarity
- [ ] Challenge questions are appropriate difficulty
- [ ] Quiz questions have correct answers verified
- [ ] Timings tested (34 minutes total confirmed)

---

## PHASE 1: IN-PERSON (4 PARTICIPANTS)

### Before First Participant
- [ ] Laptop/computer ready with platform running
- [ ] Room booked and set up
- [ ] WiFi password available
- [ ] Consent forms ready
- [ ] Timer/clock visible

### For Each Participant (P001-P004)

**Pre-Session (5 mins):**
- [ ] Greet participant warmly
- [ ] Provide Participant Information Sheet
- [ ] Answer any questions
- [ ] Obtain informed consent signature
- [ ] Collect demographic questionnaire
- [ ] Assign them to device/laptop

**During Session (34 mins):**
- [ ] Participant enters name and starts
- [ ] Observe for technical issues ONLY (don't interfere)
- [ ] Note any crashes/bugs in log
- [ ] Remain available but give participant space

**Post-Session (3 mins):**
- [ ] Provide debrief statement
- [ ] Explain AI bots and rationale
- [ ] Answer questions
- [ ] Obtain post-debrief consent confirmation
- [ ] Thank participant

**After Participant Leaves:**
- [ ] Export and back up data immediately
- [ ] Note any issues for fixing

### After Phase 1 Complete
- [ ] Review all 4 sessions for patterns
- [ ] Fix critical bugs only (no protocol changes)
- [ ] Test fixes thoroughly
- [ ] Prepare for Phase 2 deployment

---

## PHASE 2: REMOTE (12 PARTICIPANTS)

### Deployment
- [ ] Platform deployed to cloud (Render/Heroku)
- [ ] Test deployed version thoroughly
- [ ] Confirm URL is accessible
- [ ] Monitoring dashboard ready

### Recruitment
- [ ] Send study invitation with URL
- [ ] Include time commitment (34 mins)
- [ ] Provide researcher contact info
- [ ] Set deadline for participation

### Monitoring (Minimal)
- [ ] Check dashboard daily for technical errors
- [ ] Respond to participant questions promptly
- [ ] Do NOT watch sessions in real-time
- [ ] Export data daily as backup

### After Each Participant
- [ ] Verify their data saved correctly
- [ ] Send thank-you email
- [ ] Provide debrief information via email
- [ ] Request post-debrief consent confirmation

---

## DATA MANAGEMENT

### During Study
- [ ] Export data after each session
- [ ] Store exports in secure location
- [ ] Maintain participant code list separately
- [ ] Never share raw data

### After Study Complete
- [ ] Export final complete dataset
- [ ] Verify N=16 (all participants)
- [ ] Anonymize any remaining identifiable info
- [ ] Back up to multiple secure locations
- [ ] Delete database from public server

---

## DATA ANALYSIS

### Prepare Data
- [ ] Export JSON data to CSV/Excel
- [ ] Create analysis spreadsheet
- [ ] Verify data integrity (no missing responses)

### Primary Analysis
- [ ] Calculate quiz scores per participant per condition
- [ ] Run paired t-test (LLM-Only vs Rotating Anchor)
- [ ] Calculate effect size (Cohen's d)
- [ ] Create visualization (bar chart, box plot)

### Secondary Analysis
- [ ] Count preference proportions
- [ ] Thematically code preference explanations
- [ ] Create preference pie chart

### Exploratory (If Time)
- [ ] ICAP coding of discussion messages
- [ ] Gini coefficient for participation equality
- [ ] Correlation analyses

---

## CW3 WRITING

### Implementation Section (15%)
- [ ] Describe platform architecture
- [ ] Explain bot behavior logic
- [ ] Detail LLM integration
- [ ] Discuss technical challenges solved
- [ ] Include code snippets or diagrams

### Results Section (30%)
- [ ] Report descriptive statistics
- [ ] Present paired t-test results
- [ ] Show preference proportions
- [ ] Include visualizations
- [ ] Report individual patterns

### Discussion Section (30%)
- [ ] Interpret findings
- [ ] Compare to Cai et al.
- [ ] Discuss unexpected patterns
- [ ] Acknowledge limitations
- [ ] Suggest future work

### Other Sections
- [ ] Introduction (5% - from CW1)
- [ ] Procedure (15% - from CW2)
- [ ] Future Work & Conclusion (10%)
- [ ] Overall Clarity (10%)

---

## QUALITY CHECKS

### Technical Quality
- [ ] No crashes during study
- [ ] All data saved correctly
- [ ] Bots behaved realistically
- [ ] Timings worked as designed
- [ ] LLM responses appropriate

### Participant Experience
- [ ] Clear instructions
- [ ] Smooth flow between phases
- [ ] No confusion about roles
- [ ] Debrief effective
- [ ] Ethical concerns addressed

### Data Quality
- [ ] Complete data for all N=16
- [ ] Quiz responses valid
- [ ] Reflections thoughtful
- [ ] Preferences explained
- [ ] No obvious bot detection (ask in debrief)

---

## TROUBLESHOOTING SCENARIOS

**Participant says "I think Alex/Jordan is a bot":**
- Don't confirm or deny during session
- Make note for analysis
- Proceed normally
- Reveal in debrief as planned

**Platform crashes mid-session:**
- Note exact time and error
- Restart participant from last completed phase
- Log as technical issue
- Exclude data if crash corrupted responses

**Participant wants to withdraw:**
- Thank them for their time
- Delete their data immediately
- Don't pressure them
- Note as withdrawal in log

**Bot stops responding:**
- Check backend logs
- Check API rate limits
- May need to restart backend
- Apologize to participant, offer to reschedule

**Participant finishes in <30 minutes:**
- Review their data - did they skip reading?
- Valid completion if all responses given
- Note in log for analysis

---

## POST-STUDY

- [ ] All data exported and backed up
- [ ] Participant list with codes secured
- [ ] Platform shut down (if deployed)
- [ ] Thank participants (email)
- [ ] Begin CW3 writing
- [ ] Submit outstanding work! 🎯

---

**Print this checklist and check off items as you go!**
