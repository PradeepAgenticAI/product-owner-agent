# Product Owner Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered assistant that helps product owners manage documentation, answer questions, and maintain alignment between business goals and technical implementation.

## 🌟 Features

- **Documentation Retrieval**: Quickly find relevant information from your product documentation
- **Context-Aware Responses**: Get answers that consider the full context of your product
- **Evaluation Framework**: Test the agent's accuracy against a golden dataset
- **Extensible Architecture**: Add new specialized agents as needed

## 📋 Requirements

- Python 3.8+
- OpenAI API key

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/PradeepAgenticAI/product-owner-agent
cd product-owner-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your environment

Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your-openai-api-key-here
LLM_MODEL=gpt-4
VERBOSE=False
SHOW_TIMING=True
```

### 4. Process your documentation

```bash
python ingestion.py
```

### 5. Start the interactive chat

```bash
python main.py
```

## 📚 Documentation Structure

Place your product documentation in the `docs/` directory. The system comes with example documentation:

- `00_vision_and_strategy.md`: Product vision and strategic goals
- `01_roadmap.md`: Product roadmap with milestones
- `02_teams_and_allocation.md`: Team structure and resource allocation
- `03_architecture_and_principles.md`: System architecture and design principles
- `04_feature_blueprints_from_slueth.md`: Implementation of Sleuth's deployment principles
- `05_accelerate_devops_principles.md`: Key principles from "Accelerate: The Science of Lean Software and DevOps"

## 🧪 Evaluation

Test the agent's accuracy with the evaluation script:

```bash
python evaluation.py
```

The script uses the `evaluation_dataset.json` file as a golden dataset for testing.

## 🏗️ Project Structure

```
/product-owner-agent
|-- docs/                 # Documentation files
|-- vectorstore/          # Vector embeddings (created during ingestion)
|-- agents/               # Specialized agents
|   |-- __init__.py
|   |-- docs_retriever_agent.py
|-- main.py               # Interactive chat application
|-- ingestion.py          # Documentation processing script
|-- evaluation.py         # Evaluation script
|-- evaluation_dataset.json # Test dataset
|-- requirements.txt      # Project dependencies
|-- .env                  # Environment variables
```

## 🔧 Customization

### Adding New Documentation

1. Add your markdown or text files to the `docs/` directory
2. Run `python ingestion.py` to process the new files

### Creating New Specialized Agents

1. Create a new agent file in the `agents/` directory
2. Implement the agent interface
3. Import and use the agent in `main.py`

## 📊 Performance Considerations

- For large documentation sets, consider increasing chunk size in `ingestion.py`
- Adjust the number of retrieved documents in `docs_retriever_agent.py` for better precision/recall balance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) for the document processing and retrieval framework
- [OpenAI](https://openai.com/) for the language model API
- [Chroma](https://www.trychroma.com/) for the vector database
