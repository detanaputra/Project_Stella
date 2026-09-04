# Cycle 0

#cycle0 #formal_record #shapr

## Cycle Title
Planning and Brainstorming with the AI Coding Partner

## Context
Canonical SHAPR mandates documenting and reviewing each cycle at its close. However, this project had already taken the shape of a cycle 1 by the time SHAPR was fully adopted. This cycle 0 note serves as a development artefact to document the situation before adopting SHAPR, and provides an honest reflection on the idea development during the initial phase.

## Concept
- The development of this tool began on the advice of the supervisor, with the idea of automating the toolchain used in the research thesis for the graduation project. The purpose of this tool is to democratize topic modelling for social scientists or practitioners who often do not have programming capability. Initially, the mechanism was written purely in a VS Code notebook. As the project's goal shifted, the Python notebook was then rewritten using a Python interface.
- Two interface frameworks were considered: ttkbootstrap, which extends tkinter, and PyQt. ttkbootstrap was considered achievable, with a leaner learning curve than the latter, since the ultimate purpose of this project is only a Minimum Viable Product until graduation.

## MVP
As this graduation project is limited by a one-semester time constraint, the Minimum Viable Product is defined as follows:
1. Topic modelling tools that leverage BERTopic's capabilities
2. The capabilities are limited to: training, hyperparameter tuning, displaying some visualisations, topic refinement (delete and merge), and topic interpretation (adding user interpretation or a user label to a topic)

## Tools
To help speed up development, code generation will be done using the Claude Code CLI with the Ollama model. The author takes full responsibility for the completion of the tool.

## Definition of Success
This graduation project is considered complete when the MVP is completed and the research thesis is submitted. The submitted app will be considered an alpha version because of the limited testing environment. The next development phase will be done after graduation.

## Verdict
This cycle note serves as a development artefact only and does not need a review, as this cycle does not decide anything.
