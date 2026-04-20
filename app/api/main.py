from fastapi import FastAPI
from pydantic import BaseModel

from app.session import Session
from app.services import handle_ticket, handle_question
from app.commands import execute_command
from app.utils.formatters import format_ticket_for_display


app = FastAPI(title="AI Workflow Assistant API")

api_session = Session()


class TicketRequest(BaseModel):
    text: str


class QuestionRequest(BaseModel):
    question: str


class HandleCommandRequest(BaseModel):
    command: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/tickets")
def create_ticket(request: TicketRequest):
    enriched_ticket = handle_ticket(api_session, request.text)

    return {
        "message": "Ticket processed successfully",
        "ticket": format_ticket_for_display(enriched_ticket),
        "total_tickets": len(api_session.tickets),
    }


@app.post("/questions")
def ask_question(request: QuestionRequest):
    answer, relevant_tickets = handle_question(api_session, request.question)

    return {
        "question": request.question,
        "answer": answer,
        "relevant_tickets": [
            format_ticket_for_display(ticket)
            for ticket in relevant_tickets
        ],
        "total_tickets": len(api_session.tickets),
    }


@app.post("/commands")
def handle_commands(request: HandleCommandRequest):
    return execute_command(request.command, api_session)