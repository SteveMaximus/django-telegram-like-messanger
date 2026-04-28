# instructions for the `social_network` project

This document helps AI agents (Copilot, ChatGPT, etc.) get up to speed and stay productive.  It is based on the current layout of the repository and the conventions the human maintainers follow.

---
## 🏗️ Big‑picture architecture

* Single Django project named `social_network` with one app `users`.  All business logic lives in `users/`.
* `manage.py` is the primary entry point for running the development server, applying migrations, creating a superuser, etc.
* The default `settings.py` is largely unmodified except:
  * `crispy_forms` is installed and added to `INSTALLED_APPS`.
  * `STATICFILES_DIRS` points at the top‑level `static/` directory; `staticfiles/` is the collectstatic target.
  * Media uploads (profile pics, message attachments) are served from `media/` with `MEDIA_ROOT`/`MEDIA_URL` configured and a development `urlpatterns += static(...)` guard in `social_network/urls.py`.
* URL routing: root URL includes `users.urls`.  See `users/urls.py` for all human‑visible routes.
* Templates are stored under `users/templates/users/`.  Each view usually renders one template with the same name (e.g. `get_user.html`).

---
## 🔁 Core data flow and patterns

* **Messaging model (`users.models.Messages`)**
  * The `message` field is stored encrypted.  `Messages.save()` overrides the base method to prepend `enc:` and encrypt text by calling `users/basic_algorithms/chiphers.encrypt` (a simple XOR + base64 scheme).  Decryption is performed with `users/basic_algorithms/chiphers.decrypt`, and views must call `msg.get_decrypted()` before rendering (see `get_and_send_user_messages`).
  * Sender/receiver are stored as plain strings (`username`), not `ForeignKey` objects.  Many queries filter by `Q(sender=current_user.username, getter=for_user.username)`.
  * Messages can carry media: `image`, generic `file`, or new `video` fields (upload paths `images/`, `files/`, `videos/`).  Templates inspect each and render appropriate `<img>`, `<video>`, or download link.
  * Attachments are handled via `ImageField`/`FileField` with the usual `enctype="multipart/form-data"` requirement in forms.
* **Profiles**: `Profile` is a `OneToOneField` to `django.contrib.auth.models.User` with an `image` field.  The `default.jpg` file should live in `media/profile_pics`.
* **Rubrics**: simple `CharField` model used nowhere yet; treat as a tag/tag‑category placeholder.

---
## ⚙️ Developer workflows

1. **Environment setup**
   ```bash
   python -m venv .venv                # or your preferred tool
   .\.venv\Scripts\activate         # Windows
   pip install django==4.2 crispy-forms
   ```
   (no `requirements.txt` is present; install additional libs as needed.)
2. **Database**
   ```bash
   python manage.py makemigrations  # regenerate when you change models
   python manage.py migrate
   ```
   The project uses SQLite (`db.sqlite3`).
3. **Running the server**
   ```bash
   python manage.py runserver
   ```
4. **Static/media**
   * Use `python manage.py collectstatic` before deploying or when adding CSS/JS under `static/`.
   * In dev `DEBUG` mode the app automatically serves `MEDIA_ROOT` via `static()`.
5. **Admin**
   ```bash
   python manage.py createsuperuser
   ```
   Registered models: `Rubric`, `Messages`, `Profile` (see `users/admin.py`).
6. **Testing**
   Tests are currently empty (`users/tests.py`).  Follow `django.test.TestCase` conventions when you add tests.

> **Note:** Most views use `@login_required`.  Some (about, user list) are intentionally left open; don’t add `login_required` unless the feature needs it.

---
## 📁 Project‑specific conventions

* All application code lives in `users/`.  If you add another app, mirror the naming and URL‑include pattern.
* Russian strings appear in model `verbose_name` attributes and templates.  Keep them if editing UI text unless asked to internationalize.
* `messages` framework is used for flash notices (see `views.register`).
* Views often return `redirect('member', user_id=user_id)` or `HttpResponseRedirect(request.META.get('HTTP_REFERER'))` after deletion.
* File and image uploads use `upload_to="…"` relative to `MEDIA_ROOT`.

---
## 🔗 Integration points & dependencies

* External libs: `django`, `crispy_forms` (templating).  No other third‑party code is included.
* Encryption uses `settings.SECRET_KEY` via the XOR cipher; changing the key will invalidate all stored messages unless you re‑encrypt them.
* The user authentication system is Django’s built‑in one (`django.contrib.auth`).  Views import `auth_views` for login/logout.

---
## 📝 Adding new features

* New URLs → add to `users/urls.py` and corresponding view/template.
* Data migrations (e.g. changing message encryption) should live in `users/migrations/`.
* When interacting with messages programmatically, always call `get_decrypted()` before display and expect the stored `message` value to start with `"enc:"`.
* Use `request.user.username` consistently; do not mix User objects and username strings.

---
## 📌 What not to do

* Don’t bypass the encryption code by writing directly to `Messages.message` unless you explicitly want plain text (rare).
* Avoid adding hard‑coded URLs; use `reverse()` or name-based `redirect()`.
* Don’t rely on uncommitted templates or static files; everything is checked into Git.

---
## ✅ Where to look when stuck

* `users/models.py` — data layer and encryption logic.
* `users/views.py` — main request handlers and query patterns.
* `users/forms.py` — forms tied to models.
* `users/urls.py` — how routes are named and wired.
* `social_network/settings.py` — static/media configuration and installed apps.


> **Feedback requested:** Are there any workflows or patterns I missed?  Let me know if parts of the app feel unclear so I can iterate on these instructions.