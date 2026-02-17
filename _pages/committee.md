---
layout: page
title: Steering Committee
---

## Gouvernance
The OMGN is governed by a Steering Committee, hereafter named OMGN-SC. The 
OMGN-SC has twelve members and two *ex officio* members. The members are either 
elected by the participants of the OMGN meeting or selected by the 
OMGN-SC. At each meeting two new members are elected by the community 
and one new member is selected by the OMGN-SC. Membership is for a term of six 
years, or longer depending on circumstances. Two co-chairs (one US, one non-US) 
are elected by the members of the committee.

### Roles of the OMGN-SC
- Appoint two people as Scientific Chairs and Organizers of the OMGN meeting.
- Provide feedback to the Scientific Chairs to ensure that there is balance in all aspects of the scientific program, including speakers that represent broad areas of oomycete biology, junior and senior speakers, and all other dimensions of diversity in the community.
- Provide feedback to the Organizers on the invited key-note.
- Provide feedback to the Organizers on issues arising about the site and logistics of the meeting.
- Provide support to the Organizers on issues related to funding and sponsoring.
- Solicit requests for proposals for upcoming OMGN meetings.
- Decide on the location of upcoming OMGN meetings with a preference for alternating between North America and Eurasia.

### Role of the Scientific Chairs
The Scientific Chairs organize the OMGN meeting, and in particular:
- Publicize the meeting.
- Publicize calls for abstracts.
- Curate the abstracts.
- Select speakers for oral presentations.
- Propose a keynote speaker.
- Assemble the scientific program in consultation with the OMGN-SC.



## Current OMGN-SC members

<div class="committee-list">
{% for p in site.data.committee %}
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

