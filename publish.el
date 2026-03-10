;;; publish.el --- Org-to-HTML export config for the blog  -*- lexical-binding: t; -*-

(require 'ox-html)
(require 'org)

;; ---------- CSS matching index.html paper style ----------

(defvar blog-css "
body {
  font-family: Georgia, 'Times New Roman', Times, serif;
  line-height: 1.6;
  color: #000;
  background-color: #fff;
  max-width: 800px;
  margin: 0 auto;
  padding: 1em;
}
h1, h2, h3, h4, h5, h6 { color: #000; margin: 0 0 0.5em 0; }
h1 { font-size: 1.5em; margin-bottom: 0.2em; }
h2 { font-size: 1.3em; margin-top: 1em; }
h3 { font-size: 1.1em; }
p, ul, ol, table, pre, dl { margin: 0 0 1em 0; }
a { color: #00e; text-decoration: none; }
a:visited { color: #551a8b; }
a:hover { text-decoration: underline; }
blockquote { border-left: 2px solid #999; margin: 0.5em 0; padding-left: 1em; color: #555; }
code, pre { font-family: 'Courier New', Courier, monospace; font-size: 0.9em; }
pre { background: #f4f4f4; padding: 0.5em; overflow-x: auto; }
hr { border: none; border-top: 1px solid #999; margin: 1.5em 0; }
strong { font-weight: bold; }
header, footer { margin: 1em 0; }
footer { margin-top: 2em; padding-top: 1em; border-top: 1px solid #999; font-size: 0.85em; color: #555; }
table { border-collapse: collapse; width: 100%; }
table td, table th { border: 1px solid #ddd; padding: 0.4em 0.8em; }
table th { background: #f4f4f4; font-weight: bold; }
.title { margin-bottom: 0.1em; }
.date { color: #555; font-size: 0.95em; margin-bottom: 1em; }
.author { color: #555; font-size: 0.95em; }
.org-src-container { margin: 0 0 1em 0; }
")

;; ---------- Export settings ----------

(setq org-html-doctype "html5")
(setq org-html-html5-fancy t)
(setq org-html-head-include-default-style nil)
(setq org-html-head-include-scripts nil)
(setq org-html-head (format "<style>%s</style>" blog-css))

;; Preamble: back to home link
(setq org-html-preamble t)
(setq org-html-preamble-format
      '(("en" "<nav style=\"margin-bottom:1em\"><a href=\"/\">&larr; Home</a></nav>")))

;; Postamble: site footer
(setq org-html-postamble t)
(setq org-html-postamble-format
      '(("en" "<footer><p>It is possible to build a cabin with no foundations, but not a lasting building.</p></footer>")))

;; Content settings
(setq org-html-validation-link nil)
(setq org-export-with-toc nil)
(setq org-export-with-section-numbers nil)
(setq org-export-with-date t)
(setq org-export-with-author t)
(setq org-html-htmlize-output-type nil)

;; ---------- Filter: inject date/author after title ----------

(defun blog-inject-metadata (output backend info)
  "Insert date and author after the <h1> title in the exported HTML."
  (let* ((date (plist-get info :date))
         (author (plist-get info :author))
         (date-str (when date (org-export-data date info)))
         (author-str (when author (org-export-data author info)))
         (meta ""))
    (when (and date-str (not (string-empty-p date-str)))
      (setq meta (concat meta (format "<p class=\"date\">%s</p>\n" date-str))))
    (when (and author-str (not (string-empty-p author-str)))
      (setq meta (concat meta (format "<p class=\"author\">%s</p>\n" author-str))))
    (if (string-empty-p meta)
        output
      (replace-regexp-in-string "</header>" (concat meta "</header>") output nil t))))

(add-to-list 'org-export-filter-final-output-functions #'blog-inject-metadata)

;; ---------- Export function ----------

(defun blog-export-file (input-file output-file)
  "Export INPUT-FILE (.org) to OUTPUT-FILE (.html)."
  (with-current-buffer (find-file-noselect input-file)
    (let ((org-export-show-temporary-export-buffer nil))
      (org-export-to-file 'html output-file nil nil nil nil nil))))
