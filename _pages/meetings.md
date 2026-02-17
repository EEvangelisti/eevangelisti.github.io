---
layout: page
title: Meetings
---

The OMGN network aims to provide a platform for discussion ranging from fundamental cell biology to translational plant protection strategies.

## Upcoming meeting

Discussions ongoing.


## Past meetings

<div class="meetings-page">

{% assign sorted = site.data.meetings | sort: "year" | reverse %}

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
        <a href="{{ m.website }}" target="_blank" rel="noopener">Website</a>
      {% endif %}

      {% if m.abstract_book %}
        ·
        <a href="{{ site.baseurl }}/assets/abstract-books/{{ m.abstract_book }}">
          Abstract book (PDF)
        </a>
      {% endif %}

    </div>

  </div>

{% endfor %}

</div>



## Older meetings

|**Date**|**Location**|**Country**|
|2019, July 10-13|Oban|United Kingdom|
|2018, July 14-17|Malmö|Sweden|
|2017, March 11-14|Asilomar Conference Grounds|California, USA|
|2014, July 2-4|Norwich|United Kingdom|
|2013|Asilomar Conference Grounds|California, USA|
|2012|Nanjing|China|
