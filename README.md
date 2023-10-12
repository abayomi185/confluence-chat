# Confluence Chat

Create `.env` from `env_example`
```
cp env_example .env
```

Install dependencies
```bash
yarn install
# Make sure to create a virtual environment for python
pip install -r requirements.txt
```

Download Confluence pages
```
python scripts/get_confluence_pages.py
```

Set up ChromaDB
This needs to be set up separately due to the structure of the ChromaDB project. It also uses Docker.
```
git clone git@github.com:chroma-core/chroma.git
cd chroma
sudo docker compose up -d --build
```

Load documents into ChromaDB
```
python scripts/load_documents_into_chroma.py
```

Run Dev server
```
turbo dev
```
