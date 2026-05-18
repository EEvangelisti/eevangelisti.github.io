---
layout: home
title: Oomycete Molecular Genetics Network (OMGN)
---

<div style="text-align:center; margin: 2rem 0;">
  <img src="{{ site.baseurl }}/assets/images/logo/logo.png"
       alt="Oomycete Molecular Genetics Network (OMGN)"
       style="max-width:500px; width:100%; height:auto;">
</div>


## **Newly Elected Steering Committee Members**

We are delighted to announce the four newly elected members to the Oomycete Steering Committee.
Many thanks to all members of the community who cast their vote, and to all 
candidates for their willingness to contribute to the future of our community.
We look forward to fruitful interactions and collaborations ahead.

<div class="committee-list">
{% for p in site.data.elections %}
  <div class="member">
    <img src="{{ site.baseurl }}/assets/images/steering/{{ p.photo }}" alt="{{ p.name }}">
    <div class="member-info">
      <div class="member-name">
        {% if p.url %}
          <a href="{{ p.url }}" target="_blank" rel="noopener">{{ p.name }}</a>
        {% else %}
          {{ p.name }}
        {% endif %}
      </div>
      <div class="member-role">{{ p.role }}</div>
      <div class="member-affiliation">{{ p.affiliation }}</div>
    </div>
  </div>
{% endfor %}
</div>


---

The **Oomycete Molecular Genetics Network (OMGN)** brings together researchers 
working on the molecular, cellular and genetic foundations of oomycete biology.

Oomycetes are filamentous eukaryotes that include some of the most devastating 
plant pathogens affecting global food security and ecosystem resilience. Despite 
their agronomic importance, their molecular mechanisms remain comparatively 
understudied relative to fungi.

OMGN was created to foster exchange, collaboration and methodological innovation 
within the oomycete research community.

### Our objectives

- Promote advances in molecular genetics and functional genomics  
- Encourage the development and sharing of tools and resources  
- Support early-career researchers  
- Facilitate international collaboration  

<!-- Inactive for the moment (but keep it for later)

<div class="info-box">
<span style="color: firebrick;"><b>The OMGN Steering Committee (SC) is soliciting nominations to fill four SC member positions.</b></span>
More information on roles of OMGN SC and a current list of SC members can be found
<a href="{{ site.baseurl }}/committee" target="_blank" rel="noopener">here</a>.
Self-nominations are welcome. Please submit one nomination per form.
Nominations will be reviewed by the current Steering Committee and used to assemble a balanced slate (career stage, geography, research areas, etc) for voting.
Please submit your nominations by <b>March 31, 2026</b> using the link below:

<div style="text-align: center; margin-top: 0.6em;">
  <a href="https://forms.office.com/Pages/ResponsePage.aspx?id=HmwhqGNNUkOMO1D6HxR1sXjxC4XIJzZKletlr31P9mFUQk81TTY0NlVaMUQ4R0xUU0hEN0xWQjFNNC4u&wdLOR=cD378959B-7CAE-C749-9A60-48E6FEBC5AD1" target="_blank" rel="noopener">
    OMGN Steering Committee Member Nomination – Fill out form
  </a>
</div>
</div>
-->
---
*Connecting researchers. Advancing oomycete biology. Strengthening our community.*

