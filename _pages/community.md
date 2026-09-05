---
layout: page
title: Community
---

The OMGN is open to all researchers with an interest in oomycetes, from disciplines ranging from molecular genetics and genomics to biology, population biology, and ecology, at either an experimental or a computational level. Investigators new to the field are always welcome, for example, those interested in saprophytes and animal pathogens.

### Joining the OMGN community
- To join the community, fill in <a href="https://airtable.com/app4z85HJOGeEMGUc/shrsOfTvREXfUnwoT" target="_blank" rel="noopener">this form</a>.
- Your name and affiliation will appear in the list below. It is updated every hour. Please allow some time for recent registrations or changes to appear.
- To update your information or request removal, <a href="mailto:contact@oomycetes.com">contact us</a>.

### Mailing list
After your registration with the OMGN community has been reviewed, you will 
receive an invitation to join our mailing list, hosted on Google Groups. 
Invitations are sent manually, so please allow some time for processing.

Once you have joined, you can email the entire mailing list at
<b>omgn-users AT googlegroups DOT com</b>. Standard mailing-list netiquette 
applies.


### OMGN community members

<div class="mailing-list-controls">
  <input
    type="search"
    id="mailing-list-search"
    placeholder="Search by name, affiliation, or country..."
    aria-label="Search the mailing list"
  >
</div>

<div class="mailing-list-alphabet" id="mailing-list-alphabet" aria-label="Filter by last name initial">
  <button type="button" data-letter="" class="active">All</button>
  {% assign letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" | split: "" %}
  {% for letter in letters %}
    <button type="button" data-letter="{{ letter }}">{{ letter }}</button>
  {% endfor %}
</div>

<table class="mailing-table" id="mailing-table">
  <thead>
    <tr>
      <th data-column="last_name">Name<span class="sort-indicator"></span></th>
      <th data-column="affiliation_main">Affiliation<span class="sort-indicator"></span></th>
      <th data-column="country">Country<span class="sort-indicator"></span></th>
    </tr>
  </thead>
  <tbody>
    {% assign sorted = site.data.mailing_list | sort: "sort_name" %}
    {% for person in sorted %}
      <tr>
        <td data-value="{{ person.last_name | append: ' ' | append: person.first_name | downcase }}">
          {{ person.last_name }}{% if person.first_name != "" %}, {{ person.first_name }}{% endif %}
        </td>
        <td data-value="{{ person.affiliation_main | downcase }}">{{ person.affiliation_main }}</td>
        <td data-value="{{ person.country | downcase }}">{{ person.country }}</td>
      </tr>
    {% endfor %}
  </tbody>
</table>

<script>
document.addEventListener("DOMContentLoaded", function () {
  const table = document.getElementById("mailing-table");
  const tbody = table.querySelector("tbody");
  const headers = Array.from(table.querySelectorAll("th"));
  const searchInput = document.getElementById("mailing-list-search");
  const alphabet = document.getElementById("mailing-list-alphabet");
  const alphabetButtons = Array.from(alphabet.querySelectorAll("button"));

  let sortState = [];
  let activeLetter = "";

  const columnIndex = {
    last_name: 0,
    affiliation_main: 1,
    country: 2
  };

  function getCellValue(row, index) {
    const cell = row.children[index];
    return (cell.dataset.value || cell.textContent).trim();
  }

  function compareRows(rowA, rowB, criteria) {
    for (const criterion of criteria) {
      const idx = columnIndex[criterion.column];
      const a = getCellValue(rowA, idx);
      const b = getCellValue(rowB, idx);

      const cmp = a.localeCompare(b, undefined, { sensitivity: "base" });

      if (cmp !== 0) {
        return criterion.direction === "asc" ? cmp : -cmp;
      }
    }

    return 0;
  }

  function updateIndicators() {
    headers.forEach(th => {
      th.classList.remove("sorted-asc", "sorted-desc", "sorted-secondary");
      th.querySelector(".sort-indicator").textContent = "";
    });

    sortState.forEach((criterion, i) => {
      const th = table.querySelector(`th[data-column="${criterion.column}"]`);
      if (!th) return;

      th.classList.add(
        criterion.direction === "asc" ? "sorted-asc" : "sorted-desc"
      );

      if (i > 0) {
        th.classList.add("sorted-secondary");
      }

      th.querySelector(".sort-indicator").textContent =
        criterion.direction === "asc" ? "▲" : "▼";
    });
  }

  function sortTable() {
    const rows = Array.from(tbody.querySelectorAll("tr"));

    rows.sort((a, b) => compareRows(a, b, sortState));

    rows.forEach(row => tbody.appendChild(row));

    updateIndicators();
  }

  function filterTable() {
    const query = searchInput.value.trim().toLowerCase();

    Array.from(tbody.querySelectorAll("tr")).forEach(row => {
      const text = row.textContent.toLowerCase();

      const name = getCellValue(row, 0);
      const firstLetter = name.charAt(0).toUpperCase();

      const matchesSearch = text.includes(query);
      const matchesLetter =
        activeLetter === "" || firstLetter === activeLetter;

      row.style.display =
        matchesSearch && matchesLetter ? "" : "none";
    });
  }

  function updateAlphabetAvailability() {
    const existingLetters = new Set(
      Array.from(tbody.querySelectorAll("tr"))
        .map(row => getCellValue(row, 0).charAt(0).toUpperCase())
    );

    alphabetButtons.forEach(button => {
      const letter = button.dataset.letter;

      if (letter === "") return;

      button.disabled = !existingLetters.has(letter);
    });
  }

  headers.forEach(th => {
    th.addEventListener("click", function (event) {
      const column = th.dataset.column;
      const existingIndex = sortState.findIndex(
        x => x.column === column
      );

      if (event.shiftKey) {
        if (existingIndex >= 0) {
          sortState[existingIndex].direction =
            sortState[existingIndex].direction === "asc"
              ? "desc"
              : "asc";
        } else {
          sortState.push({
            column,
            direction: "asc"
          });
        }
      } else {
        if (existingIndex >= 0 && sortState.length === 1) {
          sortState[0].direction =
            sortState[0].direction === "asc"
              ? "desc"
              : "asc";
        } else {
          sortState = [{
            column,
            direction: "asc"
          }];
        }
      }

      sortTable();
    });
  });

  searchInput.addEventListener("input", filterTable);

  alphabetButtons.forEach(button => {
    button.addEventListener("click", function () {
      activeLetter = button.dataset.letter;

      alphabetButtons.forEach(b =>
        b.classList.remove("active")
      );

      button.classList.add("active");

      filterTable();
    });
  });

  updateAlphabetAvailability();
});
</script>
