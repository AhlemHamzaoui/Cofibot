# 🤖 CofiBot — Intelligent Energy & Production Assistant (Backend + NLP)

CofiBot is an **AI-powered assistant** developed for the **Energy Department at Coficab**.  
It allows managers and administrators to **query energy consumption and production metrics** using **natural language**, supported by a **Retrieval-Augmented Generation (RAG)** architecture.

This repository contains the **backend API**, **RAG pipeline**, and **local LLM integration**.

---

## 🧠 Key Features

- **Chat in natural language** to retrieve insights
- **Local, secure inference** using `llama3.2:3b` with **Ollama**
- **RAG (Retrieval-Augmented Generation)** to ground answers in internal data
- **Data analytics queries** based on:
  - Machines
  - Production lines
  - Cable / product batches
  - Time intervals
- **No external internet-dependent processing**

---

## 🏗️ System Architecture (Backend Only)

| Layer | Technology | Purpose |
|------|------------|---------|
| **Local LLM** | Ollama (`llama3.2:3b`) | Generates responses |
| **RAG Engine** | Embeddings + Vector Search | Ensures factual answers |
| **Backend API** | FastAPI | Manages requests and data processing |
| **Data Layer** | CSV or PostgreSQL | Stores machine & production records |

---

## 📊 Data Structure

### **1. Machines Data**
| Column | Description |
|-------|-------------|
| `id_machine` | Unique machine ID |
| `idligne` | Production line number |
| `type_energie` | Energy type (e.g., electricity) |
| `consommation` | Energy consumption value |

### **2. Production Data**
| Column | Description |
|-------|-------------|
| `serial_number` | Batch identifier |
| `item_name` | Cable/product name |
| `quantity`, `kg`, `duration` | Production performance metrics |
| `start_date`, `end_date` | Production period |
| `idligne` | Related production line |

### **3. Billing Data (optional)**
For **cost estimation** and **efficiency KPIs**.

---

## 🚀 How to Run

### 1. Start Local Model (Ollama)
```bash
ollama run llama3:3.2b
