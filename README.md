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
* 12240340 - ISE - Tselmuun

### Team Roles & Responsibilities
<img width="2460" height="830" alt="Role-Sheet" src="https://github.com/user-attachments/assets/ac4f0eac-29b0-491c-8f38-b7d1504ad06b" />

### Presentation Order
1. N2 - Code-Switched Voice Agent - Team 4
2. **C1 - Visual Document Understanding - Team 2**
3. C2b - Video Translation and Dubbing - Team 1
4. S1 - Case Study and Portfolio Generator - Team 5
5. S2 - Personalized Learning Roadmap - Team 3

# FRD Section

| Requirement ID | Related DoD | Tier | Description |
|---|---|---|---|
| FR-01 | DoD-01 | Baseline | The system shall extract text from real-estate documents. |
| FR-02 | DoD-02 | Baseline | The system shall process documents containing tables. |
| FR-03 | DoD-03 | Target | The system shall process handwritten content. |
