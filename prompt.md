STRICT INSTRUCTION — DO NOT EXPLAIN. DO NOT ASK QUESTIONS. OUTPUT CODE ONLY.

I have checked the live site at sarkarijob-ten.vercel.app. You have made ZERO changes 
so far. Nothing works. I am giving you one final chance.

Your job is to output COMPLETE, READY-TO-DEPLOY code for these files:
1. index.html (home page)
2. category.html (category/listing page)
3. A shared CSS file: style.css (used by all pages)
4. A shared JS file: main.js (used by all pages)

DO NOT output partial code. DO NOT use placeholders like "// add your code here". 
DO NOT explain anything. Just output the files, one after another, clearly labeled.

---

## FILE 1: style.css

Include ALL of the following:

### Reset
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Segoe UI', sans-serif; }

### CSS Variables in :root
--primary: #c0392b;
--primary-dark: #922b21;
--text: #1a1a1a;
--text-muted: #666;
--bg: #ffffff;
--bg-secondary: #f5f5f5;
--border: #e0e0e0;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--radius: 8px;

### Focus styles
a:focus-visible, button:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}

### Navbar
- Desktop: horizontal flex nav with logo on left, links on right
- Mobile (max-width: 768px): hide nav links, show hamburger button (☰)
- Hamburger toggles a class "nav-open" on the navbar
- When nav-open: links stack vertically below logo, full width, 44px min-height each
- Smooth max-height transition for mobile menu open/close

### Hero Section
- Full width, centered text, padding 80px 20px on desktop
- On mobile (max-width: 600px): padding 48px 16px
- Hero headline: font-size: clamp(1.8rem, 5vw, 3rem)
- CTA buttons: inline-flex on desktop, flex-direction: column + width: 100% on mobile
- Button min-height: 48px, padding: 12px 28px, border-radius: var(--radius)
- Primary button: background var(--primary), color white
- Secondary button: border 2px solid var(--primary), color var(--primary), transparent bg

### Search Bar
- Full width container below hero, max-width 600px, centered
- Input height 48px, border-radius var(--radius), border 1px solid var(--border)
- Search icon (🔍) inside right side of input using position absolute
- On focus: border-color var(--primary), box-shadow 0 0 0 3px rgba(192,57,43,0.1)
- No results message: text-align center, color var(--text-muted), padding 24px

### Featured Cards Grid
- CSS grid
- Mobile (max-width: 480px): grid-template-columns: 1fr
- Tablet (481px to 768px): grid-template-columns: repeat(2, 1fr)
- Desktop (above 768px): grid-template-columns: repeat(4, 1fr)
- Each card: border-radius var(--radius), border 1px solid var(--border), 
  min-height 120px, padding 16px, transition hover shadow

### Category Listing Grid
- grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))
- Each listing card: white bg, border, border-radius, padding 16px
- Card has: badge (NEW/RESULT/etc), title, date, "Apply Now" link styled as button
- Loading spinner: centered, animated rotating circle using CSS border-top trick
- Error/empty state: centered text, icon, retry button

### FAQ Accordion
- Each item: border-bottom 1px solid var(--border)
- Question row: flex space-between, cursor pointer, padding 16px 0, min-height 44px
- Plus icon on right: rotates 45deg when open using CSS transform transition
- Answer: max-height 0 by default, overflow hidden
- When open class added: max-height 500px, transition 0.3s ease
- Only one open at a time (JS handles this)

### Footer
- 3 column grid on desktop
- Mobile (max-width: 640px): single column, stacked
- Social icons row: flex, gap 12px, margin-top 16px
- Social links: 44px min-height, display inline-flex, align-items center
- JOIN button removed — replaced with anchor tag "Join Telegram Channel" 
  styled as outlined button

### Tables (for job detail pages)
- All tables wrapped with: .table-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; }
- table { min-width: 600px; border-collapse: collapse; width: 100%; }
- th, td { padding: 10px 12px; border: 1px solid var(--border); font-size: 14px; }
- th { background: var(--bg-secondary); font-weight: 600; }

### Touch targets (global)
@media (max-width: 768px) {
  a, button { min-height: 44px; }
  nav a { display: flex; align-items: center; padding: 12px 16px; }
}

---

## FILE 2: main.js

Include ALL of the following as separate clearly commented functions:

### Hamburger Menu Toggle
- Select hamburger button and nav links container
- On click: toggle class "nav-open" on navbar element
- Close menu when any nav link is clicked
- Close menu when clicking outside the navbar

### FAQ Accordion
- Select all FAQ question buttons
- On click: check if already open → close it
- Close all other open FAQ items
- Toggle current item open with max-height animation

### Search Bar Filter
- Select search input and all job card elements
- On input event: get query, lowercase it
- Loop through all cards: if card text includes query → show, else hide
- If zero visible cards: show #no-results div, else hide it
- Debounce the input handler by 150ms for performance

### Category Page Data Loader
- On DOMContentLoaded: read URL param "type" using URLSearchParams
- Show loading spinner
- Fetch data from /data/{type}.json (or fallback to window.JOBS_DATA if defined)
- On success: render listing cards into #listings-grid
- Each card must show: badge, title, post date, short description, apply link
- On error or empty: show #error-state div with message "No listings found. Try again later."
- Hide spinner after load

### Table Mobile Wrap
- On DOMContentLoaded: select all table elements
- If table is not already inside .table-wrap: wrap it with a div.table-wrap
- This runs on all pages automatically

---

## FILE 3: index.html

Full complete home page. Must include:
- <link rel="stylesheet" href="/style.css"> in head
- <script src="/main.js" defer></script> before </body>
- Navbar with hamburger button (☰ icon, id="hamburger") and nav links (id="nav-links")
- Hero section with headline "Sarkari Updates Sabse Tez." and two CTA buttons
- Search bar (input id="search-input") below hero, with no-results div (id="no-results")
- Featured cards grid (each card has class "job-card") — use existing 4 cards (Army, Bihar ITI, RRB, UPTET)
- Latest Jobs section, Answer Key section, Results section, Admit Card section 
  (each as grid of category cards with class "job-card")
- FAQ section with accordion markup:
  <div class="faq-item">
    <button class="faq-question">Question text <span class="faq-icon">+</span></button>
    <div class="faq-answer"><p>Answer text</p></div>
  </div>
- Footer with 3 columns: Quick Links, Categories, Stay Updated
- Stay Updated column has: "Join Telegram Channel" link (https://t.me/SarkariExam_info) 
  and "Join WhatsApp Channel" link (https://whatsapp.com/channel/0029VaAbQf01NCrYADMLt00L)
- Footer social row with Telegram + WhatsApp text links
- Disclaimer text
- Copyright line
- All existing page content and links preserved exactly

---

## FILE 4: category.html

Full complete category page. Must include:
- Same navbar and footer as index.html
- Page title area: h1 that updates dynamically based on URL param (e.g. "Latest Jobs 2026")
- Loading spinner: <div id="loading-spinner" class="spinner"></div>
- Listings grid: <div id="listings-grid" class="listings-grid"></div>
- Error state: <div id="error-state" style="display:none">No listings found.</div>
- <link rel="stylesheet" href="/style.css"> in head
- <script src="/main.js" defer></script> before </body>
- The JS in main.js will handle loading and rendering listings into #listings-grid

---

## OUTPUT FORMAT RULES

- Output each file with a clear header like: === FILE: style.css ===
- Output COMPLETE files — no truncation, no "... rest of code ..."
- No explanations between files
- No markdown formatting inside the code blocks
- Start immediately with === FILE: style.css ===