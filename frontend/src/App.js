import React, { useState, useEffect, createContext, useContext, useCallback, useRef, useMemo } from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate, useParams, useSearchParams } from "react-router-dom";
import axios from "axios";
import mermaid from "mermaid";
import html2canvas from "html2canvas";
import { jsPDF } from "jspdf";
import "@/App.css";

mermaid.initialize({ startOnLoad: false, theme: "dark", themeVariables: { primaryColor: "#4f46e5", primaryBorderColor: "#6366f1", primaryTextColor: "#e4e4e7", lineColor: "#71717a", secondaryColor: "#27272a", tertiaryColor: "#18181b", background: "#18181b", mainBkg: "#27272a", nodeBorder: "#6366f1", clusterBkg: "#1a1a2e", titleColor: "#e4e4e7" }, flowchart: { padding: 35, nodeSpacing: 100, rankSpacing: 100, htmlLabels: true, wrappingWidth: 200, curve: "basis", useMaxWidth: false }, sequence: { actorMargin: 150, messageMargin: 70 } });

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;
// WebSocket URL: proxy redirects external->internal, so use window.location for WS base
const getWsUrl = (path) => {
  const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${proto}//${window.location.host}${path}`;
};

// --- Collaboration Identity ---
const COLLAB_COLORS = ["#ef4444","#f97316","#eab308","#22c55e","#06b6d4","#3b82f6","#8b5cf6","#ec4899","#14b8a6","#f43f5e"];
function getCollabIdentity() {
  let identity = null;
  try { identity = JSON.parse(localStorage.getItem("ekh-collab-identity")); } catch {}
  if (!identity || !identity.id) {
    identity = { id: "u_" + Math.random().toString(36).slice(2, 10), name: "User " + Math.floor(Math.random() * 900 + 100), color: COLLAB_COLORS[Math.floor(Math.random() * COLLAB_COLORS.length)] };
    localStorage.setItem("ekh-collab-identity", JSON.stringify(identity));
  }
  return identity;
}

// --- useCollaboration Hook ---
function useCollaboration(docId, enabled = true) {
  const [users, setUsers] = useState([]);
  const [remoteContent, setRemoteContent] = useState(null);
  const [saved, setSaved] = useState(null);
  const wsRef = useRef(null);
  const identity = useMemo(() => getCollabIdentity(), []);

  useEffect(() => {
    if (!docId || !enabled) return;
    const url = getWsUrl(`/api/ws/collab/${docId}?user_id=${encodeURIComponent(identity.id)}&name=${encodeURIComponent(identity.name)}&color=${encodeURIComponent(identity.color)}`);
    let ws;
    let reconnectTimer;
    const connect = () => {
      ws = new WebSocket(url);
      wsRef.current = ws;
      ws.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data);
          if (msg.type === "presence") setUsers(msg.users);
          else if (msg.type === "content_update") setRemoteContent({ content: msg.content, senderId: msg.sender_id, cursor: msg.cursor });
          else if (msg.type === "doc_saved") setSaved({ senderId: msg.sender_id, at: Date.now() });
        } catch {}
      };
      ws.onclose = () => { reconnectTimer = setTimeout(connect, 2000); };
      ws.onerror = () => { ws.close(); };
    };
    connect();
    return () => { clearTimeout(reconnectTimer); wsRef.current = null; ws?.close(); };
  }, [docId, enabled, identity]);

  const sendContent = useCallback((content, cursor) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) wsRef.current.send(JSON.stringify({ type: "content_update", content, cursor }));
  }, []);

  const sendCursor = useCallback((cursor, selectionEnd) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) wsRef.current.send(JSON.stringify({ type: "cursor_update", cursor, selection_end: selectionEnd }));
  }, []);

  const sendMode = useCallback((mode) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) wsRef.current.send(JSON.stringify({ type: "mode_change", mode }));
  }, []);

  const sendSave = useCallback((content, title) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) wsRef.current.send(JSON.stringify({ type: "save", content, title }));
  }, []);

  return { users, remoteContent, saved, identity, sendContent, sendCursor, sendMode, sendSave };
}

// --- Contexts ---
const AuthContext = createContext(null);
const ThemeContext = createContext(null);
const KeywordContext = createContext({});
export const useAuth = () => useContext(AuthContext);
export const useTheme = () => useContext(ThemeContext);
export const useKeywords = () => useContext(KeywordContext);

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
  const [user] = useState({ user_id: "default", email: "admin@emergent.sh", name: "Admin", role: "admin", picture: "" });
  const [loading] = useState(false);

  const api = useCallback(async (method, url, data) => {
    return axios({ method, url: `${API}${url}`, data, maxRedirects: 5 });
  }, []);

  const logout = () => {};

  return <AuthContext.Provider value={{ user, loading, api, logout, setUser: () => {} }}>{children}</AuthContext.Provider>;
}

function ProtectedRoute({ children }) {
  return children;
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
    Users: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>,
    Wifi: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 20h.01"/><path d="M2 8.82a15 15 0 0 1 20 0"/><path d="M5 12.859a10 10 0 0 1 14 0"/><path d="M8.5 16.429a5 5 0 0 1 7 0"/></svg>,
    Save: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M15.2 3a2 2 0 0 1 1.4.6l3.8 3.8a2 2 0 0 1 .6 1.4V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z"/><path d="M17 21v-7a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v7"/><path d="M7 3v4a1 1 0 0 0 1 1h7"/></svg>,
    BarChart: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" x2="12" y1="20" y2="10"/><line x1="18" x2="18" y1="20" y2="4"/><line x1="6" x2="6" y1="20" y2="16"/></svg>,
    TrendingUp: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>,
    Eye: <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/></svg>,
  };
  return icons[name] || icons.FileText;
}

// --- Markdown Renderer ---
// Collapsible section for H2 headings
function CollapsibleH2({ text, id, children }) {
  const [open, setOpen] = useState(true);
  return (
    <div className="collapsible-section" data-testid={`section-${id}`}>
      <h2 className="doc-h2 collapsible-h2" id={id} onClick={() => setOpen(!open)}>
        <span className="collapse-icon">{open ? "−" : "+"}</span>
        {text}
      </h2>
      {open && <div className="collapsible-body">{children}</div>}
    </div>
  );
}

function MarkdownContent({ content, currentDocId }) {
  if (!content) return null;
  const lines = content.split("\n");
  // First pass: parse all elements
  const parsed = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (line.startsWith("```")) {
      const lang = line.slice(3).trim();
      const codeLines = [];
      i++;
      while (i < lines.length && !lines[i].startsWith("```")) { codeLines.push(lines[i]); i++; }
      i++;
      if (lang === "mermaid") parsed.push({ type: "mermaid", content: codeLines.join("\n") });
      else parsed.push({ type: "code", content: codeLines.join("\n"), lang });
      continue;
    }
    if (line.startsWith("# ")) { i++; continue; }
    if (line.startsWith("## ")) { parsed.push({ type: "h2", text: line.slice(3), id: line.slice(3).toLowerCase().replace(/[^a-z0-9]+/g,"-") }); i++; continue; }
    if (line.startsWith("### ")) { parsed.push({ type: "h3", text: line.slice(4) }); i++; continue; }
    if (line.includes("|") && lines[i+1]?.includes("---")) {
      const headers = line.split("|").map(c=>c.trim()).filter(Boolean);
      i += 2;
      const rows = [];
      while (i < lines.length && lines[i].includes("|")) { rows.push(lines[i].split("|").map(c=>c.trim()).filter(Boolean)); i++; }
      parsed.push({ type: "table", headers, rows });
      continue;
    }
    if (line.startsWith("- ")) {
      const items = [];
      while (i < lines.length && lines[i].startsWith("- ")) { items.push(lines[i].slice(2)); i++; }
      parsed.push({ type: "ul", items });
      continue;
    }
    if (/^\d+\.\s/.test(line)) {
      const items = [];
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) { items.push(lines[i].replace(/^\d+\.\s/, "")); i++; }
      parsed.push({ type: "ol", items });
      continue;
    }
    if (!line.trim()) { i++; continue; }
    parsed.push({ type: "p", text: line });
    i++;
  }
  // Second pass: group into collapsible H2 sections
  const elements = [];
  let idx = 0;
  while (idx < parsed.length) {
    const item = parsed[idx];
    if (item.type === "h2") {
      const sectionItems = [];
      idx++;
      while (idx < parsed.length && parsed[idx].type !== "h2") { sectionItems.push(parsed[idx]); idx++; }
      elements.push(
        <CollapsibleH2 key={elements.length} text={item.text} id={item.id}>
          {sectionItems.map((si, j) => renderParsedItem(si, `${elements.length}-${j}`, currentDocId))}
        </CollapsibleH2>
      );
    } else {
      elements.push(renderParsedItem(item, elements.length, currentDocId));
      idx++;
    }
  }
  return <>{elements}</>;
}

function renderParsedItem(item, key, currentDocId) {
  switch (item.type) {
    case "mermaid": return <MermaidDiagram key={key} chart={item.content} />;
    case "code": return <CodeBlock key={key} code={item.content} lang={item.lang} />;
    case "h3": return <h3 key={key} className="doc-h3">{item.text}</h3>;
    case "table": return (
      <div key={key} className="doc-table-wrap">
        <table className="doc-table"><thead><tr>{item.headers.map((h,j) => <th key={j} dangerouslySetInnerHTML={{__html: renderInlineHtml(h)}} />)}</tr></thead>
        <tbody>{item.rows.map((r,j) => <tr key={j}>{r.map((c,k) => <td key={k} dangerouslySetInnerHTML={{__html: renderInlineHtml(c)}} />)}</tr>)}</tbody></table>
      </div>
    );
    case "ul": return <ul key={key} className="doc-ul">{item.items.map((it, j) => <li key={j}><KeywordLinkedText currentDocId={currentDocId}>{renderInline(it)}</KeywordLinkedText></li>)}</ul>;
    case "ol": return <ol key={key} className="doc-ol">{item.items.map((it, j) => <li key={j}><KeywordLinkedText currentDocId={currentDocId}>{renderInline(it)}</KeywordLinkedText></li>)}</ol>;
    case "p": return <p key={key} className="doc-p"><KeywordLinkedText currentDocId={currentDocId}>{renderInline(item.text)}</KeywordLinkedText></p>;
    default: return null;
  }
}

function renderInlineHtml(text) {
  if (!text) return "";
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code class="doc-inline-code">$1</code>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="doc-link" target="_blank" rel="noreferrer">$1</a>')
    .replace(/(^|[^"'>])(https?:\/\/[^\s<,|]+)/g, '$1<a href="$2" class="doc-link" target="_blank" rel="noreferrer">$2</a>');
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
    const italicMatch = remaining.match(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/);
    let earliest = null;
    let earliestIdx = remaining.length;
    if (boldMatch && boldMatch.index < earliestIdx) { earliest = "bold"; earliestIdx = boldMatch.index; }
    if (codeMatch && codeMatch.index < earliestIdx) { earliest = "code"; earliestIdx = codeMatch.index; }
    if (linkMatch && linkMatch.index < earliestIdx) { earliest = "link"; earliestIdx = linkMatch.index; }
    if (italicMatch && italicMatch.index < earliestIdx) { earliest = "italic"; earliestIdx = italicMatch.index; }
    if (!earliest) { parts.push(remaining); break; }
    if (earliestIdx > 0) parts.push(remaining.slice(0, earliestIdx));
    if (earliest === "bold") { parts.push(<strong key={key++}>{boldMatch[1]}</strong>); remaining = remaining.slice(earliestIdx + boldMatch[0].length); }
    else if (earliest === "code") { parts.push(<code key={key++} className="doc-inline-code">{codeMatch[1]}</code>); remaining = remaining.slice(earliestIdx + codeMatch[0].length); }
    else if (earliest === "link") { parts.push(<a key={key++} href={linkMatch[2]} className="doc-link" target="_blank" rel="noreferrer">{linkMatch[1]}</a>); remaining = remaining.slice(earliestIdx + linkMatch[0].length); }
    else if (earliest === "italic") { parts.push(<em key={key++}>{italicMatch[1]}</em>); remaining = remaining.slice(earliestIdx + italicMatch[0].length); }
  }
  return parts;
}

// Keyword auto-linking wrapper
function KeywordLinkedText({ children, currentDocId }) {
  const keywords = useKeywords();
  const navigate = useNavigate();
  if (!children || (typeof children === "string" && !children.trim())) return children;
  const entries = Object.entries(keywords);
  if (entries.length === 0) return children;

  const processText = (text) => {
    if (typeof text !== "string" || text.length < 6) return text;
    const lower = text.toLowerCase();
    // Find the best (longest) keyword match
    let bestMatch = null;
    let bestIdx = text.length;
    for (const [kw, docId] of entries) {
      if (kw.length < 4 || kw.length > 25) continue; // Skip very short or full titles
      if (docId === currentDocId) continue; // Don't link to current document
      const kwLower = kw.toLowerCase();
      const idx = lower.indexOf(kwLower);
      if (idx !== -1 && idx < bestIdx) {
        const before = idx > 0 ? lower[idx - 1] : " ";
        const after = idx + kw.length < lower.length ? lower[idx + kw.length] : " ";
        if (/[\s,.;:!?()\-]/.test(before) || idx === 0) {
          if (/[\s,.;:!?()\-]/.test(after) || idx + kw.length === lower.length) {
            bestMatch = { keyword: kw, docId, index: idx, length: kw.length };
            bestIdx = idx;
          }
        }
      }
    }
    if (!bestMatch) return text;
    const { index, length, docId } = bestMatch;
    const before = text.slice(0, index);
    const match = text.slice(index, index + length);
    const after = text.slice(index + length);
    return <>{before}<a className="doc-keyword-link" data-testid={`keyword-link-${docId.slice(0,8)}`} onClick={(e) => { e.preventDefault(); navigate(`/doc/${docId}`); }}>{match}</a>{after}</>;
  };

  if (typeof children === "string") return processText(children);
  if (Array.isArray(children)) return children.map((c, i) => typeof c === "string" ? <React.Fragment key={i}>{processText(c)}</React.Fragment> : c);
  return children;
}

function MermaidDiagram({ chart }) {
  const ref = useRef(null);
  const [svg, setSvg] = useState("");
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState(false);
  const [zoom, setZoom] = useState(1);
  const { dark } = useTheme();

  useEffect(() => {
    const render = async () => {
      try {
        const themeVars = dark
          ? { primaryColor: "#4f46e5", primaryBorderColor: "#6366f1", primaryTextColor: "#e4e4e7", lineColor: "#71717a", secondaryColor: "#27272a", tertiaryColor: "#18181b", background: "transparent", mainBkg: "#27272a", nodeBorder: "#6366f1", clusterBkg: "#1a1a2e", titleColor: "#e4e4e7", edgeLabelBackground: "#18181b", nodeTextColor: "#e4e4e7", fontSize: "14px" }
          : { primaryColor: "#4f46e5", primaryBorderColor: "#6366f1", primaryTextColor: "#18181b", lineColor: "#71717a", background: "transparent", mainBkg: "#eef2ff", secondaryColor: "#f0f0ff", tertiaryColor: "#f8f8ff", nodeBorder: "#6366f1", edgeLabelBackground: "#ffffff", nodeTextColor: "#18181b", clusterBkg: "#f5f5ff", titleColor: "#18181b", fontSize: "14px" };
        mermaid.initialize({ startOnLoad: false, theme: dark ? "dark" : "base", themeVariables: themeVars, flowchart: { padding: 35, nodeSpacing: 100, rankSpacing: 100, htmlLabels: true, wrappingWidth: 200, curve: "basis", useMaxWidth: false }, sequence: { actorMargin: 150, messageMargin: 70 } });
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
        <button className="mermaid-expand-btn" data-testid="mermaid-expand-btn" onClick={() => { setExpanded(true); setZoom(1); }}><Icon name="Maximize" size={12}/>Expand</button>
      </div>
      {expanded && (
        <div className="mermaid-modal" data-testid="mermaid-modal" onClick={() => setExpanded(false)}>
          <div className="mermaid-modal-content" onClick={e => e.stopPropagation()}>
            <div className="mermaid-modal-toolbar">
              <div className="mermaid-zoom-controls">
                <button data-testid="zoom-out" onClick={() => setZoom(z => Math.max(0.3, z - 0.2))}>-</button>
                <span>{Math.round(zoom * 100)}%</span>
                <button data-testid="zoom-in" onClick={() => setZoom(z => Math.min(3, z + 0.2))}>+</button>
                <button data-testid="zoom-reset" onClick={() => setZoom(1)}>Reset</button>
              </div>
              <button className="mermaid-modal-close" data-testid="mermaid-modal-close" onClick={() => setExpanded(false)}><Icon name="X" size={16}/> Close</button>
            </div>
            <div className="mermaid-modal-svg">
              <div style={{transform: `scale(${zoom})`, transformOrigin: "top left", transition: "transform 0.15s"}} dangerouslySetInnerHTML={{ __html: svg }} />
            </div>
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
function InlineSearch({ categories, documents, onSelect }) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [catResults, setCatResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [focused, setFocused] = useState(false);
  const { api } = useAuth();
  const timerRef = useRef(null);
  const wrapRef = useRef(null);

  useEffect(() => {
    const handler = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") { e.preventDefault(); wrapRef.current?.querySelector("input")?.focus(); }
      if (e.key === "Escape") { setQuery(""); setResults([]); setCatResults([]); wrapRef.current?.querySelector("input")?.blur(); }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  useEffect(() => {
    if (query.length < 1) { setResults([]); setCatResults([]); return; }
    // Local category search
    const q = query.toLowerCase();
    const matchedCats = categories.filter(c => c.name.toLowerCase().includes(q));
    setCatResults(matchedCats.slice(0, 5));
    // Remote doc search
    clearTimeout(timerRef.current);
    timerRef.current = setTimeout(async () => {
      setSearching(true);
      try { const r = await api("get", `/search?q=${encodeURIComponent(query)}`); setResults(r.data); } catch {}
      setSearching(false);
    }, 200);
    return () => clearTimeout(timerRef.current);
  }, [query, api, categories]);

  const getCatName = (id) => categories.find(c => c.id === id)?.name || "";
  const getFirstDocInCat = (catId) => {
    const children = categories.filter(c => c.parent_id === catId);
    return documents.find(d => d.category_id === catId || children.some(c => c.id === d.category_id));
  };

  return (
    <div className="inline-search" ref={wrapRef} data-testid="inline-search">
      <div className="inline-search-input">
        <Icon name="Search" size={15}/>
        <input data-testid="search-input" placeholder="Search..." value={query} onChange={e => setQuery(e.target.value)} onFocus={() => setFocused(true)} onBlur={() => setTimeout(() => setFocused(false), 200)} />
        {searching && <span className="search-spinner"/>}
        <kbd>Ctrl+K</kbd>
      </div>
      {focused && query.length >= 1 && (
        <div className="inline-search-dropdown" data-testid="search-results">
          {catResults.length > 0 && (
            <div className="search-group">
              <div className="search-group-label">Categories</div>
              {catResults.map(c => (
                <button key={c.id} className="search-result-item" data-testid={`search-cat-${c.id}`} onMouseDown={() => { const doc = getFirstDocInCat(c.id); if (doc) onSelect(doc.id); setQuery(""); }}>
                  <Icon name={c.icon || "FolderOpen"} size={14}/>
                  <div><div className="search-result-title">{c.name}</div><div className="search-result-cat">{c.parent_id ? "Subcategory" : "Category"}</div></div>
                </button>
              ))}
            </div>
          )}
          {results.length > 0 && (
            <div className="search-group">
              {catResults.length > 0 && <div className="search-group-label">Documents</div>}
              {results.map(d => (
                <button key={d.id} className="search-result-item" data-testid={`search-result-${d.id}`} onMouseDown={() => { onSelect(d.id); setQuery(""); }}>
                  <Icon name="FileText" size={14}/>
                  <div>
                    <div className="search-result-title">{d.title}</div>
                    <div className="search-result-cat">{getCatName(d.category_id)}</div>
                    {d.snippet && <div className="search-result-snippet" data-testid="search-snippet">{d.snippet}</div>}
                  </div>
                </button>
              ))}
            </div>
          )}
          {catResults.length === 0 && results.length === 0 && !searching && <div className="search-empty">No results found</div>}
        </div>
      )}
    </div>
  );
}


// --- Document Quiz ---
function DocQuiz({ docId }) {
  const { api } = useAuth();
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    setQuiz(null); setAnswers({}); setSubmitted(false);
    if (docId) api("get", `/documents/${docId}/quiz`).then(r => { if (r.data?.questions?.length > 0) setQuiz(r.data); }).catch(() => {});
  }, [docId, api]);

  if (!quiz || quiz.questions.length === 0) return null;

  const score = quiz.questions.reduce((acc, q) => acc + (answers[q.id] === q.correct ? 1 : 0), 0);
  const total = quiz.questions.length;
  const allAnswered = Object.keys(answers).length === total;

  return (
    <div className="doc-quiz" data-testid="doc-quiz">
      <h3 className="doc-quiz-title"><Icon name="Check" size={18}/> Test Your Understanding</h3>
      {quiz.questions.map((q, qi) => (
        <div key={q.id} className="quiz-question" data-testid={`quiz-q-${qi}`}>
          <p className="quiz-question-text">{qi + 1}. {q.question}</p>
          <div className="quiz-options">
            {q.options.map((opt, oi) => {
              const selected = answers[q.id] === oi;
              const isCorrect = submitted && oi === q.correct;
              const isWrong = submitted && selected && oi !== q.correct;
              return (
                <button key={oi} className={`quiz-option ${selected ? "selected" : ""} ${isCorrect ? "correct" : ""} ${isWrong ? "wrong" : ""}`} data-testid={`quiz-opt-${qi}-${oi}`} onClick={() => { if (!submitted) setAnswers(prev => ({...prev, [q.id]: oi})); }} disabled={submitted}>
                  <span className="quiz-option-letter">{String.fromCharCode(65 + oi)}</span>{opt}
                </button>
              );
            })}
          </div>
          {submitted && answers[q.id] !== undefined && (
            <p className={`quiz-explanation ${answers[q.id] === q.correct ? "correct" : "wrong"}`} data-testid={`quiz-explain-${qi}`}>
              {answers[q.id] === q.correct ? "Correct! " : "Incorrect. "}{q.explanation}
            </p>
          )}
        </div>
      ))}
      <div className="quiz-footer">
        {!submitted ? (
          <button className="editor-btn-primary" data-testid="quiz-submit" onClick={() => setSubmitted(true)} disabled={!allAnswered}>Check Answers ({Object.keys(answers).length}/{total})</button>
        ) : (
          <div className="quiz-result" data-testid="quiz-result">
            <span className="quiz-score">Score: {score}/{total} ({Math.round(score/total*100)}%)</span>
            <button className="editor-btn-secondary" onClick={() => { setAnswers({}); setSubmitted(false); }}>Try Again</button>
          </div>
        )}
      </div>
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
          {isOwn && (
            <button className="comment-action comment-delete" data-testid={`delete-comment-${comment.id}`} onClick={() => deleteComment(comment.id)}>
              <Icon name="Trash" size={13}/>
            </button>
          )}
        </div>
        {replyTo === comment.id && (
          <div className="comment-reply-box">
            <input autoFocus data-testid={`reply-input-${comment.id}`} placeholder="Write a reply..." value={replyText} onChange={e => setReplyText(e.target.value)} onKeyDown={e => { if (e.key === "Enter") submit(replyText, comment.id); }} />
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
function Sidebar({ categories, documents, activeDocId, onSelectDoc, onNewDoc, collapsed, setCollapsed, bookmarkCount, onManageCategories, isAdmin, sidebarWidth, onResizeSidebar }) {
  const [expanded, setExpanded] = useState({});
  const { dark, toggle } = useTheme();
  const { logout, user } = useAuth();
  const navigate = useNavigate();
  const navRef = useRef(null);
  const resizing = useRef(false);
  const currentPath = window.location.pathname;

  const parentCats = categories.filter(c => !c.parent_id && !c.internal).sort((a,b) => a.order - b.order);
  const getChildren = (pid) => categories.filter(c => c.parent_id === pid).sort((a,b) => a.order - b.order);
  const getDocsForCat = (catId) => documents.filter(d => d.category_id === catId).sort((a,b) => a.order - b.order);
  const toggleCat = (id) => setExpanded(p => ({...p, [id]: !p[id]}));

  const handleMouseDown = (e) => {
    e.preventDefault();
    resizing.current = true;
    const move = (ev) => { if (resizing.current) onResizeSidebar(Math.max(200, Math.min(500, ev.clientX))); };
    const up = () => { resizing.current = false; document.removeEventListener("mousemove", move); document.removeEventListener("mouseup", up); };
    document.addEventListener("mousemove", move);
    document.addEventListener("mouseup", up);
  };

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
    <aside className={`sidebar ${collapsed ? "sidebar-collapsed" : ""}`} data-testid="sidebar" style={!collapsed ? {width: sidebarWidth} : undefined}>
      <div className="sidebar-header">
        {!collapsed && <div className="sidebar-brand" data-testid="sidebar-brand"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/><path d="M8 7h6"/><path d="M8 11h4"/></svg><span>Agent Anatomy</span></div>}
        <button className="sidebar-collapse-btn" data-testid="sidebar-collapse-btn" onClick={() => setCollapsed(!collapsed)}><Icon name={collapsed ? "Menu" : "PanelLeft"} size={18}/></button>
      </div>
      {!collapsed && (
        <>
          <InlineSearch categories={categories} documents={documents} onSelect={onSelectDoc} />
          <nav className="sidebar-nav" ref={navRef} data-testid="sidebar-nav">
            <button className={`sidebar-item ${currentPath === "/" && !activeDocId ? "active" : ""}`} data-testid="sidebar-home-btn" onClick={() => navigate("/")}><Icon name="Home" size={16}/><span>Home</span></button>
            <button className={`sidebar-item ${currentPath === "/bookmarks" ? "active" : ""}`} data-testid="sidebar-bookmarks-btn" onClick={() => navigate("/bookmarks")}><Icon name="Bookmark" size={16}/><span>Bookmarks</span>{bookmarkCount > 0 && <span className="sidebar-badge">{bookmarkCount}</span>}</button>
            <button className={`sidebar-item ${currentPath === "/learn" ? "active" : ""}`} data-testid="sidebar-learn-btn" onClick={() => navigate("/learn")}><Icon name="Rocket" size={16}/><span>Learning Paths</span></button>
            <button className={`sidebar-item ${currentPath === "/tools" ? "active" : ""}`} data-testid="sidebar-tools-btn" onClick={() => navigate("/tools")}><Icon name="Monitor" size={16}/><span>Tools</span></button>
            {isAdmin && <button className={`sidebar-item ${currentPath === "/trash" ? "active" : ""}`} data-testid="sidebar-trash-btn" onClick={() => navigate("/trash")}><Icon name="Undo" size={16}/><span>Trash</span></button>}
            {isAdmin && <button className={`sidebar-item ${currentPath === "/settings" ? "active" : ""}`} data-testid="sidebar-settings-btn" onClick={() => navigate("/settings")}><Icon name="Users" size={16}/><span>Settings</span></button>}
            {isAdmin && <button className={`sidebar-item ${currentPath === "/analytics" ? "active" : ""}`} data-testid="sidebar-analytics-btn" onClick={() => navigate("/analytics")}><Icon name="BarChart" size={16}/><span>Analytics</span></button>}
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
      {!collapsed && <div className="sidebar-resize" data-testid="sidebar-resize" onMouseDown={handleMouseDown} />}
    </aside>
  );
}

// --- TOC with Scroll Spy ---
function TocScrollSpy({ headings }) {
  const [activeId, setActiveId] = useState("");
  useEffect(() => {
    const main = document.querySelector('.main-content');
    if (!main) return;
    const handler = () => {
      let current = "";
      for (const h of headings) {
        const el = document.getElementById(h.id);
        if (el) {
          const rect = el.getBoundingClientRect();
          if (rect.top <= 150) current = h.id;
        }
      }
      setActiveId(current);
    };
    main.addEventListener('scroll', handler);
    handler();
    return () => main.removeEventListener('scroll', handler);
  }, [headings]);
  return (
    <div className="doc-toc" data-testid="doc-toc">
      <div className="doc-toc-title">On this page</div>
      {headings.map((h, i) => (
        <a key={i} href={`#${h.id}`} className={`doc-toc-link ${activeId === h.id ? "toc-active" : ""}`}>{h.text}</a>
      ))}
    </div>
  );
}

// --- Presence Avatars ---
function PresenceAvatars({ users, identity }) {
  const others = users.filter(u => u.user_id !== identity?.id);
  if (others.length === 0) return null;
  return (
    <div className="presence-avatars" data-testid="presence-avatars">
      {others.map(u => (
        <div key={u.user_id} className="presence-avatar" data-testid={`presence-${u.user_id}`} style={{ borderColor: u.color, backgroundColor: u.color + "22" }} title={`${u.name} (${u.mode})`}>
          <span style={{ color: u.color }}>{u.name[0]?.toUpperCase()}</span>
          {u.mode === "editing" && <span className="presence-editing-dot" />}
        </div>
      ))}
      <span className="presence-label">{others.length} {others.length === 1 ? "viewer" : "viewers"}</span>
    </div>
  );
}


function DocNavigation({ currentDoc, documents, categories, onSelect }) {
  if (!currentDoc || !documents?.length) return null;
  // Get docs in the same category, sorted by order
  const sameCat = documents.filter(d => d.category_id === currentDoc.category_id).sort((a,b) => (a.order || 0) - (b.order || 0));
  const idx = sameCat.findIndex(d => d.id === currentDoc.id);
  const prev = idx > 0 ? sameCat[idx - 1] : null;
  const next = idx < sameCat.length - 1 ? sameCat[idx + 1] : null;
  // If no prev/next in same category, try adjacent categories
  const parentCats = categories.filter(c => !c.parent_id && !c.internal).sort((a,b) => a.order - b.order);
  const allCatIds = [];
  parentCats.forEach(pc => { allCatIds.push(pc.id); categories.filter(c => c.parent_id === pc.id).sort((a,b) => a.order - b.order).forEach(sc => allCatIds.push(sc.id)); });
  if (!prev || !next) {
    const catIdx = allCatIds.indexOf(currentDoc.category_id);
    if (!prev && catIdx > 0) {
      for (let i = catIdx - 1; i >= 0; i--) {
        const prevCatDocs = documents.filter(d => d.category_id === allCatIds[i]).sort((a,b) => (a.order || 0) - (b.order || 0));
        if (prevCatDocs.length > 0) { var prevDoc = prevCatDocs[prevCatDocs.length - 1]; break; }
      }
    }
    if (!next && catIdx < allCatIds.length - 1) {
      for (let i = catIdx + 1; i < allCatIds.length; i++) {
        const nextCatDocs = documents.filter(d => d.category_id === allCatIds[i]).sort((a,b) => (a.order || 0) - (b.order || 0));
        if (nextCatDocs.length > 0) { var nextDoc = nextCatDocs[0]; break; }
      }
    }
  }
  const prevFinal = prev || prevDoc;
  const nextFinal = next || nextDoc;
  if (!prevFinal && !nextFinal) return null;
  return (
    <div className="doc-nav" data-testid="doc-navigation">
      {prevFinal ? <button className="doc-nav-btn doc-nav-prev" data-testid="nav-prev" onClick={() => onSelect(prevFinal.id)}><Icon name="ArrowLeft" size={14}/><div><span className="doc-nav-label">Previous</span><span className="doc-nav-title">{prevFinal.title}</span></div></button> : <div/>}
      {nextFinal ? <button className="doc-nav-btn doc-nav-next" data-testid="nav-next" onClick={() => onSelect(nextFinal.id)}><div><span className="doc-nav-label">Next</span><span className="doc-nav-title">{nextFinal.title}</span></div><Icon name="ChevronRight" size={14}/></button> : <div/>}
    </div>
  );
}


function RelatedDocs({ currentDoc, categories, documents, onSelect }) {
  if (!currentDoc || !documents?.length) return null;
  const siblings = documents.filter(d => d.category_id === currentDoc.category_id && d.id !== currentDoc.id);
  // Also find docs from parent category
  const currentCat = categories?.find(c => c.id === currentDoc.category_id);
  const parentId = currentCat?.parent_id;
  const cousins = parentId ? documents.filter(d => {
    if (d.id === currentDoc.id) return false;
    const dCat = categories?.find(c => c.id === d.category_id);
    return dCat?.parent_id === parentId && d.category_id !== currentDoc.category_id;
  }) : [];
  const related = [...siblings, ...cousins.slice(0, 3)].slice(0, 5);
  if (related.length === 0) return null;
  const getCatName = (id) => categories?.find(c => c.id === id)?.name || "";
  return (
    <div className="related-docs" data-testid="related-docs">
      <h3 className="related-docs-title">Related Documents</h3>
      <div className="related-docs-list">
        {related.map(d => (
          <button key={d.id} className="related-doc-item" data-testid={`related-${d.id}`} onClick={() => onSelect(d.id)}>
            <Icon name="FileText" size={15}/><div><span className="related-doc-name">{d.title}</span><span className="related-doc-cat">{getCatName(d.category_id)}</span></div>
          </button>
        ))}
      </div>
    </div>
  );
}

// --- Document Viewer ---
function DocumentViewer({ doc, category, parentCategory, isBookmarked, onToggleBookmark, onEdit, onDelete, isAdmin, onNavigateHome, categories, documents, onSelectDoc }) {
  const { api } = useAuth();
  const [versions, setVersions] = useState([]);
  const [showVersions, setShowVersions] = useState(false);
  const [viewingVersion, setViewingVersion] = useState(null);
  const [exporting, setExporting] = useState(false);
  const [shareId, setShareId] = useState(doc?.share_id || null);
  const [copied, setCopied] = useState(false);
  const [showShare, setShowShare] = useState(false);
  const contentRef = useRef(null);
  const { users, identity } = useCollaboration(doc?.id, !!doc);

  // Track document view
  useEffect(() => {
    if (doc?.id) api("post", `/documents/${doc.id}/view`).catch(() => {});
  }, [doc?.id, api]);

  useEffect(() => { setShowVersions(false); setViewingVersion(null); setVersions([]); setShareId(doc?.share_id || null); setShowShare(false); }, [doc?.id, doc?.share_id]);

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
      alert("PDF exported successfully!");
    } catch (e) { console.error("PDF export error:", e); alert("PDF export failed. Please try again."); }
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
  const headings = (() => {
    const raw = displayContent?.match(/^## .+/gm)?.map(h => ({ text: h.slice(3), id: h.slice(3).toLowerCase().replace(/[^a-z0-9]+/g, "-") })) || [];
    const seen = new Set();
    return raw.filter(h => { if (seen.has(h.id)) return false; seen.add(h.id); return true; });
  })();
  const tags = doc.tags || [];

  return (
    <div className="doc-viewer" data-testid="doc-viewer">
      <div className="doc-breadcrumb" data-testid="doc-breadcrumb">
        {parentCategory && <><button className="doc-breadcrumb-link" onClick={onNavigateHome}>{parentCategory.name}</button><Icon name="ChevronRight" size={14}/></>}
        {category && <><button className="doc-breadcrumb-link" onClick={onNavigateHome}>{category.name}</button><Icon name="ChevronRight" size={14}/></>}
        <span className="doc-breadcrumb-active">{doc.title}</span>
      </div>
      <div className="doc-header">
        <div>
          <h1 className="doc-title" data-testid="doc-title">{viewingVersion ? `${doc.title} (version)` : doc.title}</h1>
          <div className="doc-meta" data-testid="doc-meta">
            <span className="doc-meta-item"><Icon name="Clock" size={12}/> {Math.max(1, Math.ceil((doc.content?.split(/\s+/).length || 0) / 200))} min read</span>
            {doc.updated_at && <span className="doc-meta-item">Updated {new Date(doc.updated_at).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}</span>}
          </div>
          {tags.length > 0 && <div className="doc-tags" data-testid="doc-tags">{tags.map((t, i) => <span key={i} className="doc-tag"><Icon name="Tag" size={11}/>{t}</span>)}</div>}
        </div>
        <div className="doc-actions">
          <PresenceAvatars users={users} identity={identity} />
          {viewingVersion && <button data-testid="version-back-btn" className="doc-action-btn" onClick={() => setViewingVersion(null)} title="Back to current"><Icon name="ArrowLeft" size={18}/></button>}
          <button data-testid="export-pdf-btn" className="doc-action-btn" onClick={exportPDF} title="Export as PDF" disabled={exporting}><Icon name="Download" size={18}/></button>
          <button data-testid="version-history-btn" className="doc-action-btn" onClick={loadVersions} title="Version history"><Icon name="Clock" size={18}/></button>
          {isAdmin && <button data-testid="share-toggle-btn" className="doc-action-btn" onClick={() => setShowShare(true)} title="Share settings"><Icon name="Share" size={18}/></button>}
          <button data-testid="bookmark-toggle-btn" className={`doc-action-btn ${isBookmarked ? "bookmarked" : ""}`} onClick={onToggleBookmark}><Icon name={isBookmarked ? "BookmarkFilled" : "Bookmark"} size={18}/></button>
          {isAdmin && <button data-testid="edit-doc-btn" className="doc-action-btn" onClick={onEdit}><Icon name="Edit" size={18}/></button>}
          {isAdmin && <button data-testid="delete-doc-btn" className="doc-action-btn doc-action-danger" onClick={onDelete}><Icon name="Trash" size={18}/></button>}
        </div>
      </div>
      <div className="doc-layout">
        <article className="doc-content" data-testid="doc-content">
          <div ref={contentRef} className="doc-content-inner">
            {doc.cover_image && <div className="doc-cover-image" data-testid="doc-cover"><img src={doc.cover_image} alt="" /></div>}
            <MarkdownContent content={displayContent} currentDocId={doc?.id} />
          </div>
          <DocNavigation currentDoc={doc} documents={documents} categories={categories} onSelect={onSelectDoc} />
          <RelatedDocs currentDoc={doc} categories={categories} documents={documents} onSelect={onSelectDoc} />
          <DocQuiz docId={doc.id} />
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
              {viewingVersion && <button className="editor-btn-primary" data-testid="restore-version-btn" style={{width:"100%",marginTop:8}} onClick={async () => { try { const r = await api("post", `/documents/${doc.id}/versions/${viewingVersion.id}/restore`); window.location.reload(); } catch { alert("Failed to restore version"); } }}>Restore this version</button>}
              <button className="doc-version-close" data-testid="version-close-btn" onClick={() => { setShowVersions(false); setViewingVersion(null); }}>Close</button>
            </div>
          )}
          {headings.length > 2 && !showVersions && (
            <TocScrollSpy headings={headings} />
          )}
        </aside>
      </div>
      {showShare && (
        <div className="search-overlay" onClick={() => setShowShare(false)} data-testid="share-dialog-overlay">
          <div className="share-dialog" onClick={e => e.stopPropagation()} data-testid="share-dialog">
            <div className="catmgr-header"><h2>Share Settings</h2><button className="catmgr-close" onClick={() => setShowShare(false)}><Icon name="X" size={18}/></button></div>
            <div className="share-dialog-body">
              {shareId ? (
                <>
                  <p className="share-status active">Public sharing is <strong>enabled</strong></p>
                  <div className="share-link-row">
                    <input readOnly value={`${window.location.origin}/share/${shareId}`} className="share-link-input" data-testid="share-link-input" />
                    <button className="editor-btn-primary" data-testid="copy-share-link" onClick={copyShareLink}>{copied ? "Copied!" : "Copy"}</button>
                  </div>
                  <button className="editor-btn-secondary share-disable-btn" data-testid="disable-sharing-btn" onClick={async () => { await toggleShare(); }}>Disable sharing</button>
                </>
              ) : (
                <>
                  <p className="share-status">Public sharing is <strong>disabled</strong></p>
                  <p className="share-desc">Enable sharing to generate a public link anyone can view without signing in.</p>
                  <button className="editor-btn-primary" data-testid="enable-sharing-btn" onClick={async () => { await toggleShare(); }}>Enable public sharing</button>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// --- Document Editor (Collaborative) ---
function DocumentEditor({ doc, categories, onSave, onCancel }) {
  const { api } = useAuth();
  const [title, setTitle] = useState(doc?.title || "");
  const [content, setContent] = useState(doc?.content || "");
  const [categoryId, setCategoryId] = useState(doc?.category_id || "");
  const [saving, setSaving] = useState(false);
  const [showPreview, setShowPreview] = useState(true);
  const [tags, setTags] = useState(doc?.tags || []);
  const [tagInput, setTagInput] = useState("");
  const [tagSuggestions, setTagSuggestions] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [showTemplates, setShowTemplates] = useState(!doc);
  const [autoSaveStatus, setAutoSaveStatus] = useState(null); // null | "saving" | "saved"
  const textareaRef = useRef(null);
  const autoSaveTimer = useRef(null);
  const lastSavedContent = useRef(doc?.content || "");
  const subCats = categories.filter(c => c.parent_id);

  // Collaboration
  const { users, remoteContent, saved, identity, sendContent, sendMode, sendSave } = useCollaboration(doc?.id, !!doc);
  const otherEditors = users.filter(u => u.user_id !== identity?.id);
  const editingUsers = otherEditors.filter(u => u.mode === "editing");

  // Notify server we're editing
  useEffect(() => {
    sendMode("editing");
    return () => sendMode("viewing");
  }, [sendMode]);

  // Receive remote content updates
  useEffect(() => {
    if (!remoteContent || remoteContent.senderId === identity?.id) return;
    const ta = textareaRef.current;
    const cursorPos = ta?.selectionStart || 0;
    setContent(remoteContent.content);
    // Restore cursor position after remote update
    requestAnimationFrame(() => {
      if (ta) { ta.selectionStart = cursorPos; ta.selectionEnd = cursorPos; }
    });
  }, [remoteContent, identity?.id]);

  // Show "saved by someone else" notification
  useEffect(() => {
    if (saved && saved.senderId !== identity?.id) {
      setAutoSaveStatus("saved");
      setTimeout(() => setAutoSaveStatus(null), 2000);
    }
  }, [saved, identity?.id]);

  // Auto-save with debounce (only for existing docs)
  useEffect(() => {
    if (!doc) return;
    if (content === lastSavedContent.current) return;
    clearTimeout(autoSaveTimer.current);
    autoSaveTimer.current = setTimeout(() => {
      setAutoSaveStatus("saving");
      sendSave(content, title);
      lastSavedContent.current = content;
      setTimeout(() => setAutoSaveStatus("saved"), 500);
      setTimeout(() => setAutoSaveStatus(null), 2500);
    }, 3000);
    return () => clearTimeout(autoSaveTimer.current);
  }, [content, title, doc, sendSave]);

  useEffect(() => {
    if (!doc) api("get", "/templates").then(r => setTemplates(r.data)).catch(() => {});
  }, [api, doc]);

  const applyTemplate = (t) => { setTitle(t.name); setContent(t.content); setShowTemplates(false); };

  const handleContentChange = (e) => {
    const val = e.target.value;
    setContent(val);
    sendContent(val, e.target.selectionStart);
  };

  const handleSave = async () => {
    if (!title.trim() || !categoryId) return;
    setSaving(true);
    clearTimeout(autoSaveTimer.current);
    await onSave({ title, content, category_id: categoryId, tags });
    lastSavedContent.current = content;
    setSaving(false);
  };
  const addTag = () => { const t = tagInput.trim().toLowerCase(); if (t && !tags.includes(t)) setTags([...tags, t]); setTagInput(""); setTagSuggestions([]); };
  const removeTag = (t) => setTags(tags.filter(x => x !== t));

  const onTagInputChange = async (val) => {
    setTagInput(val);
    if (val.length >= 1) {
      try { const r = await api("get", `/tags/suggestions?q=${encodeURIComponent(val)}`); setTagSuggestions(r.data.filter(t => !tags.includes(t))); } catch {}
    } else { setTagSuggestions([]); }
  };

  return (
    <div className="doc-editor" data-testid="doc-editor">
      {/* Collaboration Banner */}
      {doc && (
        <div className="collab-banner" data-testid="collab-banner">
          <div className="collab-banner-left">
            <Icon name="Wifi" size={14}/>
            <span className="collab-live-dot" />
            <span>Live editing</span>
            {editingUsers.length > 0 && (
              <span className="collab-editors-info">
                {editingUsers.map(u => u.name).join(", ")} also editing
              </span>
            )}
          </div>
          <div className="collab-banner-right">
            {otherEditors.length > 0 && (
              <div className="collab-mini-avatars">
                {otherEditors.slice(0, 5).map(u => (
                  <div key={u.user_id} className="collab-mini-avatar" style={{ backgroundColor: u.color }} title={u.name}>
                    {u.name[0]?.toUpperCase()}
                  </div>
                ))}
                {otherEditors.length > 5 && <span className="collab-more">+{otherEditors.length - 5}</span>}
              </div>
            )}
            {autoSaveStatus === "saving" && <span className="collab-save-status" data-testid="autosave-saving">Saving...</span>}
            {autoSaveStatus === "saved" && <span className="collab-save-status saved" data-testid="autosave-saved"><Icon name="Check" size={12}/>Saved</span>}
          </div>
        </div>
      )}
      {showTemplates && templates.length > 0 && !doc && (
        <div className="template-picker" data-testid="template-picker">
          <div className="template-picker-header">
            <h3>Start from a template</h3>
            <button className="catmgr-close" onClick={() => setShowTemplates(false)}><Icon name="X" size={16}/></button>
          </div>
          <div className="template-grid">
            <button className="template-card" data-testid="template-blank" onClick={() => setShowTemplates(false)}>
              <Icon name="FileText" size={24}/><span>Blank page</span>
            </button>
            {templates.map(t => (
              <button key={t.id} className="template-card" data-testid={`template-${t.id}`} onClick={() => applyTemplate(t)}>
                <Icon name={t.icon} size={24}/><span>{t.name}</span>
              </button>
            ))}
          </div>
        </div>
      )}
      <div className="editor-header">
        <h2>{doc ? "Edit page" : "New page"}</h2>
        <div className="editor-actions">
          {!doc && <button data-testid="editor-templates-btn" className="editor-btn-toggle" onClick={() => setShowTemplates(!showTemplates)}><Icon name="Layers" size={14}/><span>Templates</span></button>}
          <button data-testid="editor-preview-toggle" className={`editor-btn-toggle ${showPreview ? "active" : ""}`} onClick={() => setShowPreview(!showPreview)}><Icon name="Monitor" size={14}/><span>{showPreview ? "Hide preview" : "Show preview"}</span></button>
          <button data-testid="editor-cancel-btn" className="editor-btn-secondary" onClick={onCancel}>Cancel</button>
          <button data-testid="editor-save-btn" className="editor-btn-primary" onClick={handleSave} disabled={saving || !title.trim() || !categoryId}><Icon name="Save" size={14}/>{saving ? "Saving..." : "Save"}</button>
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
        <div className="tag-input-wrap">
          <input data-testid="editor-tag-input" className="editor-tag-input" placeholder="Add tag..." value={tagInput} onChange={e => onTagInputChange(e.target.value)} onKeyDown={e => { if (e.key === "Enter") { e.preventDefault(); addTag(); }}} />
          {tagSuggestions.length > 0 && (
            <div className="tag-suggestions" data-testid="tag-suggestions">
              {tagSuggestions.map(s => <button key={s} className="tag-suggestion" onClick={() => { setTags([...tags, s]); setTagInput(""); setTagSuggestions([]); }}>{s}</button>)}
            </div>
          )}
        </div>
      </div>
      <div className={`editor-split ${showPreview ? "editor-split-active" : ""}`}>
        <textarea ref={textareaRef} data-testid="editor-content-textarea" className="editor-textarea" placeholder="Write in markdown..." value={content} onChange={handleContentChange} />
        {showPreview && <div className="editor-preview" data-testid="editor-preview"><div className="editor-preview-header">Preview</div><div className="editor-preview-content">{title && <h1 className="doc-title" style={{marginBottom:"1rem"}}>{title}</h1>}<MarkdownContent content={content} />{!content && <p className="editor-preview-empty">Start typing to see preview...</p>}</div></div>}
      </div>
    </div>
  );
}

// --- Home / Dashboard ---
function HomePage({ categories, documents, onSelectDoc }) {
  const parentCats = categories.filter(c => !c.parent_id && !c.internal).sort((a,b) => a.order - b.order);
  const getChildCount = (catId) => { const children = categories.filter(c => c.parent_id === catId); return documents.filter(d => d.category_id === catId || children.some(c => c.id === d.category_id)).length; };

  return (
    <div className="home-page" data-testid="home-page">
      <div className="home-hero"><h1>Agent Anatomy</h1><p>The definitive guide to AI agents — architecture, orchestration, LLMs, tooling, and the infrastructure that powers them.</p></div>
      <div className="home-grid">{parentCats.map(cat => (
        <button key={cat.id} className="home-card" data-testid={`home-card-${cat.id}`} onClick={() => {
          const firstDoc = documents.find(d => { const children = categories.filter(c => c.parent_id === cat.id); return d.category_id === cat.id || children.some(c => c.id === d.category_id); });
          if (firstDoc) onSelectDoc(firstDoc.id);
        }}>
          {cat.cover_image && <div className="home-card-cover" style={{backgroundImage: `url(${cat.cover_image})`}} />}
          <div className="home-card-body"><div className="home-card-icon"><Icon name={cat.icon} size={24}/></div><h3>{cat.name}</h3><p className="home-card-count">{getChildCount(cat.id)} documents</p></div>
        </button>
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
function TrashPage({ onDocumentsChanged }) {
  const { api } = useAuth();
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { api("get", "/trash").then(r => setDocs(r.data)).catch(() => {}).finally(() => setLoading(false)); }, [api]);
  const restore = async (id) => { try { await api("post", `/trash/${id}/restore`); setDocs(prev => prev.filter(d => d.id !== id)); if (onDocumentsChanged) onDocumentsChanged(); } catch {} };
  const permDelete = async (id) => { if (!window.confirm("Permanently delete? This cannot be undone.")) return; try { await api("delete", `/trash/${id}`); setDocs(prev => prev.filter(d => d.id !== id)); } catch {} };
  if (loading) return <div className="edh-loading"><div className="edh-spinner"/></div>;
  return (
    <div className="bookmarks-page" data-testid="trash-page">
      <h1>Trash</h1>
      {docs.length === 0 ? <div className="doc-empty"><Icon name="Trash" size={48}/><h2>Trash is empty</h2><p>Deleted documents will appear here.</p></div>
      : <div className="bookmarks-list">{docs.map(d => (
        <div key={d.id} className="bookmark-item" data-testid={`trash-item-${d.id}`}>
          <div className="bookmark-item-content"><Icon name="FileText" size={18}/><div><div className="bookmark-title">{d.title}</div><div className="bookmark-cat">Deleted {d.deleted_at ? new Date(d.deleted_at).toLocaleDateString() : ""}</div></div></div>
          <button className="trash-restore-btn" data-testid={`restore-${d.id}`} onClick={() => restore(d.id)}><Icon name="Undo" size={14}/> Restore</button>
        </div>
      ))}</div>}
    </div>
  );
}

// --- Tools & Resources Page ---
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

  const del = async (id) => { if (!window.confirm("Delete this resource?")) return; try { await api("delete", `/tools/${id}`); setTools(prev => prev.filter(t => t.id !== id)); } catch {} };

  const categories = [...new Set(tools.map(t => t.category))].sort();
  const getDomain = (url) => { try { return new URL(url).hostname.replace("www.", ""); } catch { return ""; } };
  const getFavicon = (url) => { try { const domain = new URL(url).origin; return `https://www.google.com/s2/favicons?domain=${domain}&sz=32`; } catch { return ""; } };

  if (loading) return <div className="edh-loading"><div className="edh-spinner"/></div>;
  return (
    <div className="tools-page" data-testid="tools-page">
      <div className="tools-header">
        <div>
          <h1><Icon name="Link" size={28}/> Tools & Resources</h1>
          <p className="tools-subtitle">Useful links, documentation, and resources for the team</p>
        </div>
        {isAdmin && <button className="editor-btn-primary" data-testid="add-tool-btn" onClick={() => { setAdding(true); setEditId(null); setForm({ name: "", url: "", description: "", category: "General" }); }}><Icon name="Plus" size={14}/> Add New Link</button>}
      </div>
      {(adding || editId) && (
        <div className="tools-form-card" data-testid="tool-form">
          <h3>{editId ? "Edit Resource" : "Add New Resource"}</h3>
          <div className="tools-form-grid">
            <div className="tools-form-field"><label>Name</label><input data-testid="tool-name" placeholder="e.g., FastAPI Documentation" value={form.name} onChange={e => setForm({...form, name: e.target.value})} /></div>
            <div className="tools-form-field"><label>URL</label><input data-testid="tool-url" placeholder="https://fastapi.tiangolo.com" value={form.url} onChange={e => setForm({...form, url: e.target.value})} /></div>
            <div className="tools-form-field"><label>Description</label><input data-testid="tool-desc" placeholder="Brief description" value={form.description} onChange={e => setForm({...form, description: e.target.value})} /></div>
          </div>
          {form.url && <div className="tools-form-preview"><img src={getFavicon(form.url)} alt="" width="16" height="16" onError={e => e.target.style.display='none'} /><span>{getDomain(form.url)}</span></div>}
          <div className="tools-form-actions"><button className="editor-btn-primary" data-testid="tool-save-btn" onClick={save} disabled={!form.name.trim() || !form.url.trim()}>Save</button><button className="editor-btn-secondary" onClick={() => { setAdding(false); setEditId(null); }}>Cancel</button></div>
        </div>
      )}
      <div className="tools-grid">
        {tools.map(t => (
          <div key={t.id} className="tools-card" data-testid={`tool-${t.id}`}>
            <div className="tools-card-header"><img src={getFavicon(t.url)} alt="" width="20" height="20" className="tools-card-favicon" onError={e => e.target.style.display='none'} /><a href={t.url} target="_blank" rel="noreferrer" className="tools-card-name">{t.name}</a></div>
            {t.description && <p className="tools-card-desc">{t.description}</p>}
            <div className="tools-card-footer">
              <span className="tools-card-domain"><Icon name="Link" size={12}/> {getDomain(t.url)}</span>
              {isAdmin && <div className="tools-card-actions"><button data-testid={`edit-tool-${t.id}`} onClick={() => { setEditId(t.id); setAdding(false); setForm({ name: t.name, url: t.url, description: t.description, category: t.category }); }}><Icon name="Edit" size={13}/></button><button data-testid={`delete-tool-${t.id}`} onClick={() => del(t.id)}><Icon name="Trash" size={13}/></button></div>}
            </div>
          </div>
        ))}
      </div>
      {tools.length === 0 && !adding && <div className="doc-empty"><Icon name="Link" size={48}/><h2>No resources yet</h2><p>{isAdmin ? "Add useful links and resources using the button above." : "Resources will appear here when added."}</p></div>}
    </div>
  );
}

// --- Analytics Dashboard ---
function AnalyticsPage() {
  const { api } = useAuth();
  const [overview, setOverview] = useState(null);
  const [popular, setPopular] = useState([]);
  const [searches, setSearches] = useState([]);
  const [chatbot, setChatbot] = useState(null);
  const [activity, setActivity] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [ov, pop, srch, chat, act] = await Promise.all([
          api("get", "/analytics/overview"),
          api("get", "/analytics/popular-docs"),
          api("get", "/analytics/searches"),
          api("get", "/analytics/chatbot"),
          api("get", "/analytics/activity"),
        ]);
        setOverview(ov.data); setPopular(pop.data); setSearches(srch.data);
        setChatbot(chat.data); setActivity(act.data);
      } catch (e) { console.error("Analytics load error:", e); }
      setLoading(false);
    };
    load();
  }, [api]);

  if (loading) return <div className="edh-loading"><div className="edh-spinner"/></div>;

  const maxViews = popular.length > 0 ? popular[0].views : 1;

  return (
    <div className="analytics-page" data-testid="analytics-page">
      <div className="analytics-header">
        <h1><Icon name="BarChart" size={28}/> Analytics Dashboard</h1>
        <p className="analytics-subtitle">Insights on document views, search trends, and chatbot usage</p>
      </div>

      {/* Overview Cards */}
      <div className="analytics-cards" data-testid="analytics-overview">
        <div className="analytics-card">
          <div className="analytics-card-icon" style={{background: "rgba(99,102,241,0.12)", color: "#6366f1"}}><Icon name="FileText" size={20}/></div>
          <div className="analytics-card-data"><span className="analytics-card-value">{overview?.total_docs || 0}</span><span className="analytics-card-label">Documents</span></div>
        </div>
        <div className="analytics-card">
          <div className="analytics-card-icon" style={{background: "rgba(34,197,94,0.12)", color: "#22c55e"}}><Icon name="Eye" size={20}/></div>
          <div className="analytics-card-data"><span className="analytics-card-value">{overview?.total_views || 0}</span><span className="analytics-card-label">Total Views</span></div>
        </div>
        <div className="analytics-card">
          <div className="analytics-card-icon" style={{background: "rgba(249,115,22,0.12)", color: "#f97316"}}><Icon name="Search" size={20}/></div>
          <div className="analytics-card-data"><span className="analytics-card-value">{overview?.total_searches || 0}</span><span className="analytics-card-label">Searches</span></div>
        </div>
        <div className="analytics-card">
          <div className="analytics-card-icon" style={{background: "rgba(236,72,153,0.12)", color: "#ec4899"}}><Icon name="MessageSquare" size={20}/></div>
          <div className="analytics-card-data"><span className="analytics-card-value">{overview?.total_chats || 0}</span><span className="analytics-card-label">AI Chats</span></div>
        </div>
        <div className="analytics-card">
          <div className="analytics-card-icon" style={{background: "rgba(14,165,233,0.12)", color: "#0ea5e9"}}><Icon name="TrendingUp" size={20}/></div>
          <div className="analytics-card-data"><span className="analytics-card-value">{overview?.views_7d || 0}</span><span className="analytics-card-label">Views (7d)</span></div>
        </div>
        <div className="analytics-card">
          <div className="analytics-card-icon" style={{background: "rgba(168,85,247,0.12)", color: "#a855f7"}}><Icon name="MessageSquare" size={20}/></div>
          <div className="analytics-card-data"><span className="analytics-card-value">{overview?.chats_7d || 0}</span><span className="analytics-card-label">Chats (7d)</span></div>
        </div>
      </div>

      <div className="analytics-grid">
        {/* Popular Documents */}
        <div className="analytics-section" data-testid="popular-docs">
          <h2 className="analytics-section-title"><Icon name="TrendingUp" size={18}/> Most Viewed Documents</h2>
          {popular.length === 0 ? <p className="analytics-empty">No view data yet. Views are tracked as users read documents.</p> : (
            <div className="analytics-bar-chart">
              {popular.map((d, i) => (
                <div key={d.doc_id} className="analytics-bar-row" data-testid={`popular-doc-${i}`}>
                  <span className="analytics-bar-rank">#{i + 1}</span>
                  <span className="analytics-bar-title">{d.title}</span>
                  <div className="analytics-bar-track">
                    <div className="analytics-bar-fill" style={{width: `${(d.views / maxViews) * 100}%`}} />
                  </div>
                  <span className="analytics-bar-count">{d.views}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Search Queries */}
        <div className="analytics-section" data-testid="search-analytics">
          <h2 className="analytics-section-title"><Icon name="Search" size={18}/> Top Search Queries</h2>
          {searches.length === 0 ? <p className="analytics-empty">No searches yet.</p> : (
            <div className="analytics-table">
              <div className="analytics-table-header"><span>Query</span><span>Count</span><span>Last Searched</span></div>
              {searches.map((s, i) => (
                <div key={i} className="analytics-table-row" data-testid={`search-query-${i}`}>
                  <span className="analytics-query">{s.query}</span>
                  <span className="analytics-count">{s.count}</span>
                  <span className="analytics-date">{s.last_searched ? new Date(s.last_searched).toLocaleDateString() : ""}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Chatbot Usage */}
        <div className="analytics-section" data-testid="chatbot-analytics">
          <h2 className="analytics-section-title"><Icon name="MessageSquare" size={18}/> AI Chatbot Usage</h2>
          {chatbot && chatbot.daily?.length > 0 ? (
            <>
              <div className="analytics-mini-chart">
                {chatbot.daily.map((d, i) => (
                  <div key={i} className="analytics-mini-bar-col" data-testid={`chat-day-${i}`}>
                    <div className="analytics-mini-bar" style={{height: `${Math.max(4, (d.count / Math.max(...chatbot.daily.map(x => x.count))) * 80)}px`}} />
                    <span className="analytics-mini-label">{d.date.slice(5)}</span>
                  </div>
                ))}
              </div>
              {chatbot.recent?.length > 0 && (
                <div className="analytics-recent-questions">
                  <h3>Recent Questions</h3>
                  {chatbot.recent.slice(0, 5).map((q, i) => (
                    <div key={i} className="analytics-question-item" data-testid={`recent-question-${i}`}>
                      <Icon name="MessageSquare" size={13}/>
                      <span>{q.question}</span>
                      <span className="analytics-date">{q.asked_at ? new Date(q.asked_at).toLocaleDateString() : ""}</span>
                    </div>
                  ))}
                </div>
              )}
            </>
          ) : <p className="analytics-empty">No chatbot conversations yet.</p>}
        </div>

        {/* Recent Activity */}
        <div className="analytics-section" data-testid="recent-activity">
          <h2 className="analytics-section-title"><Icon name="Clock" size={18}/> Recent Activity</h2>
          {activity?.recent_docs?.length > 0 ? (
            <div className="analytics-activity-list">
              {activity.recent_docs.map((d, i) => (
                <div key={i} className="analytics-activity-item" data-testid={`activity-${i}`}>
                  <Icon name="FileText" size={14}/>
                  <span className="analytics-activity-title">{d.title}</span>
                  <span className="analytics-date">{d.updated_at ? new Date(d.updated_at).toLocaleDateString() : ""}</span>
                </div>
              ))}
            </div>
          ) : <p className="analytics-empty">No recent activity.</p>}
          {activity?.recent_comments?.length > 0 && (
            <div className="analytics-activity-list" style={{marginTop: 12}}>
              <h3 style={{fontSize: "0.8rem", color: "var(--text-muted)", marginBottom: 8}}>Recent Comments</h3>
              {activity.recent_comments.slice(0, 5).map((c, i) => (
                <div key={i} className="analytics-activity-item">
                  <Icon name="MessageSquare" size={14}/>
                  <span className="analytics-activity-title">{c.user_name}: {c.content?.slice(0, 60)}</span>
                  <span className="analytics-date">{c.created_at ? new Date(c.created_at).toLocaleDateString() : ""}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// --- Settings / Invite Page ---
function SettingsPage({ isAdmin }) {
  const { api } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [inviteEmail, setInviteEmail] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    if (!isAdmin) return;
    api("get", "/users").then(r => setUsers(r.data)).catch(() => {}).finally(() => setLoading(false));
  }, [api, isAdmin]);

  const invite = async () => {
    if (!inviteEmail.trim()) return;
    setError("");
    try {
      const r = await api("post", "/invite", { email: inviteEmail.trim(), role: "viewer" });
      setUsers(prev => [...prev, r.data]);
      setInviteEmail("");
      setSuccess("Invitation sent!");
      setTimeout(() => setSuccess(""), 3000);
    } catch (e) { setError(e.response?.data?.detail || "Failed to invite"); }
  };

  const removeUser = async (userId) => {
    if (!window.confirm("Remove this user?")) return;
    setError("");
    try {
      await api("delete", `/users/${userId}`);
      setUsers(prev => prev.filter(u => u.user_id !== userId));
      setSuccess("User removed");
      setTimeout(() => setSuccess(""), 3000);
    } catch (e) { setError(e.response?.data?.detail || "Cannot remove"); }
  };

  if (!isAdmin) return <div className="doc-empty"><Icon name="Lock" size={48}/><h2>Admin Only</h2></div>;
  if (loading) return <div className="edh-loading"><div className="edh-spinner"/></div>;

  return (
    <div className="bookmarks-page" data-testid="settings-page">
      <h1>Team</h1>
      <div className="settings-section">
        <h2 className="settings-section-title">Invite People</h2>
        {error && <div className="auth-error">{error}</div>}
        {success && <div className="auth-error" style={{background: "var(--accent-light)", color: "var(--accent)", borderColor: "var(--accent)"}}>{success}</div>}
        <div className="invite-row" data-testid="invite-row">
          <input data-testid="invite-email" type="email" placeholder="Email address" value={inviteEmail} onChange={e => setInviteEmail(e.target.value)} onKeyDown={e => { if (e.key === "Enter") invite(); }} />
          <button className="editor-btn-primary" data-testid="invite-btn" onClick={invite} disabled={!inviteEmail.trim()}>Invite</button>
        </div>
      </div>
      <div className="settings-section">
        <h2 className="settings-section-title">Members ({users.length})</h2>
        <div className="users-list" data-testid="users-list">
          {users.map(u => (
            <div key={u.user_id || u.email} className="user-row" data-testid={`user-${u.user_id || u.email}`}>
              <div className="user-info">
                <div className="sidebar-user-avatar">{u.name?.[0]?.toUpperCase() || "?"}</div>
                <div><div className="user-name">{u.name || u.email}</div><div className="user-email">{u.email}</div></div>
              </div>
              <button className="catmgr-action-btn catmgr-danger" data-testid={`remove-user-${u.user_id}`} onClick={() => removeUser(u.user_id)}><Icon name="Trash" size={14}/></button>
            </div>
          ))}
        </div>
      </div>
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
      <div className="public-header"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/><path d="M8 7h6"/><path d="M8 11h4"/></svg><span>Agent Anatomy</span></div>
      <article className="doc-viewer" style={{maxWidth:800,margin:"0 auto",padding:"2rem"}}>
        <h1 className="doc-title" data-testid="public-doc-title">{doc.title}</h1>
        {doc.tags?.length > 0 && <div className="doc-tags">{doc.tags.map((t,i) => <span key={i} className="doc-tag"><Icon name="Tag" size={11}/>{t}</span>)}</div>}
        <div className="doc-content"><MarkdownContent content={doc.content} /></div>
      </article>
    </div>
  );
}

// --- Reading Progress (Finshots style - sticky right side) ---
function ReadingProgress() {
  const [progress, setProgress] = useState(0);
  useEffect(() => {
    const handler = () => {
      const main = document.querySelector('.main-content');
      if (!main) return;
      const scrollTop = main.scrollTop;
      const scrollHeight = main.scrollHeight - main.clientHeight;
      setProgress(scrollHeight > 0 ? Math.round((scrollTop / scrollHeight) * 100) : 0);
    };
    // Use interval to re-attach if element isn't ready yet
    const attach = () => {
      const main = document.querySelector('.main-content');
      if (main) {
        main.addEventListener('scroll', handler);
        handler(); // initial calc
      }
    };
    attach();
    const retryTimer = setTimeout(attach, 500);
    return () => {
      clearTimeout(retryTimer);
      const main = document.querySelector('.main-content');
      main?.removeEventListener('scroll', handler);
    };
  }, []);
  if (progress < 2) return null;
  const r = 20;
  const circ = 2 * Math.PI * r;
  const offset = circ - (progress / 100) * circ;
  return (
    <div className="progress-indicator" data-testid="reading-progress">
      <svg width="52" height="52" viewBox="0 0 52 52">
        <circle cx="26" cy="26" r={r} fill="none" stroke="var(--border-clr)" strokeWidth="3" />
        <circle cx="26" cy="26" r={r} fill="none" stroke="var(--accent)" strokeWidth="3" strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round" transform="rotate(-90 26 26)" style={{transition:"stroke-dashoffset 0.2s"}} />
      </svg>
      <span className="progress-pct">{progress}%</span>
    </div>
  );
}


// --- Learning Paths Page ---
function LearningPathsPage() {
  const { api } = useAuth();
  const navigate = useNavigate();
  const [paths, setPaths] = useState([]);
  const [activePath, setActivePath] = useState(null);
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(() => {
    try { return JSON.parse(localStorage.getItem("aa-learning-progress") || "{}"); } catch { return {}; }
  });

  useEffect(() => { api("get", "/learning-paths").then(r => setPaths(r.data)).catch(() => {}).finally(() => setLoading(false)); }, [api]);

  const markComplete = (pathId, docId) => {
    const key = `${pathId}:${docId}`;
    const updated = { ...progress, [key]: true };
    setProgress(updated);
    localStorage.setItem("aa-learning-progress", JSON.stringify(updated));
  };

  const getPathProgress = (path) => {
    if (!path?.steps) return 0;
    const completed = path.steps.filter(s => progress[`${path.id}:${s.document_id}`]).length;
    return Math.round((completed / path.steps.length) * 100);
  };

  if (loading) return <div className="edh-loading"><div className="edh-spinner"/></div>;

  if (activePath) {
    const pct = getPathProgress(activePath);
    const completedCount = activePath.steps.filter(s => progress[`${activePath.id}:${s.document_id}`]).length;
    return (
      <div className="lp-detail" data-testid="learning-path-detail">
        <button className="lp-back" data-testid="lp-back" onClick={() => setActivePath(null)}><Icon name="ArrowLeft" size={16}/> All Paths</button>
        <h1>{activePath.title}</h1>
        <p className="lp-desc">{activePath.description}</p>
        <div className="lp-stats">
          <span className={`lp-badge lp-badge-${activePath.difficulty}`}>{activePath.difficulty}</span>
          <span><Icon name="Clock" size={13}/> {activePath.estimated_time}</span>
          <span>{completedCount}/{activePath.steps.length} completed</span>
        </div>
        <div className="lp-progress-bar"><div className="lp-progress-fill" style={{width: `${pct}%`}} /><span>{pct}%</span></div>

        {/* Animated Roadmap */}
        <div className="lp-roadmap" data-testid="lp-roadmap">
          {activePath.steps.map((step, i) => {
            const done = progress[`${activePath.id}:${step.document_id}`];
            const isLast = i === activePath.steps.length - 1;
            return (
              <div key={i} className={`lp-road-node ${done ? "completed" : ""}`} data-testid={`lp-road-${i}`}>
                <div className="lp-road-dot">{done ? <Icon name="Check" size={12}/> : <span>{i + 1}</span>}</div>
                {!isLast && <div className={`lp-road-line ${done ? "completed" : ""}`} />}
                <span className="lp-road-label">{step.title}</span>
              </div>
            );
          })}
        </div>

        {/* Step Cards */}
        <div className="lp-steps">
          {activePath.steps.map((step, i) => {
            const done = progress[`${activePath.id}:${step.document_id}`];
            const isLast = i === activePath.steps.length - 1;
            const nextStep = !isLast ? activePath.steps[i + 1] : null;
            return (
              <div key={i} className={`lp-step ${done ? "completed" : ""}`} data-testid={`lp-step-${i}`}>
                <div className="lp-step-number">{done ? <Icon name="Check" size={16}/> : i + 1}</div>
                <div className="lp-step-content">
                  <h3>{step.title}</h3>
                  <p>{step.description}</p>
                  <div className="lp-step-actions">
                    <button className="editor-btn-primary" onClick={() => { markComplete(activePath.id, step.document_id); navigate(`/doc/${step.document_id}`); }}>
                      {done ? "Review" : "Start Reading"}
                    </button>
                    {!done && <button className="editor-btn-secondary" onClick={() => markComplete(activePath.id, step.document_id)}>Mark Complete</button>}
                  </div>
                  {done && nextStep && !progress[`${activePath.id}:${nextStep.document_id}`] && (
                    <button className="lp-next-btn" data-testid={`lp-next-${i}`} onClick={() => { document.querySelector(`[data-testid="lp-step-${i+1}"]`)?.scrollIntoView({behavior:"smooth"}); }}>
                      Next: {nextStep.title} <Icon name="ChevronRight" size={14}/>
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
        {pct === 100 && (
          <div className="lp-complete-banner" data-testid="lp-complete">
            <Icon name="Check" size={24}/> <span>Path Complete! You've finished all {activePath.steps.length} lessons.</span>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="lp-page" data-testid="learning-paths-page">
      <div className="lp-hero">
        <h1>Learning Paths</h1>
        <p>Guided sequences to master AI agent concepts — from beginner to advanced.</p>
      </div>
      <div className="lp-grid">
        {paths.map(path => {
          const pct = getPathProgress(path);
          const completedCount = path.steps?.filter(s => progress[`${path.id}:${s.document_id}`]).length || 0;
          return (
            <button key={path.id} className="lp-card" data-testid={`lp-card-${path.id}`} onClick={() => setActivePath(path)}>
              <div className="lp-card-icon"><Icon name={path.icon} size={28}/></div>
              <h2>{path.title}</h2>
              <p className="lp-card-desc">{path.description}</p>
              <div className="lp-card-meta">
                <span className={`lp-badge lp-badge-${path.difficulty}`}>{path.difficulty}</span>
                <span><Icon name="Clock" size={13}/> {path.estimated_time}</span>
                <span>{path.steps?.length} lessons</span>
              </div>
              <div className="lp-card-progress"><div className="lp-card-progress-fill" style={{width: `${pct}%`}} /></div>
              <div className="lp-card-pct">{completedCount}/{path.steps?.length || 0} completed ({pct}%)</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

// --- AI Chatbot ---
function AIChatbot({ docId }) {
  const { api, user } = useAuth();
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const sessionId = useRef(`chat_${user?.user_id}_${Date.now()}`);
  const endRef = useRef(null);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const send = async () => {
    if (!input.trim() || loading) return;
    const msg = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", text: msg }]);
    setLoading(true);
    try {
      const r = await api("post", "/chat", { message: msg, session_id: sessionId.current, doc_id: docId || null });
      setMessages(prev => [...prev, { role: "ai", text: r.data.response }]);
    } catch (e) {
      console.error("Chatbot error:", e);
      setMessages(prev => [...prev, { role: "ai", text: "Sorry, I encountered an error. Please try again." }]);
    }
    setLoading(false);
  };

  return (
    <>
      <button className="chatbot-fab" data-testid="chatbot-fab" onClick={() => setOpen(!open)} title="Ask AI">
        <Icon name="MessageSquare" size={22}/>
      </button>
      {open && (
        <div className="chatbot-panel" data-testid="chatbot-panel">
          <div className="chatbot-header">
            <span>Ask AI about docs</span>
            <button onClick={() => setOpen(false)} data-testid="chatbot-close"><Icon name="X" size={16}/></button>
          </div>
          <div className="chatbot-messages" data-testid="chatbot-messages">
            {messages.length === 0 && <div className="chatbot-welcome">Ask me anything about the documentation!</div>}
            {messages.map((m, i) => (
              <div key={i} className={`chatbot-msg ${m.role}`} data-testid={`chatbot-msg-${i}`}>
                <div className="chatbot-msg-bubble">{m.text}</div>
              </div>
            ))}
            {loading && <div className="chatbot-msg ai"><div className="chatbot-msg-bubble chatbot-typing">Thinking...</div></div>}
            <div ref={endRef} />
          </div>
          <div className="chatbot-input">
            <input data-testid="chatbot-input" placeholder="Ask a question..." value={input} onChange={e => setInput(e.target.value)} onKeyDown={e => { if (e.key === "Enter") send(); }} />
            <button data-testid="chatbot-send" onClick={send} disabled={!input.trim() || loading}><Icon name="ChevronRight" size={18}/></button>
          </div>
        </div>
      )}
    </>
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
  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => window.innerWidth < 768);
  const [sidebarWidth, setSidebarWidth] = useState(272);
  const [loading, setLoading] = useState(true);
  const [catManagerOpen, setCatManagerOpen] = useState(false);
  const isAdmin = user?.role === "admin";

  const [connectionError, setConnectionError] = useState(false);
  const retryTimeout = useRef(null);

  const loadData = useCallback(async (isRetry = false) => {
    if (!isRetry) setLoading(true);
    setConnectionError(false);
    try {
      const [catRes, docRes, bmRes] = await Promise.all([api("get", "/categories"), api("get", "/documents"), api("get", "/bookmarks")]);
      setCategories(catRes.data); setDocuments(docRes.data); setBookmarkedIds(bmRes.data.bookmarks.map(b => b.document_id));
      setLoading(false);
    } catch (e) {
      console.error(e);
      setConnectionError(true);
      setLoading(false);
      retryTimeout.current = setTimeout(() => loadData(true), 5000);
    }
  }, [api]);

  useEffect(() => {
    loadData();
    return () => { if (retryTimeout.current) clearTimeout(retryTimeout.current); };
  }, [loadData]);

  useEffect(() => {
    if (docId && documents.length > 0) {
      const doc = documents.find(d => d.id === docId);
      if (doc) { setActiveDoc(doc); setEditing(false); setCreating(false); }
    }
  }, [docId, documents]);

  const selectDoc = (id) => navigate(`/doc/${id}`);
  const toggleBookmark = async (dId) => { try { const r = await api("post", `/bookmarks/${dId}`); setBookmarkedIds(prev => r.data.bookmarked ? [...prev, dId] : prev.filter(x => x !== dId)); } catch {} };
  const refreshDocuments = async () => { try { const r = await api("get", "/documents"); setDocuments(r.data); } catch {} };

  const handleSaveDoc = async (data) => {
    try {
      if (creating) { const r = await api("post", "/documents", data); setDocuments(prev => [...prev, r.data]); setCreating(false); navigate(`/doc/${r.data.id}`); }
      else if (editing && activeDoc) { const r = await api("put", `/documents/${activeDoc.id}`, data); setDocuments(prev => prev.map(d => d.id === activeDoc.id ? r.data : d)); setActiveDoc(r.data); setEditing(false); }
    } catch {}
  };

  const handleDelete = async () => {
    if (!activeDoc) return;
    const confirmed = window.confirm("Move this document to trash?");
    if (!confirmed) return;
    try {
      await api("delete", `/documents/${activeDoc.id}`);
      setDocuments(prev => prev.filter(d => d.id !== activeDoc.id));
      setActiveDoc(null);
      navigate("/");
    } catch (e) {
      console.error("Delete failed:", e);
      alert(e.response?.data?.detail || "Failed to delete");
    }
  };

  const startNew = () => { setCreating(true); setEditing(false); setActiveDoc(null); };

  if (loading || connectionError) return (
    <div className="edh-loading" data-testid="loading-screen">
      <div className="edh-loading-content">
        <div className="edh-spinner"/>
        <h2 className="edh-loading-title">{connectionError ? "Connecting to server..." : "Loading Agent Anatomy..."}</h2>
        {connectionError && <p className="edh-loading-subtitle">The server is waking up. Retrying automatically...</p>}
        {connectionError && <button className="edh-loading-retry" data-testid="retry-btn" onClick={() => { if (retryTimeout.current) clearTimeout(retryTimeout.current); loadData(true); }}>Retry Now</button>}
      </div>
    </div>
  );

  const currentCat = activeDoc ? categories.find(c => c.id === activeDoc.category_id) : null;
  const parentCat = currentCat?.parent_id ? categories.find(c => c.id === currentCat.parent_id) : null;
  const bookmarkedDocs = documents.filter(d => bookmarkedIds.includes(d.id));
  const activeBookmarkCount = bookmarkedDocs.length;
  const isBookmarksRoute = window.location.pathname === "/bookmarks";
  const isLearnRoute = window.location.pathname === "/learn";
  const isToolsRoute = window.location.pathname === "/tools";
  const isTrashRoute = window.location.pathname === "/trash";
  const isSettingsRoute = window.location.pathname === "/settings";
  const isAnalyticsRoute = window.location.pathname === "/analytics";
  const showHome = !docId && !creating && !editing && !isBookmarksRoute && !isLearnRoute && !isToolsRoute && !isTrashRoute && !isSettingsRoute && !isAnalyticsRoute;

  return (
    <div className="dashboard" data-testid="dashboard">
      {false && <ReadingProgress />}
      <Sidebar categories={categories} documents={documents} activeDocId={activeDoc?.id} onSelectDoc={selectDoc} onNewDoc={startNew} collapsed={sidebarCollapsed} setCollapsed={setSidebarCollapsed} bookmarkCount={activeBookmarkCount} onManageCategories={() => setCatManagerOpen(true)} isAdmin={isAdmin} sidebarWidth={sidebarWidth} onResizeSidebar={setSidebarWidth} />
      <main className="main-content" data-testid="main-content" style={{marginLeft: sidebarCollapsed ? 48 : sidebarWidth}}>
        {creating || editing ? <DocumentEditor doc={editing ? activeDoc : null} categories={categories} onSave={handleSaveDoc} onCancel={() => { const wasCreating = creating; setCreating(false); setEditing(false); if (!wasCreating && activeDoc) navigate(`/doc/${activeDoc.id}`); }} />
        : isBookmarksRoute ? <BookmarksPage bookmarkedDocs={bookmarkedDocs} categories={categories} onSelectDoc={selectDoc} onToggleBookmark={toggleBookmark} />
        : isLearnRoute ? <LearningPathsPage />
        : isToolsRoute ? <ToolsPage isAdmin={isAdmin} />
        : isTrashRoute && isAdmin ? <TrashPage onDocumentsChanged={refreshDocuments} />
        : isSettingsRoute && isAdmin ? <SettingsPage isAdmin={isAdmin} />
        : isAnalyticsRoute && isAdmin ? <AnalyticsPage />
        : showHome ? <HomePage categories={categories} documents={documents} onSelectDoc={selectDoc} />
        : <DocumentViewer doc={activeDoc} category={currentCat} parentCategory={parentCat} isBookmarked={bookmarkedIds.includes(activeDoc?.id)} onToggleBookmark={() => activeDoc && toggleBookmark(activeDoc.id)} onEdit={() => setEditing(true)} onDelete={handleDelete} isAdmin={isAdmin} onNavigateHome={() => navigate("/")} categories={categories} documents={documents} onSelectDoc={selectDoc} />}
      </main>
      <CategoryManager open={catManagerOpen} onClose={() => setCatManagerOpen(false)} categories={categories} onCategoriesChange={setCategories} isAdmin={isAdmin} />
      <AIChatbot docId={activeDoc?.id} />
    </div>
  );
}

function AppRouter() {
  return (
    <Routes>
      <Route path="/share/:shareId" element={<PublicDocPage />} />
      <Route path="/bookmarks" element={<Dashboard />} />
      <Route path="/learn" element={<Dashboard />} />
      <Route path="/tools" element={<Dashboard />} />
      <Route path="/trash" element={<Dashboard />} />
      <Route path="/settings" element={<Dashboard />} />
      <Route path="/analytics" element={<Dashboard />} />
      <Route path="/doc/:docId" element={<Dashboard />} />
      <Route path="/" element={<Dashboard />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}

function NotFoundPage() {
  const navigate = useNavigate();
  return (
    <div className="edh-loading" data-testid="not-found-page">
      <div className="edh-loading-content">
        <h2 className="edh-loading-title">Page not found</h2>
        <p className="edh-loading-subtitle">The page you're looking for doesn't exist.</p>
        <button className="edh-loading-retry" onClick={() => navigate("/")}>Go Home</button>
      </div>
    </div>
  );
}

function KeywordProvider({ children }) {
  const [keywords, setKeywords] = useState({});
  useEffect(() => {
    axios.get(`${API}/keywords`).then(r => setKeywords(r.data)).catch(() => {});
  }, []);
  return <KeywordContext.Provider value={keywords}>{children}</KeywordContext.Provider>;
}

class ErrorBoundary extends React.Component {
  constructor(props) { super(props); this.state = { hasError: false }; }
  static getDerivedStateFromError() { return { hasError: true }; }
  render() {
    if (this.state.hasError) return (
      <div className="edh-loading"><div className="edh-loading-content">
        <h2 className="edh-loading-title">Something went wrong</h2>
        <p className="edh-loading-subtitle">An unexpected error occurred.</p>
        <button className="edh-loading-retry" onClick={() => { this.setState({ hasError: false }); window.location.href = "/"; }}>Reload</button>
      </div></div>
    );
    return this.props.children;
  }
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <AuthProvider>
          <KeywordProvider>
            <BrowserRouter>
              <AppRouter />
            </BrowserRouter>
          </KeywordProvider>
        </AuthProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
