---
layout: page
title: Mailing list
---

The OMGN is open to all researchers with an interest in oomycetes, from disciplines ranging from molecular genetics and genomics to biology, population biology, and ecology, at either an experimental or a computational level. Investigators new to the field are always welcome, for example, those interested in saprophytes and animal pathogens.

- To join, fill in <a href="https://airtable.com/app4z85HJOGeEMGUc/shrsOfTvREXfUnwoT" target="_blank" rel="noopener">this form</a>.
- To send an email to the mailing list, email omgn-users AT lists DOT oregonstate DOT edu.
- To update your information or request removal, <a href="mailto:contact@oomycetes.com">contact us</a>.

Current members are listed below.

<div class="mailing-list-controls">
  <input
    type="search"
    id="mailing-list-search"
    placeholder="Search by name, affiliation, or country..."
    aria-label="Search the mailing list"
  >
</div>

<table class="mailing-table" id="mailing-table">
  <thead>
    <tr>
      <th data-column="last_name">Last name <span class="sort-indicator"></span></th>
      <th data-column="first_name">First name <span class="sort-indicator"></span></th>
      <th data-column="affiliation_main">Affiliation <span class="sort-indicator"></span></th>
      <th data-column="country">Country <span class="sort-indicator"></span></th>
    </tr>
  </thead>
  <tbody>
    {% assign sorted = site.data.mailing_list | sort: "sort_name" %}
    {% for person in sorted %}
      <tr>
        <td data-value="{{ person.last_name | downcase }}">{{ person.last_name }}</td>
        <td data-value="{{ person.first_name | downcase }}">{{ person.first_name }}</td>
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

  let sortState = [];

  const columnIndex = {
    last_name: 0,
    first_name: 1,
    affiliation_main: 2,
    country: 3
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

      th.classList.add(criterion.direction === "asc" ? "sorted-asc" : "sorted-desc");
      if (i > 0) th.classList.add("sorted-secondary");

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

  headers.forEach(th => {
    th.addEventListener("click", function (event) {
      const column = th.dataset.column;
      const existingIndex = sortState.findIndex(x => x.column === column);

      if (event.shiftKey) {
        if (existingIndex >= 0) {
          sortState[existingIndex].direction =
            sortState[existingIndex].direction === "asc" ? "desc" : "asc";
        } else {
          sortState.push({ column, direction: "asc" });
        }
      } else {
        if (existingIndex >= 0 && sortState.length === 1) {
          sortState[0].direction = sortState[0].direction === "asc" ? "desc" : "asc";
        } else {
          sortState = [{ column, direction: "asc" }];
        }
      }

      sortTable();
    });
  });

  searchInput.addEventListener("input", function () {
    const query = searchInput.value.trim().toLowerCase();

    Array.from(tbody.querySelectorAll("tr")).forEach(row => {
      const text = row.textContent.toLowerCase();
      row.style.display = text.includes(query) ? "" : "none";
    });
  });
});
</script>
