/* =============================================
   LEARNING FUTURE WITH US — MAIN JS
   ============================================= */

/* ---- SHARED DATA ---- */
const COURSES = [
  {
    id: 'c1', cat: 'foundations', icon: '🧠',
    thumbClass: 'thumb-yellow', tagColor: '#f7c948', tag: 'AI Foundations',
    title: 'AI & ML Fundamentals',
    desc: 'Start your AI journey. Python, statistics, intro to ML — zero to job-ready in 8 weeks.',
    price: '₹4,999/mo', dur: '8 Weeks',
    videos: [
      { type: 'live',     title: 'Intro to Neural Networks',   sub: 'Live · Mon & Thu 7PM', badge: true },
      { type: 'recorded', title: 'Python for AI — Module 1',   sub: '45 min · HD' },
      { type: 'recorded', title: 'Statistics Bootcamp',         sub: '60 min · HD' },
    ]
  },
  {
    id: 'c2', cat: 'foundations', icon: '📊',
    thumbClass: 'thumb-yellow', tagColor: '#f7c948', tag: 'AI Foundations',
    title: 'Data Science Essentials',
    desc: 'Master pandas, matplotlib, EDA, and feature engineering with real datasets.',
    price: '₹4,999/mo', dur: '6 Weeks',
    videos: [
      { type: 'live',     title: 'Data Wrangling Masterclass',  sub: 'Live · Wed 6PM', badge: true },
      { type: 'recorded', title: 'EDA with Pandas',             sub: '55 min · HD' },
      { type: 'recorded', title: 'Feature Engineering Secrets', sub: '50 min · HD' },
    ]
  },
  {
    id: 'c3', cat: 'applied', icon: '⚙️',
    thumbClass: 'thumb-coral', tagColor: '#ff6f61', tag: 'Applied AI',
    title: 'Machine Learning Pro',
    desc: 'Supervised, unsupervised, and reinforcement learning with hands-on Kaggle projects.',
    price: '₹9,999/mo', dur: '12 Weeks',
    videos: [
      { type: 'live',     title: 'XGBoost & LightGBM Deep Dive', sub: 'Live · Tue & Fri 8PM', badge: true },
      { type: 'recorded', title: 'Random Forests Explained',      sub: '70 min · HD' },
      { type: 'recorded', title: 'Model Evaluation Metrics',      sub: '40 min · HD' },
    ]
  },
  {
    id: 'c4', cat: 'applied', icon: '🗣️',
    thumbClass: 'thumb-coral', tagColor: '#ff6f61', tag: 'Applied AI',
    title: 'NLP & Generative AI',
    desc: 'Build chatbots, text classifiers, and LLM-powered apps using OpenAI & HuggingFace.',
    price: '₹9,999/mo', dur: '10 Weeks',
    videos: [
      { type: 'live',     title: 'Building with Claude API',      sub: 'Live · Mon 7PM', badge: true },
      { type: 'recorded', title: 'Transformers Architecture',     sub: '80 min · HD' },
      { type: 'recorded', title: 'Prompt Engineering Mastery',    sub: '65 min · HD' },
    ]
  },
  {
    id: 'c5', cat: 'applied', icon: '👁️',
    thumbClass: 'thumb-coral', tagColor: '#ff6f61', tag: 'Applied AI',
    title: 'Computer Vision with AI',
    desc: 'Image classification, object detection, and real-time video analysis using PyTorch.',
    price: '₹9,999/mo', dur: '10 Weeks',
    videos: [
      { type: 'live',     title: 'YOLOv8 Implementation',       sub: 'Live · Thu 6PM', badge: true },
      { type: 'recorded', title: 'CNN Architecture Deep Dive',  sub: '75 min · HD' },
      { type: 'recorded', title: 'OpenCV Fundamentals',         sub: '50 min · HD' },
    ]
  },
  {
    id: 'c6', cat: 'advanced', icon: '🚀',
    thumbClass: 'thumb-teal', tagColor: '#00e5c3', tag: 'Advanced AI',
    title: 'Deep Learning Research',
    desc: 'GANs, Diffusion Models, Transformers from scratch. Research paper implementation.',
    price: '₹19,999/mo', dur: '16 Weeks',
    videos: [
      { type: 'live',     title: 'Diffusion Models from Scratch', sub: 'Live · Daily 9PM', badge: true },
      { type: 'recorded', title: 'Attention Mechanism Explained', sub: '90 min · 4K' },
      { type: 'recorded', title: 'GAN Training Techniques',       sub: '85 min · 4K' },
    ]
  },
  {
    id: 'c7', cat: 'advanced', icon: '🏢',
    thumbClass: 'thumb-teal', tagColor: '#00e5c3', tag: 'Advanced AI',
    title: 'AI for Business & Strategy',
    desc: 'AI ROI, ethics, governance, and deploying AI products in enterprise environments.',
    price: '₹19,999/mo', dur: '8 Weeks',
    videos: [
      { type: 'live',     title: 'AI Ethics & Governance',     sub: 'Live · Wed & Sat 7PM', badge: true },
      { type: 'recorded', title: 'AI Product Strategy',         sub: '60 min · HD' },
      { type: 'recorded', title: 'Case Studies: Fortune 500 AI',sub: '55 min · HD' },
    ]
  },
];

const BACKEND_DATA = [
  { id:'LF-2024-0001', name:'Rahul Sharma',   course:'ML Pro',          plan:'Professional', fee:'₹59,994',    date:'Jan 12, 2024', progress:'92%', status:'active' },
  { id:'LF-2024-0042', name:'Priya Singh',    course:'AI Foundations',  plan:'Starter',      fee:'₹14,997',    date:'Feb 3, 2024',  progress:'78%', status:'active' },
  { id:'LF-2024-0089', name:'Amit Kumar',     course:'Deep Learning',   plan:'Elite',        fee:'₹2,39,988',  date:'Mar 15, 2024', progress:'45%', status:'active' },
  { id:'LF-2024-0103', name:'Sneha Patel',    course:'NLP & GenAI',     plan:'Professional', fee:'₹29,997',    date:'Mar 28, 2024', progress:'61%', status:'pending' },
  { id:'LF-2024-0156', name:'Rajesh Verma',   course:'Computer Vision', plan:'Professional', fee:'₹9,999',     date:'Apr 1, 2024',  progress:'20%', status:'active' },
  { id:'LF-2024-0201', name:'Meera Joshi',    course:'AI for Business', plan:'Elite',        fee:'₹1,19,994',  date:'Apr 10, 2024', progress:'88%', status:'inactive' },
  { id:'LF-2024-0237', name:'Vikram Rao',     course:'Data Science',    plan:'Starter',      fee:'₹4,999',     date:'Apr 18, 2024', progress:'10%', status:'pending' },
  { id:'LF-2024-0289', name:'Anjali Mishra',  course:'ML Pro',          plan:'Professional', fee:'₹1,19,988',  date:'May 2, 2024',  progress:'55%', status:'active' },
];

const CHAT_RESPONSES = {
  'fee':         '💰 Our plans start from ₹4,999/month. Professional is ₹9,999/mo and Elite is ₹19,999/mo. EMI options are available on all plans!',
  'course':      '📚 We offer 3 categories: AI Foundations, Applied AI, and Advanced AI — with 7 specialized courses in total.',
  'certificate': '🎓 Certificates are issued after 80% course completion + passing the final assessment. Auto-downloadable from your profile.',
  'refund':      '↩ We have a 7-day money-back guarantee. Contact us within 7 days of enrollment for a full refund — no questions asked.',
  'emi':         '📅 0% EMI available on HDFC, ICICI, SBI & Axis Bank cards for 3, 6, and 12-month plans.',
  'schedule':    '📅 Live classes run Mon–Sat. Timings vary by course — check your student portal for the full schedule.',
  'callback':    '📞 Sure! A counselor will call you within 2 hours. Please keep your phone available.',
  'live agent':  '🧑‍💼 Connecting you to a live agent... Expected wait time: ~2 minutes. Thank you for your patience!',
  'password':    '🔑 To reset your password, click "Forgot Password" on the login page or email support@learningfuture.ai.',
  'placement':   '🏢 We have a 98% placement rate with 200+ hiring partners including top startups and MNCs.',
};

const FAQS = [
  { q: 'How do I access live classes?',          a: 'After enrollment, login to your student portal and go to "Live Sessions". You receive a join link 30 minutes before each class via email and SMS.' },
  { q: 'Can I download recorded videos?',        a: 'Yes! All recorded lectures can be downloaded for offline viewing within 30 days. The Elite plan includes lifetime access to all content.' },
  { q: 'What is the refund policy?',             a: 'We offer a 7-day money-back guarantee. If you are not satisfied within the first week, contact our help desk for a full, hassle-free refund.' },
  { q: 'Is EMI available on all plans?',         a: '0% EMI is available on 3, 6, and 12-month plans via HDFC, ICICI, SBI, and Axis Bank credit cards. No processing fee.' },
  { q: 'How do I get my certificate?',           a: 'Certificates are auto-generated once you complete 80% of course content and pass the final assessment. Download directly from your profile page.' },
  { q: 'Can I switch courses mid-way?',          a: 'Yes! You can switch to a different course within 14 days of enrollment without any extra charges. Contact the help desk to initiate.' },
  { q: 'Are the mentors industry professionals?',a: 'Absolutely! All our 50+ mentors are active industry professionals with 5+ years of experience at leading AI companies and research labs.' },
];

/* ---- UTILITIES ---- */
function toggleMenu() {
  const nav = document.querySelector('.nav-links');
  if (nav) nav.classList.toggle('open');
}

function renderCourseCard(c, idx) {
  return `
    <div class="course-card">
      <div class="course-thumb ${c.thumbClass}">${c.icon}</div>
      <div class="course-body">
        <div class="course-tag" style="color:${c.tagColor}">${c.tag}</div>
        <div class="course-title">${c.title}</div>
        <div class="course-desc">${c.desc}</div>
        <div class="course-meta">
          <div class="course-price">${c.price}</div>
          <div class="course-dur">⏱ ${c.dur}</div>
        </div>
        <button class="dropdown-btn" onclick="toggleDD('dd${idx}','arr${idx}')">
          <span>📹 View Classes & Videos</span>
          <span class="dropdown-arrow" id="arr${idx}">▼</span>
        </button>
        <div class="dropdown-content" id="dd${idx}">
          <div class="dropdown-inner">
            ${c.videos.map(v => `
              <div class="video-item">
                <div class="video-icon ${v.type === 'live' ? 'vi-live' : 'vi-recorded'}">${v.type === 'live' ? '🔴' : '▶'}</div>
                <div class="video-info">
                  <div class="video-title">${v.title}${v.badge ? ' <span class="live-badge">LIVE</span>' : ''}</div>
                  <div class="video-sub">${v.sub}</div>
                </div>
              </div>
            `).join('')}
            <button class="upload-btn" onclick="handleUpload()">⬆ Upload Taught Video</button>
          </div>
        </div>
      </div>
    </div>`;
}

function toggleDD(ddId, arrId) {
  const dd  = document.getElementById(ddId);
  const arr = document.getElementById(arrId);
  if (!dd) return;
  dd.classList.toggle('open');
  if (arr) arr.classList.toggle('open');
}

function handleUpload() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'video/*';
  input.onchange = e => {
    if (e.target.files[0]) {
      alert(`✅ Video "${e.target.files[0].name}" uploaded successfully!\nIt will be available to students within 30 minutes after processing.`);
    }
  };
  input.click();
}

function showAlert(id, msg, type) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = msg;
  el.className = `alert alert-${type} show`;
  setTimeout(() => el.classList.remove('show'), 4000);
}

function genStudentId() {
  return 'LF-' + new Date().getFullYear() + '-' + String(Math.floor(Math.random() * 9000) + 1000);
}

/* ---- CHAT ENGINE (used in helpdesk.html) ---- */
function sendChat(preset) {
  const inp  = document.getElementById('chatIn');
  const msgs = document.getElementById('chatMsgs');
  if (!inp || !msgs) return;
  const msg = preset || inp.value.trim();
  if (!msg) return;
  msgs.innerHTML += `<div class="msg-user">${msg}</div>`;
  inp.value = '';
  const key   = Object.keys(CHAT_RESPONSES).find(k => msg.toLowerCase().includes(k));
  const reply = key ? CHAT_RESPONSES[key] : 'Thanks for reaching out! Our team will respond within 2 hours. You can also call us at <strong>1800-AI-LEARN</strong>.';
  setTimeout(() => {
    msgs.innerHTML += `<div class="msg-bot">${reply}</div>`;
    msgs.scrollTop = msgs.scrollHeight;
  }, 650);
  msgs.scrollTop = msgs.scrollHeight;
}

/* ---- PAYMENT CALC (used in payment.html) ---- */
function calcOrder() {
  const courseEl = document.getElementById('courseSelect');
  const durEl    = document.getElementById('durSelect');
  if (!courseEl || !durEl) return;
  const monthly  = parseInt(courseEl.value);
  const dur      = parseInt(durEl.value);
  const discMap  = { 1: 0, 3: 10, 6: 15, 12: 20 };
  const discPct  = discMap[dur] || 0;
  const sub      = monthly * dur;
  const discAmt  = Math.round(sub * discPct / 100);
  const gst      = Math.round((sub - discAmt) * 0.18);
  const total    = sub - discAmt + gst;
  const emi      = Math.round(total / dur);
  const fmt      = n => '₹' + n.toLocaleString('en-IN');

  const set = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
  set('ordDur',   dur + ' Month' + (dur > 1 ? 's' : ''));
  set('ordMon',   fmt(monthly));
  set('ordSub',   fmt(sub));
  set('ordDisc',  discPct ? '-' + fmt(discAmt) : '₹0');
  set('ordGst',   fmt(gst));
  set('ordTotal', fmt(total));
  const emiEl = document.getElementById('emiInfo');
  if (emiEl) emiEl.textContent = dur > 1
    ? `📅 EMI Option: ${fmt(emi)}/month for ${dur} months at 0% interest on HDFC, ICICI, SBI & Axis Bank cards`
    : 'EMI available for 3, 6, and 12-month plans.';
}
