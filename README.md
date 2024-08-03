# OpenPerPlex

OpenPerPlex is an open-source AI search engine that leverages cutting-edge technologies to provide search capabilities over the web.

## front end app (vuejs)

- `https://github.com/YassKhazzan/openperplex_front.git`

## 🌟 Features

- Semantic chunking using Cohere and semantic-chunkers library (`https://github.com/aurelio-labs/semantic-chunkers/blob/main/semantic_chunkers/chunkers/statistical.py`)
- Reranking results with JINA API
- Google search integration via serper.dev
- Groq as the inference engine
- Llama 3 70B MODEL

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone the repository:
 git clone [https://github.com/YassKhazzan/openperplex_backend_os.git](https://github.com/YassKhazzan/openperplex_backend_os.git) 
2. Install the required packages: `pip install -r requirements.txt`
3. Set up your environment variables:
- Copy the `.env_example` file to `.env`
- Fill in your API keys in the `.env` file

### Running the Project

To start the OpenPerPlex server: ```uvicorn main:app --port 8000```

The server will be available at `http://localhost:8000`

## 🔧 Configuration

Make sure to set up your `.env` file with the necessary API keys:

- COHERE_API_KEY
- JINA_API_KEY
- SERPER_API_KEY
- GROQ_API_KEY

## 🤝 Contributing

We welcome contributions to OpenPerPlex! Please feel free to submit issues, fork the repository and send pull requests!

## 📝 License

This project is licensed under the [MIT License](LICENSE).

## 🙏 Acknowledgements

- [Cohere](https://cohere.ai/) for semantic chunking
- [JINA AI](https://jina.ai/) for reranking
- [serper.dev](https://serper.dev/) for Google search integration
- [Groq](https://groq.com/) for inference engine
- [META](https://www.meta.ai/) opensource models

## 📬 Contact

For any questions or feedback, please open an issue on this repository or contact me on [X](https://x.com/KhazzanYassine)     

---

Happy searching with OpenPerPlex! 🚀🔍
