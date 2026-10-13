---
layout: page
title: Community Ideas
description: Share, discuss and vote on ideas for the Oomycete Molecular Genetics Network.
permalink: /ideas/
---

Help shape the future of OMGN. Suggest an idea, support a proposal, or join a discussion. No account is required. Contributions are published immediately and may be moderated afterwards.

<div id="omgn-ideas" class="ideas-app">
  <form id="idea-form" class="ideas-form">
    <h2>Suggest an idea</h2>
    <label for="idea-title">Title</label>
    <input id="idea-title" maxlength="140" required placeholder="What would you like the OMGN community to do?">
    <label for="idea-category">Category</label>
    <select id="idea-category" required>
      <option value="Research Topics">Research Topics</option>
      <option value="Methods & Protocols">Methods &amp; Protocols</option>
      <option value="Tools & Resources">Tools &amp; Resources</option>
      <option value="Collaborations">Collaborations</option>
      <option value="Events & Training">Events &amp; Training</option>
      <option value="Community & Other">Community &amp; Other</option>
    </select>
    <label for="idea-description">Description (optional)</label>
    <textarea id="idea-description" maxlength="2000" rows="3" placeholder="Add context or explain your suggestion"></textarea>
    <button type="submit">Publish idea</button>
  </form>
  <div class="ideas-toolbar">
    <label for="ideas-filter">Category</label><select id="ideas-filter"><option value="">All categories</option></select>
    <label for="ideas-sort">Sort</label><select id="ideas-sort"><option value="top">Top rated</option><option value="new">Newest</option></select>
  </div>
  <p id="ideas-status" role="status" aria-live="polite"></p>
  <div id="ideas-list"></div>
</div>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.js" defer></script>
<script src="{{ '/assets/js/community-ideas.js' | relative_url }}" defer></script>
