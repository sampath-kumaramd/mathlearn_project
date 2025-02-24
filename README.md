# Requirements Specification Document

# AI-Enhanced Mathematics Learning Framework for Visually Impaired Students in Sri Lanka

## 1. Introduction

### 1.1 Purpose

This document defines the requirements for the development of an AI-Enhanced Mathematics Learning Framework specifically designed for 9th-grade visually impaired students in Sri Lanka. The system will utilize artificial intelligence to create an accessible, personalized, and culturally relevant learning environment that addresses the unique challenges faced by visually impaired learners in mathematics education.

### 1.2 Scope

The framework will focus on delivering 9th-grade mathematics curriculum through auditory interfaces and Braille-compatible digital outputs. It will incorporate personalized learning paths, interactive Q&A capabilities, audio-based graph comprehension, and shape recognition features. The system will operate primarily in Sinhala with emphasis on Sri Lankan cultural contexts.

### 1.3 Definitions and Acronyms

- **AI**: Artificial Intelligence
- **NLP**: Natural Language Processing
- **TTS**: Text-to-Speech
- **STEM**: Science, Technology, Engineering, and Mathematics
- **WCAG**: Web Content Accessibility Guidelines

## 2. System Description

### 2.1 System Context

The AI-Enhanced Mathematics Learning Framework will serve as a comprehensive educational tool for visually impaired students in Sri Lanka's educational system. It will operate within the context of the national mathematics curriculum for 9th-grade students, addressing the specific accessibility challenges these students face in mathematical education.

### 2.2 User Characteristics

The system will be designed primarily for:

- 9th-grade students with varying degrees of visual impairment:
  - Congenital blindness (blind since birth)
  - Acquired blindness (became blind later in life)
  - Low vision (partial sight)
- Mathematics teachers working with visually impaired students
- Special education coordinators and administrators

### 2.3 System Dependencies

- Internet connectivity for initial deployment and updates
- Basic ICT infrastructure in schools
- Compatibility with existing screen readers and Braille displays

## 3. Functional Requirements

### 3.1 Sinhala-Centric NLP Architecture

#### 3.1.1 STEM-Specific Language Models

- **FR-1.1**: The system shall utilize STEM-specific language models trained on the UCSC 10M Word Contemporary Sinhala Corpus.
- **FR-1.2**: The system shall recognize and process complex mathematical terminology in Sinhala, including terms like හරය (denominator) and වර්ගමූලය (square root).
- **FR-1.3**: The system shall implement a hybrid tokenization approach that handles both Unicode Sinhala (සමීකරණ) and LaTeX-style equations.

#### 3.1.2 Speech Synthesis for Mathematical Content

- **FR-1.4**: The system shall convert mathematical equations to spoken Sinhala using appropriate pitch modulation and emphasis.
- **FR-1.5**: The system shall integrate with Path Nirvana TTS datasets for natural-sounding speech synthesis.
- **FR-1.6**: The system shall verbalize mathematical expressions with proper terminology and pacing.

#### 3.1.3 Contextual Understanding

- **FR-1.7**: The system shall resolve mathematical term ambiguities (e.g., කෝණ for angle/coin) using curriculum-aligned semantic analysis.
- **FR-1.8**: The system shall understand and process mathematical queries in conversational Sinhala.

### 3.2 Cultural Problem Generator

#### 3.2.1 Localized Context Integration

- **FR-2.1**: The system shall convert generic algebra problems to culturally relevant scenarios while maintaining mathematical integrity.
- **FR-2.2**: The system shall incorporate Sri Lankan agricultural contexts in problem formulation.
- **FR-2.3**: The system shall maintain a 60:40 rural-to-urban scenario ratio in generated content.

#### 3.2.2 Cultural Event Integration

- **FR-2.4**: The system shall integrate Sri Lankan cultural events and festivals into probability and statistics problems.
- **FR-2.5**: The system shall reference local measurements and contexts familiar to Sri Lankan students.

### 3.3 Adaptive Learning System

#### 3.3.1 Student Profiling

- **FR-3.1**: The system shall classify and adapt to three visual impairment profiles:
  - Congenital blindness: Audio-centric navigation
  - Acquired blindness: Graduated spatial memory training
  - Low vision: High-contrast auditory highlighting
- **FR-3.2**: The system shall track and update student profiles based on performance and interaction patterns.

#### 3.3.2 Learning Path Generation

- **FR-3.3**: The system shall track 42 learning objectives from Grade 7-9 curricula using Education Ministry benchmarks.
- **FR-3.4**: The system shall dynamically adjust content difficulty based on Bloom's Taxonomy levels.
- **FR-3.5**: The system shall modify audio explanation depth based on student needs and performance.
- **FR-3.6**: The system shall adjust concept reinforcement frequency for optimal learning.

### 3.4 Feedback System

#### 3.4.1 Error Analysis

- **FR-4.1**: The system shall identify 19 common mathematical error types (e.g., sign reversal in ඍණ සංඛ්යා/negative numbers).
- **FR-4.2**: The system shall provide conceptual corrections for identified errors.
- **FR-4.3**: The system shall generate procedural guidance for error resolution.

#### 3.4.2 Emotion-Aware Interaction

- **FR-4.4**: The system shall detect learner frustration through voice analysis with 88% accuracy.
- **FR-4.5**: The system shall adapt pacing based on detected emotional states.
- **FR-4.6**: The system shall provide encouraging feedback for sustained engagement.

#### 3.4.3 Progress Tracking

- **FR-4.7**: The system shall generate biweekly progress reports highlighting topic-specific improvements.
- **FR-4.8**: The system shall identify areas requiring additional attention.

### 3.5 Accessibility Features

#### 3.5.1 Audio Interface

- **FR-5.1**: The system shall provide spoken instructions and feedback in Sinhala.
- **FR-5.2**: The system shall support keyboard navigation with audio confirmation.
- **FR-5.3**: The system shall include audio cues for all interactive elements.

#### 3.5.2 Braille Compatibility

- **FR-5.4**: The system shall generate content compatible with standard Braille displays.
- **FR-5.5**: The system shall export learning materials in Braille-ready formats.

## 4. Non-Functional Requirements

### 4.1 Performance

- **NFR-1.1**: The system shall provide real-time feedback with response times under 2 seconds.
- **NFR-1.2**: The system shall support concurrent usage by at least 30 students without performance degradation.
- **NFR-1.3**: The system shall function on computers with minimum specifications equivalent to:
  - Intel i3 processor or equivalent
  - 4GB RAM
  - 5GB available storage

### 4.2 Reliability

- **NFR-2.1**: The system shall maintain 99% uptime during school hours.
- **NFR-2.2**: The system shall include error recovery mechanisms to prevent data loss.
- **NFR-2.3**: The system shall perform automatic backups of student progress data.

### 4.3 Usability

- **NFR-3.1**: The system shall comply with WCAG 2.1 Level AA accessibility standards.
- **NFR-3.2**: First-time users shall be able to navigate the system successfully with minimal guidance.
- **NFR-3.3**: The system shall provide clear audio instructions for all functions.

### 4.4 Security and Privacy

- **NFR-4.1**: The system shall implement end-to-end encryption for student audio data.
- **NFR-4.2**: The system shall comply with relevant data protection regulations.
- **NFR-4.3**: The system shall anonymize data used for system improvement.

### 4.5 Scalability

- **NFR-5.1**: The system shall be deployable across 3,500+ government schools with basic ICT infrastructure.
- **NFR-5.2**: The system architecture shall support future expansion to additional grade levels.
- **NFR-5.3**: The system shall allow for curriculum updates without major restructuring.

## 5. Technical Implementation

### 5.1 Phase 1: Core NLP Pipeline (6 Weeks)

- Fine-tune SinLingua models for mathematical syntax
- Develop hybrid tokenizer for Sinhala+MathML
- Record 200 hours of math-specific TTS data

### 5.2 Phase 2: Cultural Adaptation (4 Weeks)

- Annotate 5,000 localized problems from Agricultural Corpus
- Train models on Sinhala curriculum documents
- Implement metric conversion API for legacy content

### 5.3 Phase 3: Feedback Integration (3 Weeks)

- Deploy MediaPipe for audio stress analysis
- Build error pattern database using SinhalaBERT
- Develop teacher dashboard with Braille export

## 6. Ethical Considerations

- **EC-1**: Regular audits of rural/urban problem distribution to ensure fair representation
- **EC-2**: End-to-end encryption of student audio data to protect privacy
- **EC-3**: WCAG 2.1 compliant audio interfaces for maximum accessibility

## 7. Testing Requirements

### 7.1 Accessibility Testing

- **TR-1.1**: The system shall be tested with actual visually impaired students representing all three impairment categories.
- **TR-1.2**: The system shall be evaluated for compatibility with common screen readers and Braille displays.

### 7.2 Performance Testing

- **TR-2.1**: The system shall be tested under various network conditions to ensure functionality in rural areas.
- **TR-2.2**: The system shall be stress-tested with simulated concurrent users.

### 7.3 Educational Effectiveness

- **TR-3.1**: The system shall be evaluated against traditional teaching methods through controlled studies.
- **TR-3.2**: Student learning outcomes shall be measured pre- and post-implementation.

## 8. Required Datasets

| Component         | Primary Source                         | Secondary Source             |
| ----------------- | -------------------------------------- | ---------------------------- |
| Language Models   | UCSC Sinhala Corpus                    | LK NLP Repository            |
| Cultural Context  | Agricultural Development Board Reports | Jathika Pasala Curriculum    |
| Feedback Patterns | BYJU's Math Companion Logs             | SinLingua Error Corpus       |
| Adaptive Logic    | National Exam Archives                 | Student Performance Database |

## 9. Deployment Requirements

- **DR-1**: The system shall be deployable on standard school computers with minimal additional hardware.
- **DR-2**: The system shall be usable with standard headphones and keyboards.
- **DR-3**: The system shall include comprehensive teacher training materials.

## Appendix A: Glossary of Sinhala Mathematical Terms

- හරය (haraya) - denominator
- ලවය (lavaya) - numerator
- වර්ගමූලය (vargamūlaya) - square root
- සමීකරණය (samīkaraṇaya) - equation
- ත්‍රිකෝණය (trikōṇaya) - triangle
- වෘත්තය (vr̥ttaya) - circle
- ඍණ සංඛ්යා (r̥ṇa saṅkhyā) - negative numbers

## Appendix B: References

1. https://iesl.lk/SLEN/10/Matematics_Education.pdf
2. https://lknlp.github.io
3. https://www.byjusfutureschool.com/blog/how-real-time-feedback-can-help-in-real-time-learning/
4. https://irjiet.com/common_src/article_file/1698327680_5f7630ec4b_7_irjiet.pdf
