/* OMGN Community Ideas — configure the two public values below. */
(() => {
  'use strict';
  const SUPABASE_URL = 'https://yocvlymzetposjbrfhcb.supabase.co';
  const SUPABASE_PUBLISHABLE_KEY = 'sb_publishable_mtQTzI7bimkoydS2G25Gsw_OIMU0M2w';
  const CATEGORIES = ['Research Topics', 'Methods & Protocols', 'Tools & Resources', 'Collaborations', 'Events & Training', 'Community & Other'];
  const root = document.getElementById('omgn-ideas');
  if (!root) return;
  const status = document.getElementById('ideas-status');
  const list = document.getElementById('ideas-list');
  const filter = document.getElementById('ideas-filter');
  const sort = document.getElementById('ideas-sort');
  const setStatus = msg => { status.textContent = msg; };
  if (SUPABASE_URL.startsWith('PASTE_') || SUPABASE_PUBLISHABLE_KEY.startsWith('PASTE_')) {
    setStatus('Community Ideas is being configured. Please check back soon.');
    document.getElementById('idea-form').hidden = true;
    return;
  }
  if (!window.supabase) { setStatus('Unable to load the discussion service. Please try again later.'); return; }
  const db = window.supabase.createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {auth: {persistSession: false, autoRefreshToken: false}});
  // Private 256-bit browser secret; never exposed in public vote queries.
  const voterKey = 'omgn_ideas_vote_secret_v2';
  let voteSecret = localStorage.getItem(voterKey);
  if (!voteSecret || !/^[0-9a-f]{64}$/.test(voteSecret)) {
    const bytes = crypto.getRandomValues(new Uint8Array(32));
    voteSecret = Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
    localStorage.setItem(voterKey, voteSecret);
  }
  CATEGORIES.forEach(c => { const option = document.createElement('option'); option.value = c; option.textContent = c; filter.append(option); });
  const el = (tag, cls, txt) => { const node = document.createElement(tag); if(cls) node.className = cls; if(txt !== undefined) node.textContent = txt; return node; };
  const date = s => new Date(s).toLocaleDateString('en', {year:'numeric', month:'short', day:'numeric'});
  const errorMessage = e => /rate|limit/i.test(e.message || '') ? 'Please wait before posting again.' : 'Sorry, the operation failed. Please try again.';
  async function load() {
    setStatus('Loading ideas…');
    const {data: ideas, error} = await db.from('ideas').select('id,title,category,description,created_at').order('created_at',{ascending:false}).limit(200);
    if (error) { setStatus(errorMessage(error)); return; }
    const ids = ideas.map(x => x.id);
    let votes = [], comments = [];
    const [vr, cr] = await Promise.all([
      db.rpc('omgn_vote_state', {p_token: voteSecret}),
      ids.length ? db.from('idea_comments').select('id,idea_id,parent_id,body,created_at').in('idea_id', ids).order('created_at',{ascending:true}) : Promise.resolve({data:[],error:null})
    ]);
    if (vr.error || cr.error) { setStatus('Could not load votes or comments.'); return; }
    votes = vr.data || []; comments = cr.data || [];
    const byId = new Map(votes.map(v => [v.idea_id,v]));
    const filtered = ideas.filter(x => !filter.value || x.category === filter.value).map(x => {
      const v = byId.get(x.id);
      return {...x, up: Number(v?.upvotes || 0), down: Number(v?.downvotes || 0), mine: Number(v?.my_vote || 0)};
    });
    if (sort.value === 'top') filtered.sort((a,b) => (b.up-b.down)-(a.up-a.down) || new Date(b.created_at)-new Date(a.created_at));
    list.replaceChildren();
    for (const idea of filtered) list.append(renderIdea(idea, comments.filter(c => c.idea_id === idea.id)));
    setStatus(`${filtered.length} idea${filtered.length === 1 ? '' : 's'}`);
  }
  const pendingVotes = new Set();
  async function vote(idea, value) {
    if (pendingVotes.has(idea.id)) return;
    pendingVotes.add(idea.id);
    const newValue = idea.mine === value ? 0 : value;
    try {
      const {error} = await db.rpc('omgn_cast_vote', {
        p_idea_id: idea.id, p_token: voteSecret, p_value: newValue
      });
      if (error) {
        console.error('OMGN vote error:', error);
        setStatus(`Vote failed: ${error.message || 'Unknown error'}`);
        return;
      }
    } catch (error) {
      console.error('OMGN vote exception:', error);
      setStatus(`Vote failed: ${error.message || 'Network error'}`);
      return;
    } finally {
      // Release the lock BEFORE load() redraws the vote buttons.
      pendingVotes.delete(idea.id);
    }
    await load();
  }
  async function publishComment(ideaId, parentId, input) {
    const body = input.value.trim(); if (!body) return;
    const {error} = await db.from('idea_comments').insert({idea_id:ideaId,parent_id:parentId,body});
    if (error) setStatus(errorMessage(error)); else await load();
  }
  function renderIdea(idea, comments) {
    const card = el('article','idea-card');
    const meta = el('div','idea-meta',`${idea.category} · ${date(idea.created_at)}`);
    card.append(meta, el('h3','idea-title',idea.title));
    if (idea.description) card.append(el('p','idea-description',idea.description));
    const controls = el('div','idea-votes');
    for (const [value,symbol,count] of [[1,'👍',idea.up],[-1,'👎',idea.down]]) {
      const chosen = idea.mine === value;
      const b = el('button', chosen ? (value === 1 ? 'vote-chosen-up' : 'vote-chosen-down') : (idea.mine ? 'vote-inactive' : ''), `${symbol} ${count}`);
      b.type = 'button';
      b.disabled = pendingVotes.has(idea.id);
      b.setAttribute('aria-label', value === 1 ? 'Upvote' : 'Downvote');
      b.setAttribute('aria-pressed', String(chosen));
      b.addEventListener('click', () => vote(idea,value));
      controls.append(b);
    }
    if (idea.mine) controls.append(el('span','vote-confirmation','✓ Vote recorded · click again to remove'));
    card.append(controls);
    const details = el('details','idea-discussion');
    const summary = el('summary','',`Discussion (${comments.length})`); details.append(summary);
    const thread = el('div','idea-thread');
    function commentNode(c, depth=0) {
      const node = el('div','idea-comment'); node.style.marginLeft = `${Math.min(depth,5)*14}px`;
      node.append(el('small','',date(c.created_at)),el('p','',c.body));
      const reply = el('button','idea-reply','Reply'); reply.type='button';
      reply.addEventListener('click',()=>{reply.remove(); node.append(commentForm(idea.id,c.id));});
      node.append(reply);
      for(const child of comments.filter(x=>x.parent_id===c.id)) node.append(commentNode(child,depth+1));
      return node;
    }
    comments.filter(x=>!x.parent_id || !comments.some(y=>y.id===x.parent_id)).forEach(c=>thread.append(commentNode(c)));
    details.append(thread,commentForm(idea.id,null)); card.append(details); return card;
  }
  function commentForm(ideaId,parentId) {
    const form = el('form','idea-comment-form'); const input = el('textarea');
    input.required=true; input.maxLength=1500; input.rows=2; input.placeholder=parentId ? 'Write a reply…' : 'Join the discussion…';
    const button = el('button','',parentId ? 'Post reply' : 'Post comment'); button.type='submit';
    form.append(input,button); form.addEventListener('submit',async e=>{e.preventDefault(); button.disabled=true; await publishComment(ideaId,parentId,input); button.disabled=false;}); return form;
  }
  document.getElementById('idea-form').addEventListener('submit',async e=>{
    const form = e.currentTarget;
    e.preventDefault(); const button=form.querySelector('button'); button.disabled=true;
    const title=document.getElementById('idea-title').value.trim();
    const category=document.getElementById('idea-category').value;
    const description=document.getElementById('idea-description').value.trim();
    if (!title || !CATEGORIES.includes(category)) { button.disabled=false; return; }
    const {error}=await db.from('ideas').insert({title,category,description});
    button.disabled=false;
    if(error) setStatus(errorMessage(error)); else {form.reset(); sort.value='new'; filter.value=''; await load();}
  });
  filter.addEventListener('change',load); sort.addEventListener('change',load); load();
})();
