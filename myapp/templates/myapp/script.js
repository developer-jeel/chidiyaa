/* =============================================
   CHIDIYAA — script.js
   All JavaScript interactions
   ============================================= */

'use strict';

/* ─────────────────────────────────────────────
   THEME (Dark Mode)
───────────────────────────────────────────── */
function getTheme() {
  return localStorage.getItem('chidiyaa-theme') ||
    (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
}
function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('chidiyaa-theme', theme);
}
function toggleTheme() {
  applyTheme(getTheme() === 'dark' ? 'light' : 'dark');
}
// init immediately (avoid FOUC)
applyTheme(getTheme());

/* ─────────────────────────────────────────────
   TOAST
───────────────────────────────────────────── */
function toast(msg, duration = 2800) {
  document.querySelectorAll('.toast').forEach(t => t.remove());
  const el = document.createElement('div');
  el.className = 'toast';
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), duration + 300);
}

/* ─────────────────────────────────────────────
   MODAL HELPERS
───────────────────────────────────────────── */
function openModal(id) {
  const el = document.getElementById(id);
  if (el) { el.classList.add('open'); document.body.style.overflow = 'hidden'; }
}
function closeModal(id) {
  const el = document.getElementById(id);
  if (el) { el.classList.remove('open'); document.body.style.overflow = ''; clearTimeout(window._storyTimer); }
}
function initModalClosers() {
  document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', e => {
      if (e.target === backdrop) closeModal(backdrop.id);
    });
  });
  document.querySelectorAll('[data-close-modal]').forEach(btn => {
    btn.addEventListener('click', () => closeModal(btn.dataset.closeModal));
  });
  document.querySelectorAll('[data-open-modal]').forEach(btn => {
    btn.addEventListener('click', () => openModal(btn.dataset.openModal));
  });
}

/* ─────────────────────────────────────────────
   LIKE BUTTON
───────────────────────────────────────────── */
function initLikes() {
  document.querySelectorAll('.action-btn.like-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const liked = this.classList.toggle('liked');
      this.textContent = liked ? '❤️' : '🤍';
      const countEl = this.closest('.post-card, .post-view-right')?.querySelector('.likes-count');
      if (countEl) {
        let n = parseInt(countEl.textContent.replace(/,/g, ''), 10);
        countEl.textContent = (liked ? n + 1 : n - 1).toLocaleString();
      }
    });
  });
}

/* Double-tap to like */
function initDoubleTapLike() {
  document.querySelectorAll('.post-image-wrap').forEach(wrap => {
    let last = 0;
    wrap.addEventListener('click', function (e) {
      const now = Date.now();
      if (now - last < 320) {
        const btn = this.closest('.post-card')?.querySelector('.like-btn');
        if (btn && !btn.classList.contains('liked')) {
          btn.click();
          floatHeart(e.clientX, e.clientY);
        }
      }
      last = now;
    });
  });
}
function floatHeart(x, y) {
  const h = document.createElement('div');
  h.textContent = '❤️';
  h.style.cssText = `position:fixed;left:${x}px;top:${y}px;font-size:58px;pointer-events:none;z-index:9999;
    transform:translate(-50%,-50%) scale(0);animation:heartFloat .8s ease forwards;`;
  if (!document.getElementById('heart-kf')) {
    const s = document.createElement('style');
    s.id = 'heart-kf';
    s.textContent = `@keyframes heartFloat{0%{transform:translate(-50%,-50%) scale(0);opacity:1}
      50%{transform:translate(-50%,-70%) scale(1.2);opacity:1}100%{transform:translate(-50%,-95%) scale(.9);opacity:0}}`;
    document.head.appendChild(s);
  }
  document.body.appendChild(h);
  setTimeout(() => h.remove(), 820);
}

/* ─────────────────────────────────────────────
   SAVE BUTTON
───────────────────────────────────────────── */
function initSaveButtons() {
  document.querySelectorAll('.save-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const saved = this.classList.toggle('saved');
      this.textContent = saved ? '🔖' : '🏷️';
    });
  });
}

/* ─────────────────────────────────────────────
   FOLLOW BUTTONS
───────────────────────────────────────────── */
function initFollowButtons() {
  document.querySelectorAll('.follow-btn, .notif-follow-btn, .reel-follow-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      const isFollowing = this.classList.toggle('following');
      if (this.classList.contains('notif-follow-btn')) {
        this.textContent = isFollowing ? 'Following' : 'Follow Back';
      } else if (this.classList.contains('reel-follow-btn')) {
        this.textContent = isFollowing ? 'Following' : 'Follow';
      } else {
        this.textContent = isFollowing ? 'Following' : 'Follow';
      }
    });
  });
}

/* ─────────────────────────────────────────────
   STORIES
───────────────────────────────────────────── */
const STORIES = [
  { user: 'aarav_k',  avatar: 'https://i.pravatar.cc/150?img=1',  emoji: '🌅', time: '2h ago' },
  { user: 'priya.s',  avatar: 'https://i.pravatar.cc/150?img=5',  emoji: '🌸', time: '3h ago' },
  { user: 'rohit_m',  avatar: 'https://i.pravatar.cc/150?img=8',  emoji: '🏔️', time: '5h ago' },
  { user: 'sneha.d',  avatar: 'https://i.pravatar.cc/150?img=9',  emoji: '🌊', time: '6h ago' },
  { user: 'dev.p',    avatar: 'https://i.pravatar.cc/150?img=12', emoji: '🎨', time: '8h ago' },
  { user: 'kavya.r',  avatar: 'https://i.pravatar.cc/150?img=15', emoji: '🦋', time: '10h ago' },
];
let _storyIdx = 0;

function openStory(idx) {
  _storyIdx = Math.max(0, Math.min(idx, STORIES.length - 1));
  const s = STORIES[_storyIdx];
  const modal = document.getElementById('story-modal');
  if (!modal) return;
  modal.querySelector('.story-modal-uname').textContent = s.user;
  modal.querySelector('.story-modal-time').textContent = s.time;
  modal.querySelector('.story-modal-ava img').src = s.avatar;
  modal.querySelector('.story-modal-placeholder').textContent = s.emoji;
  // reset + run progress bars
  modal.querySelectorAll('.story-prog-fill').forEach((b, i) => {
    b.style.animation = 'none'; b.classList.remove('done','active');
    b.offsetHeight; // reflow
    if (i < _storyIdx) b.classList.add('done');
    if (i === _storyIdx) b.classList.add('active');
  });
  openModal('story-modal');
  clearTimeout(window._storyTimer);
  window._storyTimer = setTimeout(() => {
    if (_storyIdx < STORIES.length - 1) openStory(_storyIdx + 1);
    else closeModal('story-modal');
  }, 5000);
}
function initStories() {
  document.querySelectorAll('.story-item[data-story-idx]').forEach(item => {
    item.addEventListener('click', () => openStory(parseInt(item.dataset.storyIdx, 10)));
  });
  document.querySelector('.story-nav-prev')?.addEventListener('click', () => {
    if (_storyIdx > 0) openStory(_storyIdx - 1);
  });
  document.querySelector('.story-nav-next')?.addEventListener('click', () => {
    if (_storyIdx < STORIES.length - 1) openStory(_storyIdx + 1);
    else closeModal('story-modal');
  });
}

/* ─────────────────────────────────────────────
   CREATE POST — file upload preview
───────────────────────────────────────────── */
function initCreatePost() {
  const fileInput = document.getElementById('post-file-input');
  const uploadZone = document.querySelector('.create-upload-zone');
  if (!fileInput || !uploadZone) return;

  const triggerPick = () => fileInput.click();
  uploadZone.addEventListener('click', triggerPick);

  fileInput.addEventListener('change', function () {
    const f = this.files[0];
    if (!f) return;
    const reader = new FileReader();
    reader.onload = e => {
      let img = uploadZone.querySelector('img');
      if (!img) { img = document.createElement('img'); uploadZone.appendChild(img); }
      img.src = e.target.result;
      uploadZone.classList.add('has-preview');
      uploadZone.querySelectorAll('.create-upload-icon,.create-upload-title,.create-upload-sub,.create-upload-cta').forEach(el => el.style.display = 'none');
    };
    reader.readAsDataURL(f);
  });

  // Drag-and-drop
  uploadZone.addEventListener('dragover', e => { e.preventDefault(); uploadZone.style.background = 'var(--accent-light)'; });
  uploadZone.addEventListener('dragleave', () => { uploadZone.style.background = ''; });
  uploadZone.addEventListener('drop', e => {
    e.preventDefault(); uploadZone.style.background = '';
    const f = e.dataTransfer.files[0];
    if (f?.type.startsWith('image/')) {
      const dt = new DataTransfer(); dt.items.add(f);
      fileInput.files = dt.files;
      fileInput.dispatchEvent(new Event('change'));
    }
  });

  // Share / submit
  document.querySelector('.create-share-btn')?.addEventListener('click', () => {
    const caption = document.querySelector('.create-caption')?.value?.trim();
    if (!uploadZone.classList.contains('has-preview')) {
      toast('📷 Please select a photo first'); return;
    }
    toast('🐦 Post shared successfully!');
    setTimeout(() => window.location.href = 'index.html', 1200);
  });

  // Caption char count
  const captionEl = document.querySelector('.create-caption');
  const charCount = document.querySelector('.create-char-count');
  if (captionEl && charCount) {
    captionEl.addEventListener('input', () => {
      charCount.textContent = `${captionEl.value.length} / 2,200`;
    });
  }
}

/* ─────────────────────────────────────────────
   AVATAR UPLOAD (signup)
───────────────────────────────────────────── */
function initAvatarUpload() {
  const input = document.getElementById('avatar-input');
  const zone = document.querySelector('.avatar-upload');
  if (!input || !zone) return;
  zone.addEventListener('click', () => input.click());
  input.addEventListener('change', function () {
    const f = this.files[0]; if (!f) return;
    const reader = new FileReader();
    reader.onload = e => {
      const circle = zone.querySelector('.avatar-preview-circle');
      let img = circle.querySelector('img');
      if (!img) { img = document.createElement('img'); circle.appendChild(img); }
      img.src = e.target.result;
      img.style.display = 'block';
      circle.querySelector('span')?.remove();
    };
    reader.readAsDataURL(f);
  });
}

/* ─────────────────────────────────────────────
   MESSAGES
───────────────────────────────────────────── */
function initMessages() {
  // Select conversation
  document.querySelectorAll('.msg-item').forEach(item => {
    item.addEventListener('click', function () {
      document.querySelectorAll('.msg-item').forEach(i => i.classList.remove('active'));
      this.classList.add('active');
      const name = this.querySelector('.msg-item-name')?.textContent;
      const img = this.querySelector('.msg-item-avatar img')?.src;
      const empty = document.getElementById('chat-empty');
      const convo = document.getElementById('chat-convo');
      if (empty) empty.style.display = 'none';
      if (convo) {
        convo.style.display = 'flex';
        convo.querySelector('.chat-topbar-name').textContent = name || '';
        const ava = convo.querySelector('.chat-topbar-avatar img');
        if (ava) ava.src = img || '';
      }
      // Mobile: show chat panel
      if (window.innerWidth <= 768) {
        document.querySelector('.msg-list-panel')?.classList.remove('visible');
        document.querySelector('.chat-panel')?.classList.add('visible');
      }
    });
  });

  // Send message
  const sendBtn = document.querySelector('.chat-send-btn');
  const inputBox = document.querySelector('.chat-text-input');
  const msgArea = document.querySelector('.chat-messages');
  if (sendBtn && inputBox && msgArea) {
    const doSend = () => {
      const txt = inputBox.value.trim();
      if (!txt) return;
      const wrap = document.createElement('div');
      wrap.className = 'chat-bubble-wrap sent';
      wrap.innerHTML = `<div class="chat-bubble">${escHtml(txt)}</div>`;
      msgArea.appendChild(wrap);
      inputBox.value = '';
      msgArea.scrollTop = msgArea.scrollHeight;
      // Simulate reply
      setTimeout(() => {
        const replies = ['Haha that\'s so fun! 😄', 'Absolutely! 🔥', 'Let\'s catch up soon 🐦', 'Wow, nice one!'];
        const reply = document.createElement('div');
        reply.className = 'chat-bubble-wrap received';
        reply.innerHTML = `
          <div class="bubble-avatar"><img src="https://i.pravatar.cc/150?img=5" alt=""/></div>
          <div class="chat-bubble">${replies[Math.floor(Math.random() * replies.length)]}</div>`;
        msgArea.appendChild(reply);
        msgArea.scrollTop = msgArea.scrollHeight;
      }, 1400);
    };
    sendBtn.addEventListener('click', doSend);
    inputBox.addEventListener('keydown', e => { if (e.key === 'Enter') doSend(); });
  }

  // Mobile back button
  document.querySelector('.chat-back-btn')?.addEventListener('click', () => {
    document.querySelector('.chat-panel')?.classList.remove('visible');
    document.querySelector('.msg-list-panel')?.classList.add('visible');
  });
}

/* ─────────────────────────────────────────────
   COMMENTS
───────────────────────────────────────────── */
function initComments() {
  document.querySelectorAll('.post-add-comment').forEach(row => {
    const input = row.querySelector('.comment-input-field');
    const btn = row.querySelector('.comment-post-btn');
    if (!input || !btn) return;
    btn.addEventListener('click', () => {
      if (input.value.trim()) { input.value = ''; toast('💬 Comment posted!'); }
    });
    input.addEventListener('keydown', e => { if (e.key === 'Enter') btn.click(); });
  });
}

/* ─────────────────────────────────────────────
   NOTIFICATIONS — mark read
───────────────────────────────────────────── */
function initNotifications() {
  document.querySelectorAll('.notif-item').forEach(item => {
    item.addEventListener('click', function () { this.classList.remove('unseen'); });
  });
}

/* ─────────────────────────────────────────────
   PROFILE TABS
───────────────────────────────────────────── */
function initProfileTabs() {
  const tabs = document.querySelectorAll('.profile-tab');
  const grids = document.querySelectorAll('.profile-tab-content');
  tabs.forEach(tab => {
    tab.addEventListener('click', function () {
      tabs.forEach(t => t.classList.remove('active'));
      grids.forEach(g => g.style.display = 'none');
      this.classList.add('active');
      const target = document.getElementById('tab-' + this.dataset.tab);
      if (target) target.style.display = 'grid';
    });
  });
}

/* ─────────────────────────────────────────────
   GRID POST CLICK (open modal)
───────────────────────────────────────────── */
function initGridClicks() {
  document.querySelectorAll('.grid-post, .search-grid-item').forEach(item => {
    item.addEventListener('click', function () {
      const img = this.querySelector('img')?.src;
      const modal = document.getElementById('post-view-modal');
      if (!modal || !img) return;
      const pvImg = modal.querySelector('.post-view-img img');
      if (pvImg) pvImg.src = img;
      openModal('post-view-modal');
    });
  });
}

/* ─────────────────────────────────────────────
   REELS PLAY TOGGLE
───────────────────────────────────────────── */
function initReels() {
  document.querySelectorAll('.reel-play-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      this.textContent = this.textContent === '▶️' ? '⏸️' : '▶️';
    });
  });
  document.querySelectorAll('.reel-action').forEach(action => {
    action.addEventListener('click', function () {
      const icon = this.querySelector('.reel-action-icon');
      if (icon?.textContent === '🤍') { icon.textContent = '❤️'; icon.style.animation = 'heartBeat .35s ease'; }
      else if (icon?.textContent === '❤️') { icon.textContent = '🤍'; icon.style.animation = ''; }
    });
  });
}

/* ─────────────────────────────────────────────
   SEARCH — chip filter
───────────────────────────────────────────── */
function initSearch() {
  document.querySelectorAll('.chip-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.chip-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
    });
  });
}

/* ─────────────────────────────────────────────
   AUTH FORMS (demo — redirect on submit)
───────────────────────────────────────────── */
function initAuthForms() {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', e => { e.preventDefault(); window.location.href = 'index.html'; });
  }
  const signupForm = document.getElementById('signup-form');
  if (signupForm) {
    signupForm.addEventListener('submit', e => {
      e.preventDefault();
      const pw = document.getElementById('pw')?.value;
      const cpw = document.getElementById('cpw')?.value;
      if (pw && cpw && pw !== cpw) { toast('⚠️ Passwords do not match'); return; }
      window.location.href = 'index.html';
    });
  }
}

/* ─────────────────────────────────────────────
   KEYBOARD SHORTCUTS
───────────────────────────────────────────── */
function initKeyboard() {
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.modal-backdrop.open').forEach(m => closeModal(m.id));
    }
    // Left/right arrows in story viewer
    if (document.getElementById('story-modal')?.classList.contains('open')) {
      if (e.key === 'ArrowRight') {
        if (_storyIdx < STORIES.length - 1) openStory(_storyIdx + 1);
        else closeModal('story-modal');
      }
      if (e.key === 'ArrowLeft' && _storyIdx > 0) openStory(_storyIdx - 1);
    }
  });
}

/* ─────────────────────────────────────────────
   MOBILE MENU TOGGLE
───────────────────────────────────────────── */
function initMobileMenu() {
  const toggle = document.getElementById('mobile-menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  if (toggle && sidebar) {
    toggle.addEventListener('click', () => {
      sidebar.style.display = sidebar.style.display === 'flex' ? 'none' : 'flex';
    });
  }
}

/* ─────────────────────────────────────────────
   STORIES HORIZONTAL SCROLL (mouse wheel)
───────────────────────────────────────────── */
function initStoriesScroll() {
  const scroll = document.querySelector('.stories-scroll');
  if (!scroll) return;
  scroll.addEventListener('wheel', e => { e.preventDefault(); scroll.scrollLeft += e.deltaY; }, { passive: false });
}

/* ─────────────────────────────────────────────
   MESSAGES PANEL — MOBILE initial state
───────────────────────────────────────────── */
function initMessagesMobile() {
  if (window.innerWidth <= 768) {
    document.querySelector('.msg-list-panel')?.classList.add('visible');
  }
}

/* ─────────────────────────────────────────────
   SMOOTH PAGE SECTION TRANSITIONS (index)
───────────────────────────────────────────── */
function initPageSections() {
  // handled per-page via data-active attributes in index.html
}

/* ─────────────────────────────────────────────
   UTIL: escape HTML
───────────────────────────────────────────── */
function escHtml(t) {
  const d = document.createElement('div');
  d.appendChild(document.createTextNode(t));
  return d.innerHTML;
}

/* ─────────────────────────────────────────────
   SKELETON LOADERS (simulate loading)
───────────────────────────────────────────── */
function initSkeletons() {
  const skeletons = document.querySelectorAll('[data-skeleton]');
  if (!skeletons.length) return;
  setTimeout(() => {
    skeletons.forEach(s => s.removeAttribute('data-skeleton'));
  }, 1200);
}

/* ─────────────────────────────────────────────
   INIT ALL
───────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  // Theme toggles
  document.querySelectorAll('.dark-toggle-row, .theme-toggle-btn').forEach(el => {
    el.addEventListener('click', toggleTheme);
  });

  // All feature inits
  initModalClosers();
  initLikes();
  initDoubleTapLike();
  initSaveButtons();
  initFollowButtons();
  initStories();
  initCreatePost();
  initAvatarUpload();
  initMessages();
  initComments();
  initNotifications();
  initProfileTabs();
  initGridClicks();
  initReels();
  initSearch();
  initAuthForms();
  initKeyboard();
  initMobileMenu();
  initStoriesScroll();
  initMessagesMobile();
  initSkeletons();
});
