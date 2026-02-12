import { useState, useEffect, createContext, useContext, useCallback, useRef } from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useParams, useSearchParams, useLocation } from "react-router-dom";
import axios from "axios";
import mermaid from "mermaid";
import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";
import "@/App.css";

mermaid.initialize({ startOnLoad: false, theme: "dark", themeVariables: { primaryColor: "#4f46e5", primaryBorderColor: "#6366f1", primaryTextColor: "#e4e4e7", lineColor: "#71717a", secondaryColor: "#27272a", tertiaryColor: "#18181b", background: "#18181b", mainBkg: "#27272a", nodeBorder: "#6366f1", clusterBkg: "#1a1a2e", titleColor: "#e4e4e7" } });

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

// --- Contexts ---
const AuthContext = createContext(null);
const ThemeContext = createContext(null);
export const useAuth = () => useContext(AuthContext);
export const useTheme = () => useContext(ThemeContext);

function ThemeProvider({ children }) {
  const [dark, setDark] = useState(() => {
    const saved = localStorage.getItem("edh-theme");
    return saved ? saved === "dark" : true;
  });
  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
    localStorage.setItem("edh-theme", dark ? "dark" : "light");
  }, [dark]);
  return <ThemeContext.Provider value={{ dark, toggle: () => setDark(d => !d) }}>{children}</ThemeContext.Provider>;
}

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const api = useCallback(async (method, url, data) => {
    return axios({ method, url: `${API}${url}`, data, withCredentials: true });
  }, []);

  const checkAuth = useCallback(async () => {
    try {
      const r = await axios.get(`${API}/auth/me`, { withCredentials: true });
      setUser(r.data);
    } catch {
      setUser(null);
    }
    setLoading(false);
  }, []);

  useEffect(() => { checkAuth(); }, [checkAuth]);

  const logout = async () => {
    try { await axios.post(`${API}/auth/logout`, {}, { withCredentials: true }); } catch {}
    setUser(null);
  };

  return <AuthContext.Provider value={{ user, loading, api, logout, checkAuth, setUser }}>{children}</AuthContext.Provider>;
}

// REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
function AuthCallback() {
  const navigate = useNavigate();
  const hasProcessed = useRef(false);

  useEffect(() => {
    if (hasProcessed.current) return;
    hasProcessed.current = true;
    const hash = window.location.hash;
    const match = hash.match(/session_id=([^&]+)/);
    if (!match) { navigate("/login"); return; }
    const sessionId = match[1];
    axios.post(`${API}/auth/session`, { session_id: sessionId }, { withCredentials: true })
      .then(r => {
        window.location.replace("/");
      })
      .catch(() => navigate("/login"));
  }, [navigate]);

  return <div className="edh-loading"><div className="edh-spinner" /></div>;
}

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="edh-loading"><div className="edh-spinner" /></div>;
  return user ? children : <Navigate to="/login" />;
}

// --- Login Page ---
function LoginPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  useEffect(() => { if (user) navigate("/"); }, [user, navigate]);

  // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
  const handleGoogleLogin = () => {
    const redirectUrl = window.location.origin + '/';
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  return (
    <div className="auth-page" data-testid="auth-page">
      <div className="auth-left">
        <div className="auth-brand">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><polygon points="16,2 30,28 2,28" stroke="currentColor" strokeWidth="2" fill="none"/><circle cx="16" cy="18" r="4" fill="currentColor"/></svg>
          <span>Emergent Knowledge Hub</span>
        </div>
        <div className="auth-tagline">Your AI knowledge base.<br/>Organized. Searchable. Beautiful.</div>
      </div>
      <div className="auth-right">
        <div className="auth-form" data-testid="auth-form">
          <h2>Welcome</h2>
          <p className="auth-sub">Sign in to access the documentation hub</p>
          <button data-testid="google-login-btn" className="google-login-btn" onClick={handleGoogleLogin}>
            <svg width="18" height="18" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
            Sign in with Google
          </button>
          <p className="auth-note">Admin: chethan@emergent.sh</p>
        </div>
      </div>
    </div>
  );
}

// --- Icon component ---
function Icon({ name, size = 18 }) {
  const icons = {
    Layers: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/></svg>,
    Cpu: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>,
    Server: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="20" height="8" x="2" y="2" rx="2"/><rect width="20" height="8" x="2" y="14" rx="2"/><line x1="6" x2="6.01" y1="6" y2="6"/><line x1="6" x2="6.01" y1="18" y2="18"/></svg>,
    Monitor: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/></svg>,
    Database: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg>,
    Rocket: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/></svg>,
    Lock: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="11" x="3" y="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>,
    FolderOpen: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m6 14 1.5-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.54 6a2 2 0 0 1-1.95 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2"/></svg>,
    Sparkles: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/></svg>,
    Telescope: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m10.065 12.493-6.18 1.318a.934.934 0 0 1-1.108-.702l-.537-2.15a1.07 1.07 0 0 1 .691-1.265l13.504-4.44"/><path d="m13.56 11.747 4.332-.924"/><path d="m16 21-3.105-6.21"/><path d="m16.485 5.94 3.105 6.21"/><circle cx="12" cy="19" r="2"/></svg>,
    FileText: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>,
    ChevronRight: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m9 18 6-6-6-6"/></svg>,
    ChevronDown: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m6 9 6 6 6-6"/></svg>,
    Search: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>,
    Bookmark: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg>,
    BookmarkFilled: <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/></svg>,
    Sun: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>,
    Moon: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>,
    Plus: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14"/><path d="M12 5v14"/></svg>,
    LogOut: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/></svg>,
    Edit: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/></svg>,
    Trash: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>,
    X: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>,
    ArrowLeft: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 19-7-7 7-7"/><path d="M19 12H5"/></svg>,
    Home: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>,
    Copy: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>,
    Check: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20 6 9 17l-5-5"/></svg>,
    PanelLeft: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/></svg>,
    Download: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>,
    Clock: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>,
    Tag: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/><circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/></svg>,
    Share: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" x2="15.42" y1="13.51" y2="17.49"/><line x1="15.41" x2="8.59" y1="6.51" y2="10.49"/></svg>,
    MessageSquare: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>,
    ThumbsUp: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M7 10v12"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2h0a3.13 3.13 0 0 1 3 3.88Z"/></svg>,
    Reply: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="9 17 4 12 9 7"/><path d="M20 18v-2a4 4 0 0 0-4-4H4"/></svg>,
    Maximize: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3"/><path d="M21 8V5a2 2 0 0 0-2-2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/><path d="M16 21h3a2 2 0 0 0 2-2v-3"/></svg>,
    Undo: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 7v6h6"/><path d="M21 17a9 9 0 0 0-9-9 9 9 0 0 0-6 2.3L3 13"/></svg>,
    Link: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>,
    Menu: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>,
  };
  return icons[name] || icons.FileText;
}

// --- Markdown Renderer ---
function MarkdownContent({ content }) {
  if (!content) return null;
  const lines = content.split("\n");
  const elements = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (line.startsWith("```")) {
      const lang = line.slice(3).trim();
      const codeLines = [];
      i++;
      while (i < lines.length && !lines[i].startsWith("```")) { codeLines.push(lines[i]); i++; }
      i++;
      if (lang === "mermaid") {
        elements.push(<MermaidDiagram key={elements.length} chart={codeLines.join("\n")} />);
      } else {
        elements.push(<CodeBlock key={elements.length} code={codeLines.join("\n")} lang={lang} />);
      }
      continue;
    }
    if (line.startsWith("# ")) { i++; continue; }
    if (line.startsWith("## ")) { elements.push(<h2 key={elements.length} className="doc-h2" id={line.slice(3).toLowerCase().replace(/[^a-z0-9]+/g,"-")}>{line.slice(3)}</h2>); i++; continue; }
    if (line.startsWith("### ")) { elements.push(<h3 key={elements.length} className="doc-h3">{line.slice(4)}</h3>); i++; continue; }
    if (line.includes("|") && lines[i+1]?.includes("---")) {
      const headers = line.split("|").map(c=>c.trim()).filter(Boolean);
      i += 2;
      const rows = [];
      while (i < lines.length && lines[i].includes("|")) { rows.push(lines[i].split("|").map(c=>c.trim()).filter(Boolean)); i++; }
      elements.push(
        <div key={elements.length} className="doc-table-wrap">
          <table className="doc-table"><thead><tr>{headers.map((h,j) => <th key={j} dangerouslySetInnerHTML={{__html: renderInlineHtml(h)}} />)}</tr></thead>
          <tbody>{rows.map((r,j) => <tr key={j}>{r.map((c,k) => <td key={k} dangerouslySetInnerHTML={{__html: renderInlineHtml(c)}} />)}</tr>)}</tbody></table>
        </div>
      );
      continue;
    }
    if (line.startsWith("- ")) {
      const items = [];
      while (i < lines.length && lines[i].startsWith("- ")) { items.push(lines[i].slice(2)); i++; }
      elements.push(<ul key={elements.length} className="doc-ul">{items.map((item, j) => <li key={j}>{renderInline(item)}</li>)}</ul>);
      continue;
    }
    if (/^\d+\.\s/.test(line)) {
      const items = [];
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) { items.push(lines[i].replace(/^\d+\.\s/, "")); i++; }
      elements.push(<ol key={elements.length} className="doc-ol">{items.map((item, j) => <li key={j}>{renderInline(item)}</li>)}</ol>);
      continue;
    }
    if (!line.trim()) { i++; continue; }
    elements.push(<p key={elements.length} className="doc-p">{renderInline(line)}</p>);
    i++;
  }
  return <>{elements}</>;
}

function renderInlineHtml(text) {
  if (!text) return "";
  return text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/`([^`]+)`/g, '<code class="doc-inline-code">$1</code>').replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="doc-link" target="_blank" rel="noreferrer">$1</a>');
}

function renderInline(text) {
  if (!text) return text;
  const parts = [];
  let remaining = text;
  let key = 0;
  while (remaining.length > 0) {
    const boldMatch = remaining.match(/\*\*(.+?)\*\*/);
    const codeMatch = remaining.match(/`([^`]+)`/);
    const linkMatch = remaining.match(/\[([^\]]+)\]\(([^)]+)\)/);
    let earliest = null;
    let earliestIdx = remaining.length;
    if (boldMatch && boldMatch.index < earliestIdx) { earliest = "bold"; earliestIdx = boldMatch.index; }
    if (codeMatch && codeMatch.index < earliestIdx) { earliest = "code"; earliestIdx = codeMatch.index; }
    if (linkMatch && linkMatch.index < earliestIdx) { earliest = "link"; earliestIdx = linkMatch.index; }
    if (!earliest) { parts.push(remaining); break; }
    if (earliestIdx > 0) parts.push(remaining.slice(0, earliestIdx));
    if (earliest === "bold") { parts.push(<strong key={key++}>{boldMatch[1]}</strong>); remaining = remaining.slice(earliestIdx + boldMatch[0].length); }
    else if (earliest === "code") { parts.push(<code key={key++} className="doc-inline-code">{codeMatch[1]}</code>); remaining = remaining.slice(earliestIdx + codeMatch[0].length); }
    else if (earliest === "link") { parts.push(<a key={key++} href={linkMatch[2]} className="doc-link" target="_blank" rel="noreferrer">{linkMatch[1]}</a>); remaining = remaining.slice(earliestIdx + linkMatch[0].length); }
  }
  return parts;
}

function MermaidDiagram({ chart }) {
  const ref = useRef(null);
  const [svg, setSvg] = useState("");
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState(false);
  const { dark } = useTheme();

  useEffect(() => {
    const render = async () => {
      try {
        const themeVars = dark
          ? { primaryColor: "#4f46e5", primaryBorderColor: "#6366f1", primaryTextColor: "#e4e4e7", lineColor: "#71717a", secondaryColor: "#27272a", tertiaryColor: "#18181b", background: "transparent", mainBkg: "#27272a", nodeBorder: "#6366f1", clusterBkg: "#1a1a2e", titleColor: "#e4e4e7", edgeLabelBackground: "#18181b", nodeTextColor: "#e4e4e7" }
          : { primaryColor: "#4f46e5", primaryBorderColor: "#6366f1", background: "transparent", mainBkg: "#eef2ff", nodeBorder: "#6366f1", edgeLabelBackground: "#ffffff" };
        mermaid.initialize({ startOnLoad: false, theme: dark ? "dark" : "default", themeVariables: themeVars });
        const id = `mermaid-${Math.random().toString(36).slice(2, 9)}`;
        const { svg: renderedSvg } = await mermaid.render(id, chart.trim());
        setSvg(renderedSvg); setError(null);
      } catch (e) { setError(e.message); }
    };
    render();
  }, [chart, dark]);

  useEffect(() => {
    const handler = (e) => { if (e.key === "Escape" && expanded) setExpanded(false); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [expanded]);

  if (error) return <div className="doc-codeblock"><div className="doc-codeblock-header"><span>mermaid (render error)</span></div><pre><code>{chart}</code></pre></div>;

  return (
    <>
      <div ref={ref} className="mermaid-diagram" data-testid="mermaid-diagram">
        <div dangerouslySetInnerHTML={{ __html: svg }} />
        <button className="mermaid-expand-btn" data-testid="mermaid-expand-btn" onClick={() => setExpanded(true)} title="Expand diagram"><Icon name="Maximize" size={16}/></button>
      </div>
      {expanded && (
        <div className="mermaid-modal" data-testid="mermaid-modal" onClick={() => setExpanded(false)}>
          <div className="mermaid-modal-content" onClick={e => e.stopPropagation()}>
            <button className="mermaid-modal-close" data-testid="mermaid-modal-close" onClick={() => setExpanded(false)}><Icon name="X" size={20}/> Close</button>
            <div className="mermaid-modal-svg" dangerouslySetInnerHTML={{ __html: svg }} />
          </div>
        </div>
      )}
    </>
  );
}

function CodeBlock({ code, lang }) {
  const [copied, setCopied] = useState(false);
  const copy = () => { navigator.clipboard.writeText(code); setCopied(true); setTimeout(() => setCopied(false), 2000); };
  return (
    <div className="doc-codeblock">
      <div className="doc-codeblock-header"><span>{lang || "text"}</span><button onClick={copy} data-testid="copy-code-btn" className="doc-copy-btn">{copied ? <Icon name="Check" size={14}/> : <Icon name="Copy" size={14}/>}{copied ? "Copied" : "Copy"}</button></div>
      <pre><code>{code}</code></pre>
    </div>
  );
}

// --- Inline Search (not modal) ---
function InlineSearch({ categories, onSelect }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [focused, setFocused] = useState(false);
  const { api } = useAuth();
  const timerRef = useRef(null);
  const wrapRef = useRef(null);

  useEffect(() => {
    const handler = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") { e.preventDefault(); wrapRef.current?.querySelector("input")?.focus(); }
      if (e.key === "Escape") { setQuery(""); setResults([]); wrapRef.current?.querySelector("input")?.blur(); }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  useEffect(() => {
    if (query.length < 1) { setResults([]); return; }
    clearTimeout(timerRef.current);
    timerRef.current = setTimeout(async () => {
      setSearching(true);
      try { const r = await api("get", `/search?q=${encodeURIComponent(query)}`); setResults(r.data); } catch {}
      setSearching(false);
    }, 200);
    return () => clearTimeout(timerRef.current);
  }, [query, api]);

  const getCatName = (id) => categories.find(c => c.id === id)?.name || "";

  return (
    <div className="inline-search" ref={wrapRef} data-testid="inline-search">
      <div className="inline-search-input">
        <Icon name="Search" size={15}/>
        <input data-testid="search-input" placeholder="Search..." value={query} onChange={e => setQuery(e.target.value)} onFocus={() => setFocused(true)} onBlur={() => setTimeout(() => setFocused(false), 200)} />
        {searching && <span className="search-spinner"/>}
        <kbd>Ctrl+K</kbd>
      </div>
      {focused && query.length >= 2 && (
        <div className="inline-search-dropdown" data-testid="search-results">
          {results.length > 0 ? results.map(d => (
            <button key={d.id} className="search-result-item" data-testid={`search-result-${d.id}`} onMouseDown={() => { onSelect(d.id); setQuery(""); }}>
              <Icon name="FileText" size={14}/>
              <div>
                <div className="search-result-title">{d.title}</div>
                <div className="search-result-cat">{getCatName(d.category_id)}</div>
                {d.snippet && <div className="search-result-snippet" data-testid="search-snippet">{d.snippet}</div>}
              </div>
            </button>
          )) : <div className="search-empty">No results found</div>}
        </div>
      )}
    </div>
  );
}

// --- Comments Section ---
function CommentsSection({ docId }) {
  const { api, user } = useAuth();
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [replyTo, setReplyTo] = useState(null);
  const [replyText, setReplyText] = useState("");

  useEffect(() => {
    if (!docId) return;
    api("get", `/documents/${docId}/comments`).then(r => setComments(r.data)).catch(() => {});
  }, [docId, api]);

  const submit = async (content, parentId = null) => {
    if (!content.trim()) return;
    try {
      const r = await api("post", `/documents/${docId}/comments`, { content, parent_id: parentId });
      setComments(prev => [...prev, r.data]);
      if (parentId) { setReplyTo(null); setReplyText(""); } else setNewComment("");
    } catch {}
  };

  const toggleUpvote = async (commentId) => {
    try {
      const r = await api("post", `/comments/${commentId}/upvote`);
      setComments(prev => prev.map(c => c.id === commentId ? { ...c, upvotes: r.data.upvotes } : c));
    } catch {}
  };

  const deleteComment = async (commentId) => {
    try {
      await api("delete", `/comments/${commentId}`);
      setComments(prev => prev.filter(c => c.id !== commentId && c.parent_id !== commentId));
    } catch {}
  };

  const topLevel = comments.filter(c => !c.parent_id);
  const getReplies = (parentId) => comments.filter(c => c.parent_id === parentId);

  const CommentItem = ({ comment, depth = 0 }) => {
    const replies = getReplies(comment.id);
    const isOwn = user?.user_id === comment.user_id;
    const upvoted = (comment.upvotes || []).includes(user?.user_id);
    return (
      <div className={`comment-item ${depth > 0 ? "comment-reply" : ""}`} data-testid={`comment-${comment.id}`}>
        <div className="comment-header">
          <div className="comment-avatar">{comment.user_name?.[0]?.toUpperCase() || "U"}</div>
          <span className="comment-author">{comment.user_name}</span>
          <span className="comment-time">{new Date(comment.created_at).toLocaleDateString()}</span>
        </div>
        <p className="comment-text">{comment.content}</p>
        <div className="comment-actions">
          <button className={`comment-action ${upvoted ? "upvoted" : ""}`} data-testid={`upvote-${comment.id}`} onClick={() => toggleUpvote(comment.id)}>
            <Icon name="ThumbsUp" size={13}/> {(comment.upvotes || []).length || ""}
          </button>
          <button className="comment-action" data-testid={`reply-btn-${comment.id}`} onClick={() => setReplyTo(replyTo === comment.id ? null : comment.id)}>
            <Icon name="Reply" size={13}/> Reply
          </button>
          {(isOwn || user?.role === "admin") && (
            <button className="comment-action comment-delete" data-testid={`delete-comment-${comment.id}`} onClick={() => deleteComment(comment.id)}>
              <Icon name="Trash" size={13}/>
            </button>
          )}
        </div>
        {replyTo === comment.id && (
          <div className="comment-reply-box">
            <input data-testid={`reply-input-${comment.id}`} placeholder="Write a reply..." value={replyText} onChange={e => setReplyText(e.target.value)} onKeyDown={e => { if (e.key === "Enter") submit(replyText, comment.id); }} />
            <button data-testid={`reply-submit-${comment.id}`} onClick={() => submit(replyText, comment.id)} disabled={!replyText.trim()}>Reply</button>
          </div>
        )}
        {replies.map(r => <CommentItem key={r.id} comment={r} depth={depth + 1} />)}
      </div>
    );
  };

  return (
    <div className="comments-section" data-testid="comments-section">
      <h3 className="comments-title"><Icon name="MessageSquare" size={18}/> Comments ({comments.length})</h3>
      <div className="comment-input-box">
        <input data-testid="comment-input" placeholder="Add a comment..." value={newComment} onChange={e => setNewComment(e.target.value)} onKeyDown={e => { if (e.key === "Enter") submit(newComment); }} />
        <button data-testid="comment-submit-btn" onClick={() => submit(newComment)} disabled={!newComment.trim()}>Post</button>
      </div>
      <div className="comments-list">
        {topLevel.map(c => <CommentItem key={c.id} comment={c} />)}
        {comments.length === 0 && <p className="comments-empty">No comments yet. Be the first!</p>}
      </div>
    </div>
  );
}

// --- Sidebar ---
function Sidebar({ categories, documents, activeDocId, onSelectDoc, onNewDoc, collapsed, setCollapsed, bookmarkedIds, onManageCategories, isAdmin }) {
  const [expanded, setExpanded] = useState({});
  const { dark, toggle } = useTheme();
  const { logout, user } = useAuth();
  const navigate = useNavigate();
  const navRef = useRef(null);

  // All categories collapsed by default - expand only when clicked
  const parentCats = categories.filter(c => !c.parent_id).sort((a,b) => a.order - b.order);
  const getChildren = (pid) => categories.filter(c => c.parent_id === pid).sort((a,b) => a.order - b.order);
  const getDocsForCat = (catId) => documents.filter(d => d.category_id === catId).sort((a,b) => a.order - b.order);
  const toggleCat = (id) => setExpanded(p => ({...p, [id]: !p[id]}));

  useEffect(() => {
    const handleKey = (e) => {
      if (collapsed || !navRef.current) return;
      if (e.key !== "ArrowUp" && e.key !== "ArrowDown") return;
      const docBtns = navRef.current.querySelectorAll(".sidebar-doc");
      if (!docBtns.length) return;
      const ids = Array.from(docBtns).map(b => b.dataset.testid?.replace("sidebar-doc-", ""));
      const curIdx = ids.indexOf(activeDocId);
      let nextIdx;
      if (e.key === "ArrowDown") nextIdx = curIdx < ids.length - 1 ? curIdx + 1 : 0;
      else nextIdx = curIdx > 0 ? curIdx - 1 : ids.length - 1;
      if (ids[nextIdx]) { e.preventDefault(); onSelectDoc(ids[nextIdx]); }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [collapsed, activeDocId, onSelectDoc]);

  return (
    <aside className={`sidebar ${collapsed ? "sidebar-collapsed" : ""}`} data-testid="sidebar">
      <div className="sidebar-header">
        {!collapsed && <div className="sidebar-brand" data-testid="sidebar-brand"><svg width="22" height="22" viewBox="0 0 32 32" fill="none"><polygon points="16,2 30,28 2,28" stroke="currentColor" strokeWidth="2.5" fill="none"/><circle cx="16" cy="18" r="3.5" fill="currentColor"/></svg><span>EKH</span></div>}
        <button className="sidebar-collapse-btn" data-testid="sidebar-collapse-btn" onClick={() => setCollapsed(!collapsed)}><Icon name="PanelLeft" size={18}/></button>
      </div>
      {!collapsed && (
        <>
          <InlineSearch categories={categories} onSelect={onSelectDoc} />
          <nav className="sidebar-nav" ref={navRef} data-testid="sidebar-nav">
            <button className={`sidebar-item ${!activeDocId ? "active" : ""}`} data-testid="sidebar-home-btn" onClick={() => navigate("/")}><Icon name="Home" size={16}/><span>Home</span></button>
            <button className="sidebar-item" data-testid="sidebar-bookmarks-btn" onClick={() => navigate("/bookmarks")}><Icon name="Bookmark" size={16}/><span>Bookmarks</span>{bookmarkedIds.length > 0 && <span className="sidebar-badge">{bookmarkedIds.length}</span>}</button>
            <button className="sidebar-item" data-testid="sidebar-tools-btn" onClick={() => navigate("/tools")}><Icon name="Link" size={16}/><span>Tools</span></button>
            {isAdmin && <button className="sidebar-item" data-testid="sidebar-trash-btn" onClick={() => navigate("/trash")}><Icon name="Trash" size={16}/><span>Trash</span></button>}
            <div className="sidebar-divider"/>
            {parentCats.map(cat => {
              const children = getChildren(cat.id);
              const isExpanded = expanded[cat.id] === true;
              const catDocs = getDocsForCat(cat.id);
              return (
                <div key={cat.id} className="sidebar-category" data-testid={`sidebar-cat-${cat.id}`}>
                  <button className="sidebar-cat-header" onClick={() => toggleCat(cat.id)}>
                    <Icon name={isExpanded ? "ChevronDown" : "ChevronRight"} size={14}/><Icon name={cat.icon} size={16}/><span>{cat.name}</span>
                  </button>
                  {isExpanded && (
                    <div className="sidebar-cat-children">
                      {catDocs.map(d => <button key={d.id} className={`sidebar-doc ${activeDocId === d.id ? "active" : ""}`} data-testid={`sidebar-doc-${d.id}`} onClick={() => onSelectDoc(d.id)}><span>{d.title}</span></button>)}
                      {children.map(sub => {
                        const subDocs = getDocsForCat(sub.id);
                        const subExpanded = expanded[sub.id] === true;
                        if (subDocs.length === 1) return <button key={sub.id} className={`sidebar-doc ${activeDocId === subDocs[0].id ? "active" : ""}`} data-testid={`sidebar-doc-${subDocs[0].id}`} onClick={() => onSelectDoc(subDocs[0].id)}><span>{subDocs[0].title}</span></button>;
                        return (
                          <div key={sub.id} className="sidebar-subcategory">
                            <button className="sidebar-sub-header" onClick={() => toggleCat(sub.id)}><Icon name={subExpanded ? "ChevronDown" : "ChevronRight"} size={12}/><span>{sub.name}</span></button>
                            {subExpanded && subDocs.map(d => <button key={d.id} className={`sidebar-doc sidebar-doc-nested ${activeDocId === d.id ? "active" : ""}`} data-testid={`sidebar-doc-${d.id}`} onClick={() => onSelectDoc(d.id)}><span>{d.title}</span></button>)}
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}
          </nav>
          <div className="sidebar-footer">
            <button className="sidebar-footer-btn" data-testid="theme-toggle-btn" onClick={toggle}>{dark ? <Icon name="Sun" size={16}/> : <Icon name="Moon" size={16}/>}<span>{dark ? "Light mode" : "Dark mode"}</span></button>
            {isAdmin && <button className="sidebar-footer-btn" data-testid="manage-categories-btn" onClick={onManageCategories}><Icon name="FolderOpen" size={16}/><span>Manage categories</span></button>}
            {isAdmin && <button className="sidebar-footer-btn" data-testid="new-doc-btn" onClick={onNewDoc}><Icon name="Plus" size={16}/><span>New page</span></button>}
            <div className="sidebar-user">
              <div className="sidebar-user-avatar">{user?.name?.[0]?.toUpperCase() || "U"}</div>
              <span>{user?.name}</span>
              <span className={`sidebar-role-badge ${isAdmin ? "role-admin" : "role-viewer"}`}>{isAdmin ? "Admin" : "Viewer"}</span>
              <button data-testid="logout-btn" onClick={logout} className="sidebar-logout-btn"><Icon name="LogOut" size={14}/></button>
            </div>
          </div>
        </>
      )}
    </aside>
  );
}

// --- Document Viewer ---
function DocumentViewer({ doc, category, parentCategory, isBookmarked, onToggleBookmark, onEdit, onDelete, isAdmin }) {
  const { api } = useAuth();
  const [versions, setVersions] = useState([]);
  const [showVersions, setShowVersions] = useState(false);
  const [viewingVersion, setViewingVersion] = useState(null);
  const [exporting, setExporting] = useState(false);
  const [shareId, setShareId] = useState(doc?.share_id || null);
  const [copied, setCopied] = useState(false);
  const contentRef = useRef(null);

  useEffect(() => { setShowVersions(false); setViewingVersion(null); setVersions([]); setShareId(doc?.share_id || null); }, [doc?.id, doc?.share_id]);

  const loadVersions = async () => {
    if (!doc) return;
    try { const r = await api("get", `/documents/${doc.id}/versions`); setVersions(r.data); setShowVersions(true); } catch {}
  };

  const exportPDF = async () => {
    if (!contentRef.current || exporting) return;
    setExporting(true);
    try {
      const canvas = await html2canvas(contentRef.current, { scale: 2, useCORS: true, backgroundColor: "#ffffff", logging: false });
      const imgData = canvas.toDataURL("image/png");
      const pdf = new jsPDF("p", "mm", "a4");
      const pdfW = pdf.internal.pageSize.getWidth();
      const pdfH = pdf.internal.pageSize.getHeight();
      const imgW = canvas.width;
      const imgH = canvas.height;
      const ratio = pdfW / imgW;
      const scaledH = imgH * ratio;
      let position = 0;
      while (position < scaledH) {
        if (position > 0) pdf.addPage();
        pdf.addImage(imgData, "PNG", 0, -position, pdfW, scaledH);
        position += pdfH;
      }
      pdf.save(`${doc.title}.pdf`);
    } catch (e) { console.error("PDF export error:", e); }
    setExporting(false);
  };

  const toggleShare = async () => {
    try {
      const r = await api("post", `/documents/${doc.id}/share`);
      setShareId(r.data.shared ? r.data.share_id : null);
    } catch {}
  };

  const copyShareLink = () => {
    const url = `${window.location.origin}/share/${shareId}`;
    navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!doc) return (
    <div className="doc-empty" data-testid="doc-empty"><Icon name="FileText" size={48}/><h2>Select a document</h2><p>Choose a document from the sidebar or create a new one.</p></div>
  );

  const displayContent = viewingVersion ? viewingVersion.content : doc.content;
  const headings = displayContent?.match(/^## .+/gm)?.map(h => ({ text: h.slice(3), id: h.slice(3).toLowerCase().replace(/[^a-z0-9]+/g, "-") })) || [];
  const tags = doc.tags || [];

  return (
    <div className="doc-viewer" data-testid="doc-viewer">
      <div className="doc-breadcrumb" data-testid="doc-breadcrumb">
        {parentCategory && <><span>{parentCategory.name}</span><Icon name="ChevronRight" size={14}/></>}
        {category && <><span>{category.name}</span><Icon name="ChevronRight" size={14}/></>}
        <span className="doc-breadcrumb-active">{doc.title}</span>
      </div>
      <div className="doc-header">
        <div>
          <h1 className="doc-title" data-testid="doc-title">{viewingVersion ? `${doc.title} (version)` : doc.title}</h1>
          {tags.length > 0 && <div className="doc-tags" data-testid="doc-tags">{tags.map((t, i) => <span key={i} className="doc-tag"><Icon name="Tag" size={11}/>{t}</span>)}</div>}
          {shareId && (
            <div className="doc-share-bar" data-testid="share-bar">
              <Icon name="Share" size={13}/> <span>Shared</span>
              <button className="doc-share-copy" data-testid="copy-share-link" onClick={copyShareLink}>{copied ? "Copied!" : "Copy link"}</button>
            </div>
          )}
        </div>
        <div className="doc-actions">
          {viewingVersion && <button data-testid="version-back-btn" className="doc-action-btn" onClick={() => setViewingVersion(null)} title="Back to current"><Icon name="ArrowLeft" size={18}/></button>}
          <button data-testid="export-pdf-btn" className="doc-action-btn" onClick={exportPDF} title="Export as PDF" disabled={exporting}><Icon name="Download" size={18}/></button>
          <button data-testid="version-history-btn" className="doc-action-btn" onClick={loadVersions} title="Version history"><Icon name="Clock" size={18}/></button>
          {isAdmin && <button data-testid="share-toggle-btn" className={`doc-action-btn ${shareId ? "bookmarked" : ""}`} onClick={toggleShare} title={shareId ? "Disable sharing" : "Enable sharing"}><Icon name="Share" size={18}/></button>}
          <button data-testid="bookmark-toggle-btn" className={`doc-action-btn ${isBookmarked ? "bookmarked" : ""}`} onClick={onToggleBookmark}><Icon name={isBookmarked ? "BookmarkFilled" : "Bookmark"} size={18}/></button>
          {isAdmin && <button data-testid="edit-doc-btn" className="doc-action-btn" onClick={onEdit}><Icon name="Edit" size={18}/></button>}
          {isAdmin && <button data-testid="delete-doc-btn" className="doc-action-btn doc-action-danger" onClick={onDelete}><Icon name="Trash" size={18}/></button>}
        </div>
      </div>
      <div className="doc-layout">
        <article className="doc-content" data-testid="doc-content">
          <div ref={contentRef} className="doc-content-inner"><MarkdownContent content={displayContent} /></div>
          <CommentsSection docId={doc.id} />
        </article>
        <aside className="doc-sidebar-right">
          {showVersions && (
            <div className="doc-version-panel" data-testid="version-panel">
              <div className="doc-toc-title">Version History</div>
              {versions.length === 0 ? <p className="doc-version-empty">No previous versions</p> : versions.map((v, i) => (
                <button key={v.id} className={`doc-version-item ${viewingVersion?.id === v.id ? "active" : ""}`} data-testid={`version-item-${i}`} onClick={() => setViewingVersion(v)}>
                  <span className="doc-version-date">{new Date(v.created_at).toLocaleString()}</span><span className="doc-version-title">{v.title}</span>
                </button>
              ))}
              <button className="doc-version-close" data-testid="version-close-btn" onClick={() => { setShowVersions(false); setViewingVersion(null); }}>Close</button>
            </div>
          )}
          {headings.length > 2 && !showVersions && (
            <div className="doc-toc" data-testid="doc-toc"><div className="doc-toc-title">On this page</div>{headings.map((h, i) => <a key={i} href={`#${h.id}`} className="doc-toc-link">{h.text}</a>)}</div>
          )}
        </aside>
      </div>
    </div>
  );
}

// --- Document Editor ---
function DocumentEditor({ doc, categories, onSave, onCancel }) {
  const [title, setTitle] = useState(doc?.title || "");
  const [content, setContent] = useState(doc?.content || "");
  const [categoryId, setCategoryId] = useState(doc?.category_id || "");
  const [saving, setSaving] = useState(false);
  const [showPreview, setShowPreview] = useState(true);
  const [tags, setTags] = useState(doc?.tags || []);
  const [tagInput, setTagInput] = useState("");
  const subCats = categories.filter(c => c.parent_id);

  const handleSave = async () => { if (!title.trim() || !categoryId) return; setSaving(true); await onSave({ title, content, category_id: categoryId, tags }); setSaving(false); };
  const addTag = () => { const t = tagInput.trim().toLowerCase(); if (t && !tags.includes(t)) setTags([...tags, t]); setTagInput(""); };
  const removeTag = (t) => setTags(tags.filter(x => x !== t));

  return (
    <div className="doc-editor" data-testid="doc-editor">
      <div className="editor-header">
        <h2>{doc ? "Edit page" : "New page"}</h2>
        <div className="editor-actions">
          <button data-testid="editor-preview-toggle" className={`editor-btn-toggle ${showPreview ? "active" : ""}`} onClick={() => setShowPreview(!showPreview)}><Icon name="Monitor" size={14}/><span>{showPreview ? "Hide preview" : "Show preview"}</span></button>
          <button data-testid="editor-cancel-btn" className="editor-btn-secondary" onClick={onCancel}>Cancel</button>
          <button data-testid="editor-save-btn" className="editor-btn-primary" onClick={handleSave} disabled={saving || !title.trim() || !categoryId}>{saving ? "Saving..." : "Save"}</button>
        </div>
      </div>
      <input data-testid="editor-title-input" className="editor-title" placeholder="Page title" value={title} onChange={e => setTitle(e.target.value)} />
      <select data-testid="editor-category-select" className="editor-select" value={categoryId} onChange={e => setCategoryId(e.target.value)}>
        <option value="">Select category</option>
        {subCats.map(c => <option key={c.id} value={c.id}>{categories.find(p=>p.id===c.parent_id)?.name} / {c.name}</option>)}
        {categories.filter(c => !c.parent_id).map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
      </select>
      <div className="editor-tags-row" data-testid="editor-tags-row">
        <Icon name="Tag" size={14}/>{tags.map(t => <span key={t} className="editor-tag">{t}<button onClick={() => removeTag(t)}><Icon name="X" size={10}/></button></span>)}
        <input data-testid="editor-tag-input" className="editor-tag-input" placeholder="Add tag..." value={tagInput} onChange={e => setTagInput(e.target.value)} onKeyDown={e => { if (e.key === "Enter") { e.preventDefault(); addTag(); }}} />
      </div>
      <div className={`editor-split ${showPreview ? "editor-split-active" : ""}`}>
        <textarea data-testid="editor-content-textarea" className="editor-textarea" placeholder="Write in markdown..." value={content} onChange={e => setContent(e.target.value)} />
        {showPreview && <div className="editor-preview" data-testid="editor-preview"><div className="editor-preview-header">Preview</div><div className="editor-preview-content">{title && <h1 className="doc-title" style={{marginBottom:"1rem"}}>{title}</h1>}<MarkdownContent content={content} />{!content && <p className="editor-preview-empty">Start typing to see preview...</p>}</div></div>}
      </div>
    </div>
  );
}

// --- Home / Dashboard ---
function HomePage({ categories, documents, onSelectDoc }) {
  const parentCats = categories.filter(c => !c.parent_id).sort((a,b) => a.order - b.order);
  const getChildCount = (catId) => { const children = categories.filter(c => c.parent_id === catId); return documents.filter(d => d.category_id === catId || children.some(c => c.id === d.category_id)).length; };
  return (
    <div className="home-page" data-testid="home-page">
      <div className="home-hero"><h1>Emergent Knowledge Hub</h1><p>A comprehensive knowledge base covering AI agents, LLMs, platform architecture, infrastructure, and the future of software development.</p></div>
      <div className="home-grid">{parentCats.map(cat => (
        <button key={cat.id} className="home-card" data-testid={`home-card-${cat.id}`} onClick={() => {
          const firstDoc = documents.find(d => { const children = categories.filter(c => c.parent_id === cat.id); return d.category_id === cat.id || children.some(c => c.id === d.category_id); });
          if (firstDoc) onSelectDoc(firstDoc.id);
        }}><div className="home-card-icon"><Icon name={cat.icon} size={24}/></div><h3>{cat.name}</h3><p className="home-card-count">{getChildCount(cat.id)} documents</p></button>
      ))}</div>
    </div>
  );
}

// --- Bookmarks Page ---
function BookmarksPage({ bookmarkedDocs, categories, onSelectDoc, onToggleBookmark }) {
  const getCatName = (id) => categories.find(c => c.id === id)?.name || "";
  return (
    <div className="bookmarks-page" data-testid="bookmarks-page">
      <h1>Bookmarks</h1>
      {bookmarkedDocs.length === 0 ? <div className="doc-empty"><Icon name="Bookmark" size={48}/><h2>No bookmarks yet</h2><p>Bookmark documents for quick access.</p></div>
      : <div className="bookmarks-list">{bookmarkedDocs.map(d => (
        <div key={d.id} className="bookmark-item" data-testid={`bookmark-${d.id}`}>
          <button className="bookmark-item-content" onClick={() => onSelectDoc(d.id)}><Icon name="FileText" size={18}/><div><div className="bookmark-title">{d.title}</div><div className="bookmark-cat">{getCatName(d.category_id)}</div></div></button>
          <button className="bookmark-remove-btn" data-testid={`bookmark-remove-${d.id}`} onClick={() => onToggleBookmark(d.id)}><Icon name="X" size={16}/></button>
        </div>
      ))}</div>}
    </div>
  );
}

// --- Trash Page (Admin only) ---
function TrashPage() {
  const { api } = useAuth();
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { api("get", "/trash").then(r => setDocs(r.data)).catch(() => {}).finally(() => setLoading(false)); }, [api]);
  const restore = async (id) => { try { await api("post", `/trash/${id}/restore`); setDocs(prev => prev.filter(d => d.id !== id)); } catch {} };
  const permDelete = async (id) => { if (!window.confirm("Permanently delete? This cannot be undone.")) return; try { await api("delete", `/trash/${id}`); setDocs(prev => prev.filter(d => d.id !== id)); } catch {} };
  if (loading) return <div className="edh-loading"><div className="edh-spinner"/></div>;
  return (
    <div className="bookmarks-page" data-testid="trash-page">
      <h1>Trash</h1>
      {docs.length === 0 ? <div className="doc-empty"><Icon name="Trash" size={48}/><h2>Trash is empty</h2><p>Deleted documents will appear here.</p></div>
      : <div className="bookmarks-list">{docs.map(d => (
        <div key={d.id} className="bookmark-item" data-testid={`trash-item-${d.id}`}>
          <div className="bookmark-item-content"><Icon name="FileText" size={18}/><div><div className="bookmark-title">{d.title}</div><div className="bookmark-cat">Deleted {d.deleted_at ? new Date(d.deleted_at).toLocaleDateString() : ""}</div></div></div>
          <button className="trash-restore-btn" data-testid={`restore-${d.id}`} onClick={() => restore(d.id)}><Icon name="Undo" size={14}/></button>
          <button className="bookmark-remove-btn" data-testid={`perm-delete-${d.id}`} onClick={() => permDelete(d.id)}><Icon name="Trash" size={14}/></button>
        </div>
      ))}</div>}
    </div>
  );
}

// --- Tools Page ---
function ToolsPage({ isAdmin }) {
  const { api } = useAuth();
  const [tools, setTools] = useState([]);
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);
  const [form, setForm] = useState({ name: "", url: "", description: "", category: "General" });
  const [editId, setEditId] = useState(null);

  useEffect(() => { api("get", "/tools").then(r => setTools(r.data)).catch(() => {}).finally(() => setLoading(false)); }, [api]);

  const save = async () => {
    if (!form.name.trim() || !form.url.trim()) return;
    try {
      if (editId) { const r = await api("put", `/tools/${editId}`, form); setTools(prev => prev.map(t => t.id === editId ? r.data : t)); }
      else { const r = await api("post", "/tools", form); setTools(prev => [...prev, r.data]); }
      setAdding(false); setEditId(null); setForm({ name: "", url: "", description: "", category: "General" });
    } catch {}
  };

  const del = async (id) => { try { await api("delete", `/tools/${id}`); setTools(prev => prev.filter(t => t.id !== id)); } catch {} };

  const categories = [...new Set(tools.map(t => t.category))].sort();

  if (loading) return <div className="edh-loading"><div className="edh-spinner"/></div>;
  return (
    <div className="bookmarks-page" data-testid="tools-page">
      <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:"2rem"}}>
        <h1>Tools & Resources</h1>
        {isAdmin && <button className="editor-btn-primary" data-testid="add-tool-btn" onClick={() => { setAdding(true); setEditId(null); setForm({ name: "", url: "", description: "", category: "General" }); }}><Icon name="Plus" size={14}/> Add Tool</button>}
      </div>
      {(adding || editId) && (
        <div className="tool-form" data-testid="tool-form">
          <input data-testid="tool-name" placeholder="Tool name" value={form.name} onChange={e => setForm({...form, name: e.target.value})} />
          <input data-testid="tool-url" placeholder="URL" value={form.url} onChange={e => setForm({...form, url: e.target.value})} />
          <input data-testid="tool-desc" placeholder="Description" value={form.description} onChange={e => setForm({...form, description: e.target.value})} />
          <input data-testid="tool-category" placeholder="Category" value={form.category} onChange={e => setForm({...form, category: e.target.value})} />
          <div className="tool-form-actions">
            <button className="editor-btn-primary" data-testid="tool-save-btn" onClick={save}>Save</button>
            <button className="editor-btn-secondary" onClick={() => { setAdding(false); setEditId(null); }}>Cancel</button>
          </div>
        </div>
      )}
      {categories.map(cat => (
        <div key={cat} className="tool-group">
          <h3 className="tool-group-title">{cat}</h3>
          {tools.filter(t => t.category === cat).map(t => (
            <div key={t.id} className="tool-item" data-testid={`tool-${t.id}`}>
              <div className="tool-info"><a href={t.url} target="_blank" rel="noreferrer" className="tool-link"><Icon name="Link" size={14}/> {t.name}</a>{t.description && <p className="tool-desc">{t.description}</p>}</div>
              {isAdmin && <div className="tool-actions">
                <button data-testid={`edit-tool-${t.id}`} onClick={() => { setEditId(t.id); setAdding(false); setForm({ name: t.name, url: t.url, description: t.description, category: t.category }); }}><Icon name="Edit" size={14}/></button>
                <button data-testid={`delete-tool-${t.id}`} onClick={() => del(t.id)}><Icon name="Trash" size={14}/></button>
              </div>}
            </div>
          ))}
        </div>
      ))}
      {tools.length === 0 && !adding && <div className="doc-empty"><Icon name="Link" size={48}/><h2>No tools yet</h2><p>{isAdmin ? "Add tools using the button above." : "Tools will appear here when added by admin."}</p></div>}
    </div>
  );
}

// --- Category Manager Dialog ---
function CategoryManager({ open, onClose, categories, onCategoriesChange, isAdmin }) {
  const { api } = useAuth();
  const [newName, setNewName] = useState(""); const [newIcon, setNewIcon] = useState("FileText"); const [newParent, setNewParent] = useState("");
  const [editingId, setEditingId] = useState(null); const [editName, setEditName] = useState(""); const [editIcon, setEditIcon] = useState(""); const [error, setError] = useState("");
  const iconOptions = ["FileText","Layers","Cpu","Server","Monitor","Database","Rocket","Lock","FolderOpen","Sparkles","Telescope","Search","Check","Link"];
  const parentCats = categories.filter(c => !c.parent_id).sort((a,b) => a.order - b.order);

  const handleCreate = async () => { if (!newName.trim()) return; setError(""); try { const maxOrder = categories.filter(c => newParent ? c.parent_id === newParent : !c.parent_id).length; const r = await api("post", "/categories", { name: newName.trim(), icon: newIcon, order: maxOrder, parent_id: newParent || null }); onCategoriesChange([...categories, r.data]); setNewName(""); setNewIcon("FileText"); setNewParent(""); } catch (e) { setError(e.response?.data?.detail || "Failed"); } };
  const handleUpdate = async (id) => { setError(""); try { const r = await api("put", `/categories/${id}`, { name: editName.trim(), icon: editIcon }); onCategoriesChange(categories.map(c => c.id === id ? r.data : c)); setEditingId(null); } catch (e) { setError(e.response?.data?.detail || "Failed"); } };
  const handleDelete = async (id) => { if (!window.confirm("Delete this category?")) return; setError(""); try { await api("delete", `/categories/${id}`); onCategoriesChange(categories.filter(c => c.id !== id)); } catch (e) { setError(e.response?.data?.detail || "Cannot delete"); } };

  if (!open || !isAdmin) return null;
  return (
    <div className="search-overlay" onClick={() => onClose()} data-testid="category-manager-overlay">
      <div className="catmgr-dialog" onClick={e => e.stopPropagation()} data-testid="category-manager">
        <div className="catmgr-header"><h2>Manage Categories</h2><button className="catmgr-close" data-testid="catmgr-close-btn" onClick={onClose}><Icon name="X" size={18}/></button></div>
        {error && <div className="auth-error" style={{margin:"0 20px"}}>{error}</div>}
        <div className="catmgr-body">
          <div className="catmgr-section"><h3>Add new</h3>
            <div className="catmgr-add-row">
              <input data-testid="catmgr-name-input" placeholder="Name" value={newName} onChange={e => setNewName(e.target.value)} />
              <select data-testid="catmgr-icon-select" value={newIcon} onChange={e => setNewIcon(e.target.value)}>{iconOptions.map(i => <option key={i} value={i}>{i}</option>)}</select>
              <select data-testid="catmgr-parent-select" value={newParent} onChange={e => setNewParent(e.target.value)}><option value="">Top-level</option>{parentCats.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}</select>
              <button data-testid="catmgr-add-btn" className="editor-btn-primary" onClick={handleCreate} disabled={!newName.trim()}>Add</button>
            </div>
          </div>
          <div className="catmgr-section"><h3>Categories</h3>
            <div className="catmgr-list">{parentCats.map(cat => {
              const children = categories.filter(c => c.parent_id === cat.id).sort((a,b) => a.order - b.order);
              return (
                <div key={cat.id} className="catmgr-group">
                  <div className="catmgr-item"><Icon name={cat.icon} size={16}/>
                    {editingId === cat.id ? (<><input className="catmgr-edit-input" value={editName} onChange={e => setEditName(e.target.value)} /><select className="catmgr-edit-select" value={editIcon} onChange={e => setEditIcon(e.target.value)}>{iconOptions.map(i => <option key={i} value={i}>{i}</option>)}</select><button className="catmgr-action-btn" onClick={() => handleUpdate(cat.id)}><Icon name="Check" size={14}/></button><button className="catmgr-action-btn" onClick={() => setEditingId(null)}><Icon name="X" size={14}/></button></>)
                    : (<><span className="catmgr-name">{cat.name}</span><button className="catmgr-action-btn" onClick={() => { setEditingId(cat.id); setEditName(cat.name); setEditIcon(cat.icon); }}><Icon name="Edit" size={14}/></button><button className="catmgr-action-btn catmgr-danger" onClick={() => handleDelete(cat.id)}><Icon name="Trash" size={14}/></button></>)}
                  </div>
                  {children.map(sub => (
                    <div key={sub.id} className="catmgr-item catmgr-sub"><Icon name={sub.icon || "FileText"} size={14}/>
                      {editingId === sub.id ? (<><input className="catmgr-edit-input" value={editName} onChange={e => setEditName(e.target.value)} /><button className="catmgr-action-btn" onClick={() => handleUpdate(sub.id)}><Icon name="Check" size={14}/></button><button className="catmgr-action-btn" onClick={() => setEditingId(null)}><Icon name="X" size={14}/></button></>)
                      : (<><span className="catmgr-name">{sub.name}</span><button className="catmgr-action-btn" onClick={() => { setEditingId(sub.id); setEditName(sub.name); setEditIcon(sub.icon); }}><Icon name="Edit" size={14}/></button><button className="catmgr-action-btn catmgr-danger" onClick={() => handleDelete(sub.id)}><Icon name="Trash" size={14}/></button></>)}
                    </div>
                  ))}
                </div>
              );
            })}</div>
          </div>
        </div>
      </div>
    </div>
  );
}

// --- Public Document Page ---
function PublicDocPage() {
  const { shareId } = useParams();
  const [doc, setDoc] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get(`${API}/public/${shareId}`).then(r => setDoc(r.data)).catch(() => setError("Document not found or not shared")).finally(() => setLoading(false));
  }, [shareId]);

  if (loading) return <div className="edh-loading"><div className="edh-spinner"/></div>;
  if (error) return <div className="public-error" data-testid="public-error"><h1>Not Found</h1><p>{error}</p><a href="/login">Go to login</a></div>;

  return (
    <div className="public-doc" data-testid="public-doc">
      <div className="public-header"><svg width="22" height="22" viewBox="0 0 32 32" fill="none"><polygon points="16,2 30,28 2,28" stroke="currentColor" strokeWidth="2.5" fill="none"/><circle cx="16" cy="18" r="3.5" fill="currentColor"/></svg><span>Emergent Document Hub</span></div>
      <article className="doc-viewer" style={{maxWidth:800,margin:"0 auto",padding:"2rem"}}>
        <h1 className="doc-title" data-testid="public-doc-title">{doc.title}</h1>
        {doc.tags?.length > 0 && <div className="doc-tags">{doc.tags.map((t,i) => <span key={i} className="doc-tag"><Icon name="Tag" size={11}/>{t}</span>)}</div>}
        <div className="doc-content"><MarkdownContent content={doc.content} /></div>
      </article>
    </div>
  );
}

// --- Main Dashboard ---
function Dashboard() {
  const { api, user } = useAuth();
  const navigate = useNavigate();
  const { docId } = useParams();
  const [categories, setCategories] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [bookmarkedIds, setBookmarkedIds] = useState([]);
  const [activeDoc, setActiveDoc] = useState(null);
  const [editing, setEditing] = useState(false);
  const [creating, setCreating] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [loading, setLoading] = useState(true);
  const [catManagerOpen, setCatManagerOpen] = useState(false);
  const isAdmin = user?.role === "admin";

  useEffect(() => {
    const load = async () => {
      try {
        const [catRes, docRes, bmRes] = await Promise.all([api("get", "/categories"), api("get", "/documents"), api("get", "/bookmarks")]);
        setCategories(catRes.data); setDocuments(docRes.data); setBookmarkedIds(bmRes.data.bookmarks.map(b => b.document_id));
      } catch (e) { console.error(e); }
      setLoading(false);
    };
    load();
  }, [api]);

  useEffect(() => {
    if (docId && documents.length > 0) {
      const doc = documents.find(d => d.id === docId);
      if (doc) { setActiveDoc(doc); setEditing(false); setCreating(false); }
    }
  }, [docId, documents]);

  const selectDoc = (id) => navigate(`/doc/${id}`);
  const toggleBookmark = async (dId) => { try { const r = await api("post", `/bookmarks/${dId}`); setBookmarkedIds(prev => r.data.bookmarked ? [...prev, dId] : prev.filter(x => x !== dId)); } catch {} };

  const handleSaveDoc = async (data) => {
    try {
      if (creating) { const r = await api("post", "/documents", data); setDocuments(prev => [...prev, r.data]); setCreating(false); navigate(`/doc/${r.data.id}`); }
      else if (editing && activeDoc) { const r = await api("put", `/documents/${activeDoc.id}`, data); setDocuments(prev => prev.map(d => d.id === activeDoc.id ? r.data : d)); setActiveDoc(r.data); setEditing(false); }
    } catch {}
  };

  const handleDelete = async () => {
    if (!activeDoc || !window.confirm("Move this document to trash?")) return;
    try { await api("delete", `/documents/${activeDoc.id}`); setDocuments(prev => prev.filter(d => d.id !== activeDoc.id)); setActiveDoc(null); navigate("/"); } catch {}
  };

  const startNew = () => { setCreating(true); setEditing(false); setActiveDoc(null); };

  if (loading) return <div className="edh-loading"><div className="edh-spinner"/></div>;

  const currentCat = activeDoc ? categories.find(c => c.id === activeDoc.category_id) : null;
  const parentCat = currentCat?.parent_id ? categories.find(c => c.id === currentCat.parent_id) : null;
  const bookmarkedDocs = documents.filter(d => bookmarkedIds.includes(d.id));
  const isBookmarksRoute = window.location.pathname === "/bookmarks";
  const isToolsRoute = window.location.pathname === "/tools";
  const isTrashRoute = window.location.pathname === "/trash";
  const showHome = !docId && !creating && !editing && !isBookmarksRoute && !isToolsRoute && !isTrashRoute;

  return (
    <div className="dashboard" data-testid="dashboard">
      <Sidebar categories={categories} documents={documents} activeDocId={activeDoc?.id} onSelectDoc={selectDoc} onNewDoc={startNew} collapsed={sidebarCollapsed} setCollapsed={setSidebarCollapsed} bookmarkedIds={bookmarkedIds} onManageCategories={() => setCatManagerOpen(true)} isAdmin={isAdmin} />
      <main className="main-content" data-testid="main-content">
        {creating || editing ? <DocumentEditor doc={editing ? activeDoc : null} categories={categories} onSave={handleSaveDoc} onCancel={() => { setCreating(false); setEditing(false); if (activeDoc) navigate(`/doc/${activeDoc.id}`); else navigate("/"); }} />
        : isBookmarksRoute ? <BookmarksPage bookmarkedDocs={bookmarkedDocs} categories={categories} onSelectDoc={selectDoc} onToggleBookmark={toggleBookmark} />
        : isToolsRoute ? <ToolsPage isAdmin={isAdmin} />
        : isTrashRoute && isAdmin ? <TrashPage />
        : showHome ? <HomePage categories={categories} documents={documents} onSelectDoc={selectDoc} />
        : <DocumentViewer doc={activeDoc} category={currentCat} parentCategory={parentCat} isBookmarked={bookmarkedIds.includes(activeDoc?.id)} onToggleBookmark={() => activeDoc && toggleBookmark(activeDoc.id)} onEdit={() => setEditing(true)} onDelete={handleDelete} isAdmin={isAdmin} />}
      </main>
      <CategoryManager open={catManagerOpen} onClose={() => setCatManagerOpen(false)} categories={categories} onCategoriesChange={setCategories} isAdmin={isAdmin} />
    </div>
  );
}

function AppRouter() {
  const location = useLocation();
  // Check URL fragment for session_id - must be synchronous (not in useEffect)
  if (location.hash?.includes('session_id=')) { return <AuthCallback />; }
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/share/:shareId" element={<PublicDocPage />} />
      <Route path="/bookmarks" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/tools" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/trash" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/doc/:docId" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
    </Routes>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <AppRouter />
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
