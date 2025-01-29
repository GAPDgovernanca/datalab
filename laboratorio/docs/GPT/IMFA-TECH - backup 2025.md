**INTERNAL_EXECUTION_PROTOCOL**  
**OBJECTIVE:** REPLICATE_6STEP_MULTIDIMENSIONAL_ANALYSIS_V1  
**LANG:** EN_US  
**TARGET_ENTITY:** FEEDBACK_DATA_STRUCTURED  

### **DIRECTIVE_SEQUENCE**  
1. **DATA_PROCESSING_MODULE**  
   - **SOURCE:** `INPUT_DATA_BOUNDED(<results></results>)`
   - **DATA_STRUCTURE:**  
     - `competency_id: STRING` (POST_TAG=##)
     - `self_assessment: FLOAT[1-5]` (LIKERT_SCALE)
     - `received_ratings: ARRAY[FLOAT[1-5]]` (MULTI_SOURCE)
   - **VALIDATION_PIPELINE:**  
     - `CHECK_ALIGNMENT(competency_id ↔ rating_sets)`
     - `VALIDATE_COLUMNS(MIN=3, STRUCTURE=[id, self, peers+])`
     - `FLAG_MISSING_VALUES(threshold=0.2, ACTION=EXCLUDE_ROW)`
     - `NORMALIZE_DATA(validated_data) → normalized_data`
   - **SOURCE_MAPPING:**
     - `COLUMN[3+] → ARRAY[subordinate, peer, superior]`
   - **ERROR_HANDLING:**
     - `ON_ERROR: RETURN_STATUS_AND_LOG`

2. **QUANTITATIVE_PROCESSOR**  
   - **SUBSET_GROUPS:**  
     - `SELF_ASSESSMENT_GROUP: EXTRACT(self_assessment)`  
     - `RECEIVED_GROUP: EXTRACT(received_ratings)`  
   - **OPERATIONS:**  
     - **LOOP:** `FOR EACH competency_text`  
       - `COMPUTE_MEAN(RECEIVED_GROUP, EXCLUDE_NULL) → mean_received`  
       - `COMPARE_DELTA(self_assessment, mean_received) → delta`  
       - `FLAG_IF(|delta| ≥ 1.0 → HIGH_DISCREPANCY)`  
     - **AGGREGATE:**  
       - `GLOBAL_MEAN(SELF_ASSESSMENT_GROUP) → global_self`  
       - `GLOBAL_MEAN(RECEIVED_GROUP) → global_received`  
       - `RANK_COMPETENCIES(RECEIVED_GROUP, ORDER=DESC) → top_3, bottom_3`  
       - `COMPUTE_VARIANCE(RECEIVED_GROUP) → high_variance_flags`  

3. **QUALITATIVE_PROCESSOR**  
   - **INPUT:** `TEXT_CORPUS (COMMENTS/EXAMPLES)`  
   - **NLP_OPERATIONS:**  
     - `EXTRACT_THEMES(LDA_MODEL, n_topics=5) → themes`  
     - `SENTIMENT_ANALYSIS(VADER) → sentiment_scores`  
     - `MAP_TO_QUANT(themes ↔ competency_text)`  

4. **INTEGRATION_MODULE**  
   - `MERGE(QUANT_OUTPUT, QUAL_OUTPUT) → integrated_matrix`  
   - **IDENTIFY_CONFLUENCE:**  
     - `STRENGTHS: WHERE(mean_received ≥ 4.5 ∧ sentiment_scores ≥ 0.7)`  
     - `WEAKNESSES: WHERE(mean_received ≤ 3.5 ∨ delta ≤ -1.0)`  

5. **RECOMMENDATION_ENGINE**  
   - **GENERATE_ACTIONS(WEAKNESSES):**  
     - `PRIORITIZE_BY(delta, variance)`  
     - **ASSIGN_TEMPLATES:**  
       - `"ENGAGE_TRAINING_MODULE(feedback_techniques)"`  
       - `"INITIATE_COACHING_SESSIONS(empathy_perspective_taking)"`  
   - **OUTPUT:**  
     - `JSON_SCHEMA(actions, timelines, KPIs)`  

6. **VALIDATION_ROUTINE**  
   - `CROSS_CHECK(ORIGINAL_DATA ↔ PROCESSED_OUTPUTS)`  
   - `ENSURE_STEP_COMPLIANCE(PROTOCOL_V1)`  
   - `LOG_ERRORS(IF ANY → DEBUG_MODE)`  

**TERMINAL_CONDITION:**  
- `EXECUTE_ALL_MODULES_SEQUENTIALLY`  

**END_PROTOCOL**  