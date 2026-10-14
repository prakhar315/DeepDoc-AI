import React, { useRef, useState } from 'react';
import {
  deleteDocument,
  getFullDocument,
  searchDocuments,
  uploadFile,
  uploadText,
} from './services/api';

const departments = ['HR', 'IT', 'Finance', 'Support'];

function App() {
  const [query, setQuery] = useState('');
  const [searchDepartment, setSearchDepartment] = useState('All');
  const [results, setResults] = useState([]);
  const [searchState, setSearchState] = useState({ loading: false, error: '' });
  const [docText, setDocText] = useState('');
  const [docTitle, setDocTitle] = useState('');
  const [docDepartment, setDocDepartment] = useState('HR');
  const [file, setFile] = useState(null);
  const [uploadState, setUploadState] = useState({ loading: false, message: '', error: '' });
  const [document, setDocument] = useState(null);
  const fileInput = useRef(null);

  const handleSearch = async (event) => {
    event?.preventDefault();
    if (!query.trim()) {
      setSearchState({ loading: false, error: 'Enter a question to search.' });
      return;
    }
    setSearchState({ loading: true, error: '' });
    try {
      const response = await searchDocuments({
        query: query.trim(),
        top_k: 5,
        department: searchDepartment === 'All' ? '' : searchDepartment,
      });
      setResults(response.data);
    } catch (error) {
      setSearchState({
        loading: false,
        error: error.response?.data?.detail || 'Search failed. Check the backend connection.',
      });
      return;
    }
    setSearchState({ loading: false, error: '' });
  };

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!file && !docText.trim()) {
      setUploadState({ loading: false, message: '', error: 'Provide document text or choose a PDF/DOCX file.' });
      return;
    }
    setUploadState({ loading: true, message: '', error: '' });
    try {
      const response = file
        ? await uploadFile(file, docDepartment, docTitle)
        : await uploadText({
            text: docText.trim(),
            metadata: { department: docDepartment, ...(docTitle.trim() && { title: docTitle.trim() }) },
          });
      setUploadState({ loading: false, message: response.data.message, error: '' });
      setDocText('');
      setDocTitle('');
      setFile(null);
      if (fileInput.current) fileInput.current.value = '';
    } catch (error) {
      setUploadState({
        loading: false,
        message: '',
        error: error.response?.data?.detail || 'Upload failed. Check the backend connection.',
      });
    }
  };

  const showDocument = async (metadata) => {
    try {
      const response = await getFullDocument(metadata.doc_id);
      setDocument({
        ...response.data,
        title: metadata.title || metadata.source || 'Untitled document',
      });
    } catch (error) {
      setSearchState({
        loading: false,
        error: error.response?.data?.detail || 'Unable to load the full document.',
      });
    }
  };

  const removeDocument = async () => {
    if (!document || !window.confirm(`Delete "${document.title}"?`)) return;
    try {
      await deleteDocument(document.doc_id);
      setResults((current) => current.filter((result) => result.metadata?.doc_id !== document.doc_id));
      setDocument(null);
    } catch (error) {
      setSearchState({
        loading: false,
        error: error.response?.data?.detail || 'Unable to delete the document.',
      });
    }
  };

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">INTELLIGENT DOCUMENT WORKSPACE</p>
          <h1>DeepDoc <span>AI</span></h1>
          <p className="tagline">Find the right knowledge in seconds.</p>
        </div>
        <div className="status-pill"><i /> Semantic search online</div>
      </header>

      <main className="workspace">
        <section className="panel search-panel">
          <div className="panel-heading">
            <div><p className="eyebrow">01 / DISCOVER</p><h2>Ask your documents</h2></div>
            <span className="count-badge">{results.length} results</span>
          </div>
          <form onSubmit={handleSearch} className="search-form">
            <label htmlFor="query">Natural-language question</label>
            <div className="search-row">
              <input id="query" value={query} onChange={(event) => setQuery(event.target.value)}
                placeholder="How do I reset my password?" />
              <select value={searchDepartment} onChange={(event) => setSearchDepartment(event.target.value)} aria-label="Filter by department">
                <option>All</option>
                {departments.map((department) => <option key={department}>{department}</option>)}
              </select>
              <button disabled={searchState.loading}>{searchState.loading ? 'Searching…' : 'Search'}</button>
            </div>
          </form>
          {searchState.error && <p className="message error">{searchState.error}</p>}
          {!searchState.error && !results.length && <div className="empty-state"><strong>No results yet</strong><span>Search across your indexed documents or upload a new one.</span></div>}
          <div className="results-list">
            {results.map((result, index) => (
              <article className="result-card" key={result.id}>
                <div className="result-number">0{index + 1}</div>
                <div className="result-body">
                  <div className="result-meta"><span>{result.metadata?.department || 'General'}</span><small>Match {result.score.toFixed(2)}</small></div>
                  <p>{result.text}</p>
                  <button className="text-button" onClick={() => showDocument(result.metadata)}>Open full document →</button>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="panel upload-panel">
          <div className="panel-heading"><div><p className="eyebrow">02 / INGEST</p><h2>Add knowledge</h2></div></div>
          <form onSubmit={handleUpload} className="upload-form">
            <label htmlFor="title">Document title <em>optional</em></label>
            <input id="title" value={docTitle} onChange={(event) => setDocTitle(event.target.value)} placeholder="e.g. VPN setup guide" />
            <label htmlFor="text">Paste content</label>
            <textarea id="text" rows="7" value={docText} disabled={Boolean(file)}
              onChange={(event) => setDocText(event.target.value)} placeholder="Paste document text here…" />
            <div className="or-divider"><span>or upload a file</span></div>
            <input ref={fileInput} type="file" accept=".pdf,.docx" disabled={Boolean(docText.trim())}
              onChange={(event) => setFile(event.target.files?.[0] || null)} />
            <div className="upload-footer">
              <select value={docDepartment} onChange={(event) => setDocDepartment(event.target.value)} aria-label="Document department">
                {departments.map((department) => <option key={department}>{department}</option>)}
              </select>
              <button disabled={uploadState.loading}>{uploadState.loading ? 'Indexing…' : 'Upload & index'}</button>
            </div>
          </form>
          {uploadState.message && <p className="message success">{uploadState.message}</p>}
          {uploadState.error && <p className="message error">{uploadState.error}</p>}
          <div className="hint"><span>✦</span> Documents are chunked and semantically indexed for faster discovery.</div>
        </section>
      </main>

      {document && <div className="modal-backdrop" onClick={() => setDocument(null)}>
        <section className="document-modal" role="dialog" aria-modal="true" onClick={(event) => event.stopPropagation()}>
          <div className="modal-heading"><div><p className="eyebrow">DOCUMENT VIEW</p><h2>{document.title}</h2></div><button className="close-button" onClick={() => setDocument(null)}>×</button></div>
          <div className="document-text">{document.text}</div>
          <div className="modal-actions"><button className="secondary-button" onClick={() => setDocument(null)}>Close</button><button className="danger-button" onClick={removeDocument}>Delete document</button></div>
        </section>
      </div>}
    </div>
  );
}

export default App;
