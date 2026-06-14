/* ═══════════════════════════════════════════════════════════
   VisePanda v3.0.1 — Frontend Application
   ═══════════════════════════════════════════════════════════ */

const VP = (function(){
  'use strict';

  // ── State ──
  const state = {
    currentView: 'home',
    messages: [],
    isStreaming: false,
    theme: document.documentElement.getAttribute('data-theme') || 'dark',
  };

  // ── DOM refs ──
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => document.querySelectorAll(s);

  // ── Navigation ──
  function navigate(view) {
    state.currentView = view;

    // Update nav buttons
    $$('.nav-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.view === view);
    });

    // Show/hide views
    $$('.view').forEach(v => v.classList.remove('active'));
    const target = document.getElementById(`view-${view}`);
    if (target) target.classList.add('active');

    // Load data on demand
    if (view === 'cities') loadCities();
    if (view === 'tools') loadTools();
    if (view === 'home') loadHomeCities();

    // Update URL hash
    window.location.hash = view;
  }

  // ── Theme ──
  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('vp_theme', next);
    state.theme = next;
    // Update toggle icon
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = next === 'dark' ? '🌙' : '☀️';
  }

  // ── API helpers ──
  async function apiGet(path) {
    try {
      const r = await fetch(path);
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return await r.json();
    } catch (e) {
      console.error(`API GET ${path}:`, e);
      return null;
    }
  }

  async function apiPost(path, data) {
    try {
      const r = await fetch(path, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data),
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r;
    } catch (e) {
      console.error(`API POST ${path}:`, e);
      return null;
    }
  }

  // ── Load Home Cities ──
  async function loadHomeCities() {
    const grid = document.getElementById('city-grid');
    if (!grid) return;
    const data = await apiGet('/api/cities');
    if (!data || !data.cities) return;

    grid.innerHTML = '';
    const entries = Object.entries(data.cities).slice(0, 8);
    entries.forEach(([name, info]) => {
      const card = document.createElement('div');
      card.className = 'city-card';
      card.onclick = () => navigate('chat');
      card.innerHTML = `
        <div style="font-size:28px;margin-bottom:8px">${getCityEmoji(name)}</div>
        <div style="font-size:16px;font-weight:600;margin-bottom:2px">${name}</div>
        <div style="font-size:12px;color:var(--text-muted)">${info.name_cn || ''}</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:4px">${info.best_season || ''} · ${info.days || ''}</div>
      `;
      grid.appendChild(card);
    });
  }

  // ── Load Cities (all) ──
  async function loadCities() {
    const grid = document.getElementById('cities-grid');
    if (!grid) return;
    const data = await apiGet('/api/cities');
    if (!data || !data.cities) return;

    grid.innerHTML = '';
    Object.entries(data.cities).forEach(([name, info]) => {
      const card = document.createElement('div');
      card.className = 'city-card';
      card.innerHTML = `
        <div style="font-size:32px;margin-bottom:8px">${getCityEmoji(name)}</div>
        <div style="font-size:16px;font-weight:600">${name}</div>
        <div style="font-size:12px;color:var(--text-muted)">${info.name_cn || ''}</div>
        <div style="font-size:12px;color:var(--text-secondary);margin-top:6px">
          ${info.highlights ? info.highlights.join(' · ') : ''}
        </div>
        <div style="font-size:11px;color:var(--text-dim);margin-top:4px">
          ${info.best_season || ''} · ${info.days || ''}
        </div>
      `;
      grid.appendChild(card);
    });
  }

  // ── Load Tools ──
  async function loadTools() {
    const grid = document.getElementById('tools-grid');
    if (!grid) return;
    const data = await apiGet('/api/tools');
    if (!data || !data.tools) return;

    grid.innerHTML = '';
    const emojis = {packing:'🧳', pricing:'💰', visa:'🛂', phrases:'💬', emergency:'🆘'};
    Object.entries(data.tools).forEach(([name, desc]) => {
      const card = document.createElement('div');
      card.className = 'tool-card';
      card.innerHTML = `
        <div style="font-size:24px;margin-bottom:8px">${emojis[name] || '🧰'}</div>
        <div style="font-size:14px;font-weight:600;margin-bottom:2px;text-transform:capitalize">${name}</div>
        <div style="font-size:12px;color:var(--text-muted)">${desc}</div>
      `;
      grid.appendChild(card);
    });
  }

  // ── City emoji helper ──
  function getCityEmoji(name) {
    const map = {
      beijing:'🏯', shanghai:'🌃', chengdu:'🐼', guangzhou:'🥟',
      shenzhen:'🌆', hangzhou:'🌊', xi_an:'🏛️', guilin:'🏞️',
      chongqing:'🌉', kunming:'🌸', suzhou:'🏯', nanjing:'🏛️',
      lhasa:'🏔️', hong_kong:'🌃', macau:'🎰',
    };
    return map[name.toLowerCase().replace(/ /g,'_')] || '🏙️';
  }

  // ── Chat ──
  let abortController = null;

  async function sendMessage() {
    const input = document.getElementById('chat-input');
    const text = input.value.trim();
    if (!text || state.isStreaming) return;

    input.value = '';
    input.style.height = 'auto';
    toggleSendButton(false);

    // Add user message
    addMessage(text, 'user');
    state.messages.push({role: 'user', content: text});

    // Show typing indicator
    const typingId = addTyping();

    // Stream response
    state.isStreaming = true;
    abortController = new AbortController();

    try {
      const resp = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          messages: state.messages.slice(-10), // last 10 for context
        }),
        signal: abortController.signal,
      });

      if (!resp.ok) {
        removeMessage(typingId);
        addMessage('Sorry, I couldn\'t process that. Please try again.', 'bot');
        return;
      }

      const reader = resp.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      let botContent = '';

      while (true) {
        const {done, value} = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, {stream: true});
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          const data = line.slice(6).trim();
          if (!data) continue;

          try {
            const parsed = JSON.parse(data);
            if (parsed.token) {
              botContent += parsed.token;
              updateTyping(typingId, botContent);
            } else if (parsed.error) {
              removeMessage(typingId);
              addMessage('Error: ' + parsed.error, 'bot');
              state.isStreaming = false;
              toggleSendButton(true);
              return;
            }
          } catch(e) {}
        }
      }

      // Finalize bot message
      if (botContent) {
        removeMessage(typingId);
        addMessage(botContent, 'bot');
        state.messages.push({role: 'assistant', content: botContent});
      } else {
        removeMessage(typingId);
        addMessage('I\'m not sure how to help with that. Could you tell me more about your travel plans?', 'bot');
      }

    } catch (e) {
      if (e.name !== 'AbortError') {
        removeMessage(typingId);
        addMessage('Connection error. Please check your network and try again.', 'bot');
      }
    } finally {
      state.isStreaming = false;
      abortController = null;
      toggleSendButton(true);
    }
  }

  function addMessage(text, role) {
    const container = document.getElementById('chat-messages');
    const msg = document.createElement('div');
    msg.className = `msg msg-${role}`;
    msg.innerHTML = `
      <div class="msg-avatar">${role === 'bot' ? '🐼' : 'Y'}</div>
      <div class="msg-body">
        <div class="msg-sender">${role === 'bot' ? 'VisePanda' : 'You'}</div>
        <div class="msg-text">${escapeHtml(text)}</div>
      </div>
    `;
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
    return msg;
  }

  function addTyping() {
    const container = document.getElementById('chat-messages');
    const msg = document.createElement('div');
    msg.className = 'msg msg-bot';
    msg.id = 'typing-msg';
    msg.innerHTML = `
      <div class="msg-avatar">🐼</div>
      <div class="msg-body">
        <div class="msg-sender">VisePanda</div>
        <div class="msg-text typing-content"></div>
      </div>
    `;
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
    return 'typing-msg';
  }

  function updateTyping(id, content) {
    const el = document.getElementById(id);
    if (!el) return;
    const textEl = el.querySelector('.typing-content');
    if (textEl) textEl.innerHTML = escapeHtml(content) + '<span class="cursor" style="animation:blink 1s infinite">▌</span>';
    const container = document.getElementById('chat-messages');
    container.scrollTop = container.scrollHeight;
  }

  function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  function toggleSendButton(enabled) {
    const btn = document.getElementById('chat-send');
    if (btn) {
      btn.disabled = !enabled;
      btn.textContent = enabled ? 'Send' : '...';
    }
  }

  // ── Chat input auto-resize ──
  function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 120) + 'px';
    // Enable/disable send button
    const btn = document.getElementById('chat-send');
    if (btn) btn.disabled = !el.value.trim() || state.isStreaming;
  }

  // ── Enter to send ──
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      const active = document.activeElement;
      if (active && active.id === 'chat-input') {
        e.preventDefault();
        sendMessage();
      }
    }
  });

  // ── HTML escaping ──
  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  // ── Init ──
  function init() {
    // Check URL hash
    const hash = window.location.hash.slice(1) || 'home';
    navigate(hash);

    // Init theme toggle icon
    const btn = document.querySelector('.theme-toggle');
    if (btn) btn.textContent = state.theme === 'dark' ? '🌙' : '☀️';

    // Home city data
    loadHomeCities();

    console.log('VisePanda v3.0.1 initialized');
  }

  // ── Public API ──
  return {
    init,
    navigate,
    toggleTheme,
    sendMessage,
    autoResize,
  };
})();

// ── Bootstrap ──
document.addEventListener('DOMContentLoaded', VP.init);
