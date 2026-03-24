---
layout: page
title: Mailing list
---

The OMGN is open to all researchers with an interest in oomycetes, from disciplines ranging from molecular genetics and genomics to biology, population biology, and ecology, at either an experimental or a computational level. Investigators new to the field are always welcome, for example, those interested in saprophytes and animal pathogens.

### How to join?
Simply fill in <a href="https://airtable.com/app4z85HJOGeEMGUc/shrsOfTvREXfUnwoT" target="_blank" rel="noopener">this form</a>.

### How to send a message to the mailing list?
Send an email to omgn-users AT lists DOT oregonstate DOT edu.

### OMGN Mailing List Members

This list brings together members of the oomycete research community. If you would like to join, please use the form above. To update your information or request removal, please contact us.

<div class="mailing-list">

  {% assign people_by_country = site.data.mailing_list | group_by: "country" %}

  {% for country_group in people_by_country %}
    <section class="country-section">
      <h2 class="country-title">{{ country_group.name }}</h2>
      <hr class="country-rule" />

      <div class="people-columns">
        {% for person in country_group.items %}
          {% assign parts = person.name | split: "," %}
          {% assign surname = parts[0] | strip | upcase %}
          {% assign given = parts[1] | default: "" | strip %}

          <div class="person">
            <span class="person-name">
              {% if given != "" %}
                {{ surname }}, {{ given }}
              {% else %}
                {{ person.name }}
              {% endif %}
            </span>
            <span class="person-meta">
              &nbsp;— {{ person.affiliation_main }}
            </span>
          </div>
        {% endfor %}
      </div>
    </section>
  {% endfor %}

</div>
