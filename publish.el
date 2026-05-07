;;; publish.el --- Org-to-HTML fragment export config  -*- lexical-binding: t; -*-

(require 'org)
(require 'ox-html)

(setq org-html-head-include-default-style nil)
(setq org-html-head-include-scripts nil)
(setq org-html-htmlize-output-type nil)
(setq org-html-validation-link nil)
(setq org-export-with-author nil)
(setq org-export-with-date nil)
(setq org-export-with-title nil)
(setq org-export-with-toc nil)
(setq org-export-with-section-numbers nil)

;; ---------- Export function ----------

(defun blog-export-file (input-file output-file)
  "Export INPUT-FILE (.org) to OUTPUT-FILE (.html fragment)."
  (with-current-buffer (find-file-noselect input-file)
    (let ((org-export-show-temporary-export-buffer nil)
          (org-html-divs '((preamble "div" "preamble")
                           (content "div" "content")
                           (postamble "div" "postamble"))))
      (org-export-to-file 'html output-file nil nil nil t nil))))
