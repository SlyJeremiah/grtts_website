# November 2026 newsletter — Southern African Wildlife College

Everything here is ready to paste into the Django admin on grtts.co.zw.
The three photographs are already committed to `static/images/newsletter/2026-11-sawc/`
and will be live on the CDN as soon as this branch is deployed.

**Deploy first, then send.** The email references the photos by their public URL.
If you send the campaign before the deploy finishes, subscribers get broken images.

---

## 1. The email campaign

**Admin → Main → Newsletter campaigns → Add**

| Field | Value |
| --- | --- |
| Title | `Two senior rangers at the Southern African Wildlife College` |
| Subject | `GRTTS field report — training in South Africa, snares at home` |
| Content | paste the whole of `campaign-content.html` |

The title is printed as the headline inside the email. The subject is what people
see in their inbox.

Alternative subject lines, if you prefer:

- `What our rangers learned in South Africa — and what they came home to`
- `Field report: the Wildlife College, and the snare line`

Save, then tick the campaign in the list and run **Send selected newsletters**.

---

## 2. The blog post

**Admin → Blog → Posts → Add**

| Field | Value |
| --- | --- |
| Title | `Two senior rangers at the Southern African Wildlife College` |
| Slug | `senior-rangers-southern-african-wildlife-college` |
| Category | pick an existing one — News or Training |
| Status | `Published` |
| Content | paste the whole of `blog-post-content.html` |
| Excerpt | see below |
| Meta description | see below |
| Featured image | upload `static/images/newsletter/2026-11-sawc/sawc-group.jpg` |

**Excerpt**

> Two of our senior rangers spent November at the Southern African Wildlife College,
> studying how wildlife moves across a landscape and how operations are planned around
> it. Back home, the deployed teams were working the snare line.

**Meta description**

> GRTTS sent two senior rangers to the Southern African Wildlife College for training in
> wildlife movements and operations, while deployed teams continued clearing wire snares
> across Zimbabwean conservation land.

The featured image is what shows on the blog index and in link previews, so it is worth
uploading even though the same photo appears inside the post.

---

## 3. Check these before you publish

I wrote the copy from the photographs and your one-line brief, so a few statements are
my reading rather than your facts. Change anything that is wrong:

- **The college's name.** You wrote "The South African Wildlife College". The sign in
  the photograph reads **Southern** African Wildlife College, which is the institution
  in South Africa, so that is what I used.
- **What the programme covers.** I described wildlife movements and operations as
  seasonal movement plus patrol, capture and translocation planning. If the syllabus was
  narrower or broader, correct the second paragraph.
- **The rangers are not named.** Add their names if you want them credited.
- **Timing.** The copy says "this month". If the course ran earlier, change it.
- **Where the snared animals were found.** I deliberately did not name a property or a
  date, because I do not know them and carcass locations are sensitive. Add them only if
  you are comfortable publishing them.
- **The group photograph** shows the whole course group, not only our two rangers. The
  caption says so. If you would rather name or point out your two, say so.

---

## Files

| File | What it is |
| --- | --- |
| `campaign-content.html` | paste into the campaign **Content** field |
| `blog-post-content.html` | paste into the post **Content** field |
| `../../static/images/newsletter/2026-11-sawc/sawc-group.jpg` | course group, 1080 × 810 |
| `../../static/images/newsletter/2026-11-sawc/snare-impala.jpg` | snared impala, 700 × 911 |
| `../../static/images/newsletter/2026-11-sawc/snare-zebra.jpg` | ranger lifting a snare, 700 × 915 |

All three were resized and had their EXIF metadata stripped, GPS tags included. The
originals from WhatsApp may still carry coordinates; these do not.
