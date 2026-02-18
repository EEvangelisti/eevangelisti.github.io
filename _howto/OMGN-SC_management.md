## Updating a Steering Committee Member

The Steering Committee page is generated automatically from the data file:

```
_data/committee.yml
```

Each member corresponds to one YAML entry.

### To Modify an Existing Member
- Open `_data/committee.yml`
- Locate the relevant member entry, e.g.:

```
- name: Anton de Bary
  role: Member
  affiliation: Eberhard Karls Universität
  url: https://en.wikipedia.org/wiki/Heinrich_Anton_de_Bary
  photo: AntonDeBary.jpg
```

- Edit the relevant fields: name, role, affiliationn url, photo.
- Commit and push the changes.

The website will update automatically via GitHub Pages.

### To Add a New Member
- Add a new YAML block at the end of `_data/committee.yml`:

```
- name: New Member
  role: Member
  affiliation: Institution
  url: https://example.org/profile
  photo: new_member.jpg
```

- Upload the corresponding photo to `assets/images/steering/`
- Ensure the filename matches exactly (case-sensitive).
- Commit and push.

### To Remove a Member
- Delete the corresponding YAML block from `_data/committee.yml`.
- Commit and push.
- (Optional: you may remove the photo file from `assets/images/steering/`.)

### Important Notes
- YAML indentation must use spaces only (no tabs).
- Each member entry begins with `-` followed by a space.
- File names are case-sensitive.
- If a url field is omitted, the name will be displayed without a hyperlink.
- The page is automatically generated using a Liquid loop in committee.md, so no manual HTML editing is required when updating members.

