# 🤖 Learning Future With Us — AI Coaching Institute Portal

## Complete Multi-Page Web Application
### Built with Pure HTML, CSS & JavaScript (No frameworks required)

---

## 📁 Project Structure

```
learning-future/
├── index.html          ← Home page (Hero, Stats, Categories, Testimonials)
├── courses.html        ← All 7 courses with dropdowns, live & recorded videos
├── fees.html           ← Fee structure, plan comparison table, EMI info
├── login.html          ← Student login + registration + profile preview
├── backend.html        ← Admin data sheet (search, filter, export CSV, add student)
├── helpdesk.html       ← AI chatbot, FAQ accordion, ticket system, contact info
├── payment.html        ← Full payment gateway (Card/UPI/Net Banking/EMI)
├── css/
│   └── style.css       ← Complete shared stylesheet (all pages)
└── js/
    └── main.js         ← Shared data (courses, students, FAQs) + utilities
```

---

## 🚀 How to Run in VS Code

### Method 1: Live Server (Recommended — Hot Reload)
1. Open VS Code
2. Install the **"Live Server"** extension by Ritwick Dey
   - Go to Extensions (Ctrl+Shift+X)
   - Search: `Live Server`
   - Click Install
3. Open the `learning-future/` folder in VS Code
4. Right-click `index.html` → **"Open with Live Server"**
5. Browser opens at `http://127.0.0.1:5500/index.html`

### Method 2: Direct Browser Open
1. Navigate to the `learning-future/` folder on your computer
2. Double-click `index.html`
3. It opens directly in your default browser
4. ✅ All navigation links work between pages

### Method 3: VS Code Preview
1. Open any `.html` file in VS Code
2. Press `Ctrl+Shift+V` to open built-in preview

---

## 🌐 Pages & Features

| Page | File | Key Features |
|------|------|-------------|
| 🏠 Home | `index.html` | Hero, floating cards, stats, 3 category cards, testimonials, CTA |
| 📚 Courses | `courses.html` | 7 courses, tab filter, dropdown with live/recorded videos, upload button |
| 💰 Fees | `fees.html` | 3 plan cards, comparison table, EMI info, discount grid |
| 🔐 Login | `login.html` | Login + Register tabs, avatar picker, profile preview, dashboard |
| 🗄️ Backend | `backend.html` | Data table, search/filter, add student modal, CSV export, bar charts |
| 🎧 Help Desk | `helpdesk.html` | AI chatbot, quick chips, ticket form, FAQ accordion, contact cards |
| 💳 Payment | `payment.html` | Card/UPI/NetBank/EMI selector, animated card visual, order summary, coupons |

---

## 🎯 Demo Instructions

### Login Page
- Use any Student ID from backend (e.g. `LF-2024-0001`)
- Password: `demo123`

### Coupon Codes (Payment Page)
- `LAUNCH25` — 25% off first month
- `STUDENT10` — 10% student discount
- `PATNA20` — 20% off for Patna students

### Chatbot Keywords (Help Desk)
Type any of these in the chat:
- `fee` / `course` / `emi` / `certificate`
- `refund` / `placement` / `schedule` / `password`

### Backend Admin
- Search students by name, ID, or course
- Filter by status (Active / Pending / Inactive)
- Filter by plan (Starter / Professional / Elite)
- Click **View** to see full student profile modal
- Click **Edit** to cycle through status
- Click **Del** to remove a student
- Click **+ Add Student** to add new records
- Click **⬇ Export CSV** to download the data sheet

---

## 🎨 Design System

| Token | Value |
|-------|-------|
| Primary Accent | `#f7c948` (Gold) |
| Secondary | `#ff6f61` (Coral) |
| Tertiary | `#00e5c3` (Teal) |
| Background | `#0d0520` → `#1a0533` → `#0d1b6e` |
| Font Display | Syne (Google Fonts) |
| Font Body | DM Sans (Google Fonts) |

---

## 📱 Responsive Breakpoints
- **Desktop**: Full layout (all columns visible)
- **Tablet (≤860px)**: Stacked hero, hamburger menu
- **Mobile (≤500px)**: Single column, compact tables

---

## 🔧 Customization Guide

### Change Institute Name
Search & replace `Learning Future With Us` in all HTML files.

### Add a New Course
In `js/main.js`, add an entry to the `COURSES` array:
```javascript
{
  id: 'c8', cat: 'foundations',   // or 'applied' / 'advanced'
  icon: '🔬', thumbClass: 'thumb-yellow',
  tagColor: '#f7c948', tag: 'AI Foundations',
  title: 'Your Course Name',
  desc: 'Course description here.',
  price: '₹4,999/mo', dur: '8 Weeks',
  videos: [
    { type: 'live',     title: 'Live Session Name', sub: 'Live · Day Time', badge: true },
    { type: 'recorded', title: 'Recorded Video Name', sub: '45 min · HD' },
  ]
}
```

### Add New Students to Backend
Edit the `BACKEND_DATA` array in `js/main.js`.

### Add FAQ Questions
Edit the `FAQS` array in `js/main.js`.

### Change Colors
Edit the CSS variables at the top of `css/style.css`:
```css
:root {
  --accent:  #f7c948;   /* Main gold */
  --accent2: #ff6f61;   /* Coral */
  --accent3: #00e5c3;   /* Teal */
}
```

---

## ✅ Browser Compatibility
- Chrome 90+ ✅
- Firefox 88+ ✅
- Edge 90+ ✅
- Safari 14+ ✅
- Mobile Chrome / Safari ✅

---

## 📦 Dependencies
**None!** This is a pure vanilla HTML/CSS/JS project.
- Google Fonts loaded via CDN (requires internet for fonts)
- No npm, no node_modules, no build step required

---

*© 2026 Learning Future With Us — World Class AI Education*
