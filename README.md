# VLM/OCR based Document Processing 
## Project Overview
### Problem
Based on the workflows and systems used by real estate agencies, there are several areas where they may be losing potential customers or failing to maximize their income:

1. The information as rental house location, room pictures are saved in Google Drive alike clouds. It has to manually updated or deleted if it gets Occupied.
2. In official Contract document, mostly is written that Customer has to write 1-2 months before about moving out. 
3. Preferences of Owners that rent the house, and Customers are mostly written on paper and thrown away. Possible crucial information is thrown when reaching again to offer new options or continuing living in same house.
4. If real-estate is growing and has more customers, no official website with AI Q/A based on database with FAQ that could potentially increase word of mouth.
### Target users
Real estate agencies that still rely on manual or fragmented systems for managing, processing, and retrieving information from business documents.
### Solution
By identifying the actual audience experiencing these problems, we can see clear opportunities for applying NLP, RAG, and VLM technologies. However, in accordance with the C1 project’s requirements, we will first focus on:

- Make analysis between OCR & VLM pipeline performance.
- Test on PDF, Scans, text, handwritten, mixed-format.
    - Contract between Customer & House Owner.
    - Building related documents from House owner.
    - Customer ID, passport.
    - Deposit Payment, First Rent payment, Brokerage-fee receipts
    - Relevant information, scribbled on notes.
    - Maintenance invoices, utility bills
- Optimize the software for specific documents types using OCR, VLM and if time constraint allows - make the Hybrid.

## Team

**Team 2**

### Team members
6 members: 
* 12230270 - IBT - Dilnozakhon 
* 12230336 - IBT - Jasmina
* 12235569 - IBT - Shukarna
* 12235639 - ISE - Ozodbek
* 12235608 - ISE - Daesan
* 12230340 - ISE - Tselmuun

### Team Roles & Responsibilities
<img width="2460" height="830" alt="Role-Sheet" src="https://github.com/user-attachments/assets/ac4f0eac-29b0-491c-8f38-b7d1504ad06b" />

### Presentation Order
1. N2 - Code-Switched Voice Agent - Team 4
2. **C1 - Visual Document Understanding - Team 2**
3. C2b - Video Translation and Dubbing - Team 1
4. S1 - Case Study and Portfolio Generator - Team 5
5. S2 - Personalized Learning Roadmap - Team 3

---

## Architecture & Technical Spec-s

### C4 Model
Level 1

<img width="822" height="311" alt="Team2_VDU_C1" src="https://github.com/user-attachments/assets/19168cec-2a32-40ee-9e03-60447334aeee" />

Level 2

<img width="1170" height="2080" alt="이미지" src="https://github.com/user-attachments/assets/d10c4c6a-e06d-413a-a66e-6ae1aaf38fab" />

### Data Source
Document Types
| Document Type | What We Test |
|---|---| 
| Rental contract | Text + layout + relationships | 
| Receipt | Text + tables | 
| Bank transfer record | Text + relationships | 
| Property information  | Text + tables + relationships | 
| Handwritten notes | Handwriting |
| Hybrid | Text + handwriting |

Potential Dataset Sources
- SROIE - https://www.kaggle.com/datasets/urbikn/sroie-datasetv2
- FUNSD - https://benlee73.tistory.com/21
- AI hub Korean handwriting Dataset - https://aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=81
- Actual document template with generated data / manually written (several samples)

Difficulty
- Finding enough datasets on Korean Language for similar documents that Real Estate Agencies rely on. 

### FRD
| Requirement ID | Related DoD | Tier | Description | Check Method | Questions |
|---|---|---|---|---|---|
| FR-01 | DoD-01 | Baseline | Extracts specified fields from document images, or answers questions about them. | Select fields & ask related questions. | |
| FR-02 | DoD-02 | Baseline | System should process documents containing tables. | Take invoices and ask relational questions to see if it sees the relations. | |
| FR-03 | DoD-03 | Baseline | System should process handwritten documents. | Test handwritten documents and check if it extracts the information correctly. | |
| FR-04 | DoD-04 | Target | Accuracy report per document type. | We will check against ground-checked datasets. | |

### Test plan

**Success criteria**
* Meet the baseline and target DoD requirements.
- Process the selected document types for above 80% accuracy. 
- Identify and categorize pipeline failures.

**Test method**
- Upload 30 documents covering plain text, tables, charts, handwriting, and different formatting.

**We should be able to answer for these questions:**
- if we put X document type, what pipeline does it the best?
- what makes the inefficient pipeline - inefficient?
