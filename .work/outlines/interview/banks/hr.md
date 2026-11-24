# HR and behavioral bank: src/content/interview/hr.json | category "hr" | 60 items | ids interview-hr-001..060
Schema {id, category "hr", question, whatInterviewerIsTesting, modelAnswer, followUps[2-3], commonMistakes[2-3], difficulty}.
modelAnswer = 4-8 short sentences, first person ("I"), written AS Nishchay would say it, STAR for story questions (Situation, Task, Action, Result with one number). Simple English. No real company names. No lying: where a story needs facts, use only profile facts or label as an example learner can swap ("Replace with your own project").

## Profile facts to use (src/data/profile.json)
- B.Tech CSE (Core), graduating 2027; coding level basic; studies 5-6 h/day; wants first job as fast as possible.
- Current UI/UX internship, does not want to continue in design. Transferable: user empathy, dashboards/readability, stakeholder feedback loops, Figma-style structured thinking, working with developers, deadlines.
- Target: Data Analyst; fintech first, healthcare second, consulting third. Any city in India, remote fine (relocation = yes, no constraint).
- Long-term: Data Analyst then Data Engineer or Analytics Engineer in 2-3 years.
- Projects: site's portfolio projects (UPI failure analysis, e-commerce RFM, etc.) described as "my projects" in generic terms; learner must have finished them.
## Personalisation rules for writer
- Never disparage design or the internship; frame as "I liked the user side; I found I enjoy answering why with data".
- Weakness answers must be real-ish and show a fix: basic coding depth -> daily SQL/Python practice with numbers.
- Fintech answers: mention UPI failures, trust, risk, ticket size, KYC.
- Relocation/shift/notice answers: flexible; notice period "none/immediate for graduate; internship ends before joining" (state as example).
- Salary: range-based, no number invented as fact; "in line with the role and market for freshers".
- Add 1 line in commonMistakes naming the usual fresher error.

## The 60 questions (id | difficulty | question | personalisation / key point)
### A. Opening and motivation (10)
001 easy Tell me about yourself. | 60-90 s: CSE 2027, UI/UX internship, discovered data, projects, goal fintech DA
002 easy Why do you want to be a Data Analyst? | curiosity about why; decisions from data; skill proof = projects
003 easy Why are you moving from UI/UX to data? | honest, positive; keep user empathy
004 easy Why this company? | research 3 facts; fintech trust + scale; avoid generic
005 easy Why fintech? | UPI scale, high-volume data, real impact; first preference
006 easy Where do you see yourself in 5 years? | DA -> DE/AE; ownership; learning
007 easy What do you know about our product/business? | structure: product, customers, metric, one idea
008 medium Why should we hire you over other freshers? | projects + communication + speed to learn; evidence not adjectives
009 medium What makes you a good fit for a data role given your design background? | stakeholder empathy, visuals
010 medium Walk me through your resume. | order by relevance; internship, projects, skills
### B. Strengths, weaknesses, self-awareness (7)
011 easy What are your strengths? | pick 2 with proof
012 easy What is your weakness? | coding depth still growing; routine to fix; measurable progress
013 easy How do you handle feedback? | design critique experience
014 medium What is your biggest achievement? | STAR; project or internship result with number
015 medium How do you prioritise learning many tools? | roadmap: SQL first, then Python/Power BI
016 medium How would your friends/teammates describe you? | 
017 medium Tell me about something you taught yourself recently. | SQL/Python self-study with hours/day 5-6
### C. Failure, conflict, pressure (9)
018 medium Tell me about a failure. | STAR; learning; example swap
019 medium Tell me about a conflict with a teammate. | design-dev disagreement; resolved via data/user test
020 medium Describe a time you worked under pressure/tight deadline. | internship delivery
021 medium How do you handle stress? | routine, breaks, prioritise
022 medium Tell me about a time you made a mistake in your work. | validate-before-share lesson
023 medium How do you handle criticism from a manager you disagree with? | listen, check facts, discuss
024 medium Tell me about a time you disagreed with a decision. | evidence-based
025 hard Describe a time you had to learn something very fast. | 
026 hard Tell me about a time you had incomplete information and still had to decide. | assumptions stated
### D. Teamwork, communication, ownership (7)
027 easy Do you prefer working alone or in a team? | both; examples
028 medium How do you explain a technical idea to a non-technical person? | analogy; UI/UX presentations
029 medium Tell me about a time you led something. | college/ internship; no title needed
030 medium How do you manage time between college and internship? | 
031 medium How do you work with someone who doesn't respond? | follow up, escalate politely
032 medium Describe your ideal manager/work environment. | clear goals, feedback
033 hard How would you handle a stakeholder who keeps changing the requirement? | scope, written agreement
### E. Education, gap, background (6)
034 easy Tell me about your academic projects. | 
035 easy What are your marks/CGPA and what do you think about them? | honest; skills over marks; (if low, own it)
036 medium Do you have any gap in education/career? | none; if exists, honest reason + productive use (template)
037 medium Why did you choose CSE and not a data/AI specialisation? | Core CSE strengths: DBMS, OS, algorithms
038 medium What did you learn from your internship that applies here? | 
039 medium You have basic coding skills; how will you handle Python/SQL tasks? | proof: daily practice, projects, timed tests
### F. Logistics and compensation (10)
040 easy Are you willing to relocate? | yes, any Indian city; remote fine; details to confirm
041 easy Are you comfortable with shift work/night shifts? | state honest limits; flexibility for roles needing coverage
042 easy What is your notice period? | none/ends before joining; internship wrap-up
043 easy When can you join? | after graduation 2027 unless earlier internship allowed; clarify
044 easy What are your salary expectations? | researched range; flexible
045 medium Why are you looking for a change when you have an internship? | growth not escape
046 medium Do you have other offers/interviews in process? | honest; no pressure
047 medium Are you okay with a service agreement/bond? | ask terms; need to read
048 medium What is your current stipend/CTC and expected? | honesty; fresher framing
049 medium What if we offer lower than your expectation? | ask growth, review timeline
### G. Role fit and situational (8)
050 medium What would you do in your first 30 days? | learn data, metrics, stakeholders
051 medium How do you stay updated with data trends? | specific habits, sites
052 medium Describe how you would handle a very repetitive task. | automate, document
053 hard You made an analysis error that went to a client: what do you do? | tell fast, fix, prevent
054 hard A senior asks you to change numbers to look better. | refuse, escalate, explain
055 hard Your manager asks for a report in 1 hour but needs 3 hours to do right. | clarify, partial deliver, communicate
056 hard How do you handle working on multiple projects with conflicting deadlines? | 
057 hard Tell me about a time you went above and beyond. | 
### H. Closing (3)
058 easy Do you have any questions for us? | give 6 good ones (team data stack, first-90-day success, mentoring, metrics, growth path to DE/AE, project example); avoid salary-first
059 easy Is there anything else you want us to know? | one-line close with evidence
060 hard If you do not get this job, what will you do? | improve, continue; same direction
Total difficulty as listed: easy 20 / medium 31 / hard 9 (final; do not relabel). Sections A-H headings are for planning only.
