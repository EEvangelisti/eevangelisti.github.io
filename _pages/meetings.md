---
layout: page
title: Meetings
---

The OMGN network aims to provide a platform for discussion ranging from fundamental cell biology to translational plant protection strategies.

<span style="color: firebrick;"><b>Update (February 2026): Discussions are currently ongoing regarding the next OMGN meeting. Stay tuned!</b></span>



<div class="meetings-page">

{% assign sorted = site.data.omgn-meetings | sort: "year" | reverse %}

{% for m in sorted %}

  <div class="meeting">

    <div class="group-picture">
      <img src="{{ site.baseurl }}/assets/meetings/group-pictures/{{ m.group-picture }}"
           alt="OMGN {{ m.year }}">
    </div>

    <div class="meeting-title">
      OMGN {{ m.year }} ({{ m.date }})
    </div>

    <div class="meeting-description">
        {{ m.description }}
    </div>

    <div class="meeting-organizers">
        <b>Local organizers:</b> {{ m.organizers }}
    </div>

    <div class="meeting-links">
      {% if m.website %}
        <a href="{{ m.website }}" target="_blank" rel="noopener">Meeting website</a>
      {% endif %}

      {% if m.abstract-book %}
        ·
        <a href="{{ site.baseurl }}/assets/meetings/abstract-books/{{ m.abstract-book }}">
          Abstract book (PDF)
        </a>
      {% endif %}

    </div>

  </div>

{% endfor %}

</div>



## Older meetings

<table class="meetings-table">

  <thead>
    <tr>
      <th>Date</th>
      <th>Location</th>
      <th>Book</th>
      <th>Photo</th>
    </tr>
  </thead>

  <tbody>

  {% assign sorted = site.data.old-omgn-meetings | sort: "year" | reverse %}

  {% for m in sorted %}
    <tr>

      <td>
        {% if m.date %}
          {{ m.date }}, <b>{{ m.year }}</b>
        {% else %}
          —
        {% endif %}
      </td>

      <td>{{ m.location }} ({{ m.country }})</td>

      <td class="icon-cell">
        {% if m.abstract_book %}
          <a href="{{ site.baseurl }}/assets/meetings/abstract-books/{{ m.abstract_book }}" target="_blank" rel="noopener">
            <img src="{{ site.baseurl }}/assets/images/icons/book_3725.png" alt="PDF" class="icon">
          </a>
        {% else %}
          —
        {% endif %}
      </td>

      <td class="icon-cell">
        {% if m.group_picture %}
          <a href="{{ site.baseurl }}/assets/meetings/group-pictures/{{ m.group_picture }}" target="_blank" rel="noopener">
            <img src="{{ site.baseurl }}/assets/images/icons/photocamera_83746.png" alt="JPG" class="icon">
          </a>
        {% else %}
          —
        {% endif %}
      </td>

    </tr>
  {% endfor %}

  </tbody>

</table>


