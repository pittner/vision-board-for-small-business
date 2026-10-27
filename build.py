#!/usr/bin/env python3
"""Builds index.html for pittner/vision-board-for-small-business.

A single-purpose page for the seasonal "small business vision board" / "business goals 2027" intent
(owners plan the next year in November-January): 36 business goals in 6 groups, each with why it
matters and a first step the owner can do this week, and a link that opens the free maker with that
goal and step already filled in (?goal=&step=&layout=text&mode=wallpaper, T-098), so it can go on the
owner's phone or be printed for the office wall. Plus 12 questions for a year-end review, a 45-minute
plan, a box for your own business goal, and FAQ.

No dependencies. Run: python3 build.py
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/vision-board-for-small-business/"
SRC = "ghpages_business"
CAMPAIGN = "business_2027"

# (group, [(business goal, why it matters, a first step the owner does this week)])
GROUPS = [
    ("Customers", [
        ("Ten new customers a month", "A clear number turns marketing into a habit.", "List 20 people who could buy or refer, and message the first five"),
        ("Ask every happy customer for a review", "Reviews sell while you sleep.", "Send a review link to your last three happy customers"),
        ("Win back customers who went quiet", "A past customer is the cheapest sale you will ever make.", "Export customers who have not bought in 6 months and write to five"),
        ("One referral a week", "Your best customers know people like them.", "Ask one loyal customer who else should know about you"),
        ("Answer every enquiry within an hour", "Speed beats price for many buyers.", "Turn on phone notifications for your contact form today"),
        ("A newsletter people actually open", "An email list is the one audience no platform can take away.", "Write a five-line update and send it to your list on Friday"),
    ]),
    ("Money", [
        ("Raise prices by 10%", "Most small businesses charge too little for the value they give.", "Pick one product or service and set the new price for new customers"),
        ("Three months of costs in reserve", "A cash buffer turns a bad month into a calm month.", "Open a separate savings account and move the first amount"),
        ("Pay yourself every month", "A business that cannot pay its owner is a hobby with risk.", "Set a fixed owner salary and a date for it in the calendar"),
        ("Invoices paid within 30 days", "Unpaid invoices are an interest-free loan to your customers.", "Chase every invoice older than 30 days this week"),
        ("Know your numbers every Monday", "Ten minutes with the numbers beats a surprise at year end.", "Make a sheet with revenue, costs and cash, and fill it in on Monday"),
        ("Cut one cost that adds nothing", "Small subscriptions add up quietly.", "Go through last month's bank statement and cancel one thing"),
    ]),
    ("Product and offer", [
        ("Launch one new product or service", "Something new gives customers a reason to come back.", "Ask five customers what they wish you also offered"),
        ("A clear offer on one page", "If people cannot see what you sell in 10 seconds, they leave.", "Write your offer in three sentences and read it to a friend"),
        ("A monthly package with repeat revenue", "Repeat revenue makes every month easier to plan.", "Sketch one subscription or retainer and price it"),
        ("Fix the most common complaint", "One fix can stop the same problem a hundred times.", "Read your last 20 reviews or emails and name the top complaint"),
        ("Better photos of what you sell", "People buy what they can see clearly.", "Take new photos of your three best sellers in daylight"),
        ("Sell online, not only in person", "An online shop takes orders after closing time.", "List your three best sellers on one online channel"),
    ]),
    ("Team and systems", [
        ("Hire the first helper", "Your time is the bottleneck of the whole business.", "Write down every task you did this week that someone else could do"),
        ("Write down how we do things", "A written process lets you take a holiday.", "Record the steps of one repeated task the next time you do it"),
        ("A weekly team meeting of 20 minutes", "Short and regular beats long and rare.", "Pick the day and send the invite with three fixed questions"),
        ("Automate one boring task", "Every hour saved each week is 50 hours a year.", "Pick the task you hate most and look for one tool that does it"),
        ("A tidy shared calendar and inbox", "Fewer missed messages, fewer missed sales.", "Archive everything older than 30 days and set up two folders"),
        ("Train someone to cover for you", "A business that needs you every day owns you.", "Choose who and show them one task this week"),
    ]),
    ("Brand and marketing", [
        ("Post useful content every week", "Being seen regularly beats going viral once.", "Write down 12 customer questions, one post per week"),
        ("A Google Business profile with fresh photos", "Most local customers check it before they call.", "Add five new photos and your opening hours today"),
        ("One local partnership", "A neighbour business shares your customers, not your product.", "Name three local businesses and visit one this week"),
        ("A website that loads fast on a phone", "Most visitors arrive on a phone and leave in seconds.", "Open your site on your phone and note the three biggest problems"),
        ("Show up at one event per quarter", "People buy from people they have met.", "Find the next local fair or meetup and put it in the calendar"),
        ("Collect ten customer stories", "A real story convinces more than any ad.", "Ask one customer for a two-sentence quote you can share"),
    ]),
    ("Owner wellbeing", [
        ("Weekends off", "A rested owner makes better decisions.", "Set an email auto-reply for this Saturday and Sunday"),
        ("Two weeks of real holiday in 2027", "If the business survives two weeks without you, it is a business.", "Pick the two weeks and put them in the calendar now"),
        ("Stop work at 6 pm", "Evenings are where energy comes back.", "Set a daily 6 pm alarm called 'close the laptop'"),
        ("Learn one new business skill", "The owner's skills are the ceiling of the business.", "Choose one course or book and block one hour a week"),
        ("A mentor or peer group", "Others have already solved your problem.", "Message one owner you admire and ask for 20 minutes"),
        ("Celebrate every milestone", "Noticing progress keeps you going in the hard months.", "Write down three wins from 2026 and share them with your team"),
    ]),
]

QUESTIONS = [
    "What was the best decision we made in 2026?",
    "Which customers brought the most money and the least stress?",
    "What did we sell the most of, and what barely sold?",
    "Where did most new customers come from?",
    "What took the most time for the least money?",
    "Which task should the owner stop doing in 2027?",
    "What do customers complain about or ask for again and again?",
    "What would we do if we had twice the time?",
    "What would we stop if we had half the time?",
    "How much do we want to earn in 2027, and from how many customers?",
    "What one change would make next December calmer?",
    "If 2027 goes really well, what is different a year from now?",
]

PLAN = [
    ("10 minutes: look back.", "Write three wins and three problems of 2026. Look at real numbers: revenue, customers, hours worked."),
    ("15 minutes: answer the questions.", "Go through the 12 questions below, alone or with your team. Short answers are fine."),
    ("10 minutes: pick three business goals.", "One for customers or money, one for the product or team, one for yourself as the owner."),
    ("10 minutes: make it visible.", "Turn your most important goal and its first step into a phone lock screen, print it for the office wall, or make a full board."),
]

FAQ = [
    ("What is a small business vision board?",
     "A board with the goals of your business for the coming year, such as more customers, higher prices, a first hire or weekends off. "
     "It keeps the year's priorities in front of you, so daily work does not push them aside."),
    ("How do you make a vision board for your business?",
     "Look back at the year with real numbers, answer a few honest questions, pick three business goals and make them visible. "
     "This page has 36 business goals with a first step, 12 year-end review questions and a 45-minute plan."),
    ("What should I put on a business vision board?",
     "Goals for customers, money, your product, your team, your marketing and yourself as the owner. "
     "Add one first step to each goal so the board says what to do this week, not only what to hope for."),
    ("Is a vision board useful for a business, not only personal goals?",
     "Yes, if it is concrete. A number, a date and a first step turn a wish into a plan you see every time you unlock your phone."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image to a phone or print it for the office."),
    ("Can I make a full vision board with several business goals?",
     "Yes. Start from your business goal in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Small Business Vision Board 2027: %%COUNT%% Business Goals, %%NQ%% Year-End Questions &amp; a Free Maker</title>
<meta name="description" content="Plan 2027 for your small business: %%COUNT%% business goals, each with a first step for this week, %%NQ%% year-end review questions and a 45-minute plan. Turn your goal into a free lock screen or a page for the office wall. No signup.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Small business vision board 2027 - %%COUNT%% business goals and a free maker">
<meta property="og:description" content="Business goals with a first step, %%NQ%% year-end questions, and a lock screen or office page in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#1D4ED8;--bg:#F8FAFD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#1E40AF;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Small business vision board 2027: %%COUNT%% business goals with a first step for this week</h1>
  <p class="lede">December is when owners finally have an hour to think about the business instead of working in it. Use that hour to plan 2027. Below are %%COUNT%% goals for a small business, each with why it matters and a first step you can do this week, plus %%NQ%% honest year-end questions. Press a goal and it opens in a free maker with the first step under it: save it as your phone lock screen or print it for the office wall. No signup, nothing uploaded.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% year-end questions &middot; 45-minute plan &middot; lock screen or office page &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your business goal?</h2>
  <div class="row">
    <div><label for="ownGoal">My business goal for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. Ten new customers a month" autocomplete="off"></div>
    <div><label for="ownStep">First step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Message five past customers on Monday" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, then save it to your phone or print it for the office.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% year-end questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% year-end questions before you choose</h2>
  <p>Answer them alone or with your team. Use real numbers where you can. The answers that surprise you point to your business goals.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Plan your business year in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with several goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full vision board around my business goals</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/vision-board-for-family/">family vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/vision-board-party-kit/">vision board party kit</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/vision-board-for-small-business">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own business goal: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your business goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()
