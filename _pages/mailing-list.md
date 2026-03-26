---
layout: page
title: Mailing list
---

The OMGN is open to all researchers with an interest in oomycetes, from disciplines ranging from molecular genetics and genomics to biology, population biology, and ecology, at either an experimental or a computational level. Investigators new to the field are always welcome, for example, those interested in saprophytes and animal pathogens.

- To join, fill in <a href="https://airtable.com/app4z85HJOGeEMGUc/shrsOfTvREXfUnwoT" target="_blank" rel="noopener">this form</a>.
- To send an email to the mailing list, email omgn-users AT lists DOT oregonstate DOT edu.
- To update your information or request removal, <a href="mailto:contact@oomycetes.com">contact us</a>.

Current members are listed below.

<table class="mailing-table">
  <thead>
    <tr>
      <th>Last name</th>
      <th>First name</th>
      <th>Affiliation</th>
      <th>Country</th>
    </tr>
  </thead>
  <tbody>

    {% assign sorted = site.data.mailing_list | sort: "sort_name" %}

    {% for person in sorted %}
      <tr>
        <td class="last-name">{{ person.last_name }}</td>
        <td>{{ person.first_name }}</td>
        <td class="meta">{{ person.affiliation_main }}</td>
        <td class="meta">{{ person.country }}</td>
      </tr>
    {% endfor %}

  </tbody>
</table>
