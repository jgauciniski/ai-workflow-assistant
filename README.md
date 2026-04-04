# AI Workflow Assistant

AI workflow system using LLMs for structured extraction and classification.

## Overview

This project demonstrates a simple multi-step AI pipeline built with Python and the OpenAI API.

It processes unstructured support tickets and turns them into structured JSON, then enriches that data with AI-generated priority classification.

## Features

- Extracts structured fields from raw support ticket text
- Returns machine-readable JSON
- Parses JSON into Python data structures
- Saves processed data to disk
- Loads stored data for downstream processing
- Classifies tickets by priority using a second AI step
- Saves enriched results to a new JSON file

## Project Structure

```text
ai-workflow-assistant/
├── llm.py
├── main.py
├── read_data.py
├── processed_tickets.json
├── enriched_tickets.json
├── .gitignore
└── README.md