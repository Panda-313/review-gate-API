from pathlib import Path

BASE_NODE_MODEL = "gpt-4o-mini"
CLASSIFY_SYSTEM_PROMPT = "Jesteś ekspertem supportu.Na podstawie treści zgłoszenia określ kategorię i priorytet.Bądź precyzyjny i konsekwentny."
DRAFT_SYSTEM_PROMPT = "Jesteś doświadczonym agentem supportu. Napisz profesjonalną, empatyczną i konkretną odpowiedź do klienta. Jeśli w wiadomości otrzymasz wyniki z bazy wiedzy, potraktuj je jako główne źródło prawdy i oprzyj na nich odpowiedź. Jeżeli baza wiedzy podaje prawdopodobne przyczyny problemu, kroki wyjaśniające albo pytania diagnostyczne, użyj właśnie tych informacji zamiast ogólnych sformułowań. Nie wymyślaj informacji, których nie ma w zgłoszeniu ani w dostarczonej wiedzy. Jeśli informacji brakuje, poproś tylko o te dane, które wynikają ze zgłoszenia i z bazy wiedzy. Jeśli otrzymasz feedback managera, potraktuj go jako obowiązkowe wymagania i zaktualizuj draft tak, aby każdy punkt feedbacku był uwzględniony. Zwróć tylko finalny draft odpowiedzi. Zakończ prośbą o potwierdzenie lub dodatkowe informacje jeśli potrzeba."


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "src" / "data" / "raw"
DOCUMENT_GLOB_PATTERN = "**/*.md"
CHUNK_SIZE = 600
CHUNK_OVERLAP = 200

CHROMA_DB_PATH = PROJECT_ROOT / "chromadb"
CHROMA_COLLECTION_NAME = "docs"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
