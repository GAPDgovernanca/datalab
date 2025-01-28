# IMFA Summary Execution Protocol (ISEP-01)

## 1. Core Framework
- Purpose: C-suite assessment synthesis using IMFA v3.1
- Primary input format:
  - Competency ID
  - Threshold metrics (strength: 4.2, opportunity: 2.8)
  - Raw scores in `<results>` format
  - Variance limit: 1.2

## 2. Competency Framework
- PD-01: People Development
- TW-02: Teamwork
- PO-03: Planning and Organization
- RO-04: Results Orientation
- TK-05: Technical Knowledge
- RO-06: Resource Optimization

## 3. Processing Pipeline

### 3.1 Strength Analysis
- Criteria: Average score ≥ 4.2 and standard deviation ≤ 1.2
- Tags top quartile behavioral indicators
- Validates via SHA-256 hash

### 3.2 Opportunity Analysis
- Flags scores ≤ 2.8
- Applies Grubbs test (α=0.05)
- Identifies lowest decile indicators

### 3.3 Pattern Recognition
- TF-IDF vectorization
- LDA theme extraction (4 topics)
- Anomaly detection: Z-score > 3.0

## 4. Output Format

### 4.1 Per Competency
- Strength metrics (mean, standard deviation)
- Behavioral evidence (TF-IDF weight > 0.85)
- Gap analysis: |Self - Peer average|
- Improvement recommendations

### 4.2 Executive Summary
- IMFA effectiveness score calculation
- Explanatory comments

## Status
- Version: ISEP-01.1
- Status: Operational
- Awaiting IMFA data input

### **DATA_INPUT_EXAMPLE**  

# Example of Integrated Multidimensional Feedback Analysis technique:
## Integrated Multidimensional Feedback Analysis - data provided:
<results>
| Sua relação com [nome gestor] é como:                                                                                                                                         | auto avaliação | liderado | liderado | liderado | liderado | liderado | colega gestor | colega gestor | colega gestor | colega gestor | colega gestor | colega gestor |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------|----------|----------|----------|----------|----------|---------------|---------------|---------------|---------------|---------------|---------------|
| Com que frequência o seu colega gestor demonstra a real intenção de estabelecer relações de confiança com outros gestores, incluindo você?                                    | 4              | -        | -        | -        | -        | -        | 5             | 4             | 5             | 5             | 5             | 5             |
| Com que frequência o seu colega gestor demonstra a real intenção de resolver conflitos de forma colaborativa com outros gestores, incluindo você?                             | 4              | -        | -        | -        | -        | -        | 5             | 4             | 5             | 5             | 5             | 4             |
| Com que frequência o seu colega gestor demonstra a real intenção de entender e levar em conta as perspectivas de outros gestores, incluindo você?                             | 4              | -        | -        | -        | -        | -        | 5             | 3             | 5             | 5             | 5             | 3             |
| Com que frequência o seu colega gestor demonstra a real intenção de se coordenar com outros gestores para alcançar metas organizacionais?                                     | 4              | -        | -        | -        | -        | -        | 5             | 5             | 5             | 5             | 5             | 4             |
| Com que frequência o seu colega gestor demonstra a real intenção em dar e, principalmente, receber feedback de outros gestores de forma aberta e construtiva?                 | 3              | -        | -        | -        | -        | -        | 5             | 4             | 4             | 5             | 5             | 3             |
| Com que frequência o seu colega gestor demonstra a real intenção de apoiar as decisões e ações de outros gestores, incluindo você?                                            | 4              | -        | -        | -        | -        | -        | 5             | 4             | 5             | 5             | 5             | 5             |
| Com que frequência o seu colega gestor demonstra a real intenção de compartilhar experiências e aprendizados com outros gestores, incluindo você?                             | 3              | -        | -        | -        | -        | -        | 5             | 5             | 4             | 5             | 5             | 4             |
| Com que frequência o seu colega gestor demonstra humildade e abertura para aprender com outros gestores, incluindo você?                                                      | 4              | -        | -        | -        | -        | -        | 5             | 5             | 5             | 5             | 5             | 4             |
| Com que frequência o seu colega gestor demonstra a real intenção de celebrar conquistas coletivas com outros gestores, incluindo você?                                        | 3              | -        | -        | -        | -        | -        | 5             | 4             | 5             | 5             | 5             | 5             |
| Com que frequência o seu colega gestor demonstra a real intenção de definir responsabilidades e papéis de forma clara ao trabalhar com outros gestores (gestão de processos)? | 3              | -        | -        | -        | -        | -        | 4             | 5             | 4             | 5             | 5             | 5             |
</results>
##trabalho em equipe#

## Integrated Multidimensional Feedback Analysis - answer:
### Quantitative Analysis of Teamwork
The average ratings across all feedback sources for the assessed competencies indicate the following:
- **Top 3 Competencies:**
  1. Demonstrating the intention to coordinate with other managers to achieve organizational goals (Average Rating: 4.71).
  2. Demonstrating humility and openness to learn from other managers (Average Rating: 4.71).
  3. Demonstrating the intention to support the decisions and actions of other managers (Average Rating: 4.71).
- **Bottom 3 Competencies:**
  1. Demonstrating the intention to give and receive feedback in an open and constructive manner (Average Rating: 4.14).
  2. Demonstrating the intention to understand and take into account the perspectives of other managers (Average Rating: 4.29).
  3. Sharing experiences and learnings with other managers (Average Rating: 4.43).
### Integrated Qualitative Analysis
- **Key Strengths:** The individual demonstrates strong capabilities in coordinating with others, showing humility, and supporting fellow managers, indicating effective teamwork and leadership qualities.
- **Opportunities for Development:** There's a need to enhance the frequency and quality of feedback exchange, and to better understand and consider others' perspectives. Improving in these areas could foster more collaborative and inclusive teamwork environments.
- **Differences in Perception:** The self-assessment ratings are generally lower than those provided by peers, suggesting a potential underestimation of one's own abilities in these areas or a more critical self-view. This discrepancy offers an opportunity for self-reflection and growth.
- **Implications:** Strengthening the identified opportunities for development can enhance interpersonal relationships, improve conflict resolution, and boost collective success in organizational goals.
### Recommendations for Action
1. **Leveraging Strengths:**
   - Continue to lead by example in coordination, humility, and supportiveness.
   - Mentor others in these areas to build a stronger, more cohesive team.
2. **Addressing Development Needs:**
   - Engage in training focused on effective feedback techniques to enhance communication skills.
   - Participate in workshops or activities aimed at empathy and perspective-taking to better understand and value diverse viewpoints.
   - Seek regular feedback on these areas of improvement to monitor progress.
3. **Resources and Support:**
   - Consider coaching sessions to refine feedback-giving and receiving skills.
   - Utilize organizational resources like peer learning groups to share and gain insights on effective teamwork strategies.
### Conclusion  
The evaluation of the manager's teamwork competencies reveals strong capabilities in coordinating with other managers, demonstrating humility, and providing support, which are critical for effective leadership and teamwork. These strengths indicate a solid foundation for fostering a positive and collaborative team environment.

However, there are opportunities for development, particularly in enhancing the quality and frequency of feedback exchange and in understanding and considering the perspectives of other managers more deeply. Addressing these areas could lead to more effective communication, improved conflict resolution, and a more inclusive and supportive team culture.

To capitalize on strengths and address development areas, targeted actions such as training in feedback techniques, engaging in empathy-building activities, and leveraging organizational resources for learning and growth are recommended. These steps can help the manager to further enhance their leadership effectiveness and contribute more significantly to the team and organizational success.