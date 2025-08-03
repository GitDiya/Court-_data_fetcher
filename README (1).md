---
title: Court Data Fetcher
emoji: 🚀
colorFrom: gray
colorTo: pink
sdk: docker
pinned: false
license: mit
short_description: This project is about fetching any court details.
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference



# Court Data Fetcher & Mini-Dashboard

## Objective
A Flask-based web app to fetch case details, parties, hearing dates, and PDF orders from Indian courts.

## Target Court
- Faridabad District Court (https://districts.ecourts.gov.in/)

## Features
- HTML UI with Flask backend.
- Case type, case number, and filing year inputs.
- SQLite database for logging queries and raw responses.
- PDF download links.
- Error handling.

## Deployment
Designed for Hugging Face Spaces.
- Create new Space → Select SDK: `Docker` (or `Python + Flask`).
- Upload `app.py`, `requirements.txt`, `templates/`, and `README.md`.
- Hugging Face will deploy and run on port `7860`.

